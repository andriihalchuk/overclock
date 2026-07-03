import os
import platform 
import ctypes
import questionary
import time
import sqlite3
from datetime import datetime
import webbrowser

# get host path based on the OS
if platform.system() == "Windows":
    HOST_PATH = r"C:\Windows\System32\drivers\etc\hosts"
else:
    HOST_PATH = "/etc/hosts" # mac and linux

REDIRECT_IP = "127.0.0.1" # local host
STARTED_MARKER = "# --- FOCUS MODE ACTIVATED --- \n"
ENDED_MARKER   = "# --- FOCUS MODE DISABLED --- \n"

#BLOCKED_SITES = ["instagram.com", "www.instagram.com"]

# check if the user has admin previleges
def is_admin():
    if platform.system() == "Windows":
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    else:
        return os.geteuid() == 0 # mac and linux
    
# find AppData directory to stare the database
def get_app_dir():
    home = os.path.expanduser("~")
    system = platform.system()

    if system == "Windows":
        # go to AppData\Local
        base = os.environ.get("LOCALAPPDATA", os.path.join(home, "AppData", "Local"))
    elif system == "Darwin":
        # go to ~/Library/Application Support (mac)
        base = os.path.join(home, "Library", "Application Support")
    else:
        # go to ~/.local/share (linux)
        base = os.environ.get("XDG_DATA_HOME", os.path.join(home, ".local", "share"))

    app_dir = os.path.join(base, "Overclock")

    #create folder if it does not exist yet
    os.makedirs(app_dir, exist_ok=True)
    return app_dir

APP_DIR = get_app_dir
DB_PATH = os.path.join(APP_DIR, "overclock.db")

# block specified sites
def block_sites(restricted_sites):
    if not is_admin():
        print("Admin previleges required for the script to run")
        return 

    # read current file
    with open(HOST_PATH, "r") as file:
        content = file.readlines()

    # cannot double-block
    if STARTED_MARKER in content:
            print("The focus mode is already enabled")
            return

    with open(HOST_PATH, "a") as file:
        file.write(STARTED_MARKER)
        for site in restricted_sites:
            # make host ip address an ip address of each forbidden site
            file.write(f"{REDIRECT_IP} {site}\n") 

            file.write(f"{REDIRECT_IP} www.{site}\n") 

            file.write(f"{REDIRECT_IP} m.{site}\n")

            file.write(f"{REDIRECT_IP} login.{site}\n")  
        file.write(ENDED_MARKER)

    print("Focus mode is activated. Work hard")

# unblock specified sites
def unblock_sites():
    if not is_admin():
        print("Admin previleges required for the script to run")
        return 
    
    with open(HOST_PATH, "r") as file:
        content = file.readlines()

    with open(HOST_PATH, "w") as file:
        in_focus_block = False
        for line in content:
            if line == STARTED_MARKER:
                in_focus_block = True
                continue

            # ignore all lines in focus block
            if not in_focus_block:
                file.write(line)

            if line == ENDED_MARKER:
                in_focus_block = False
        
    print("Focus mode is disabled")

'''
# code for when i mess up
# delete every line that has marker in it
def clean_up():
    if not is_admin():
        print("Admin previleges required for the script to run")
        return 
    
    with open(HOST_PATH, "r") as file:
        content = file.readlines()

    with open(HOST_PATH, "w") as file:
        skip_line = False
        for line in content:
            if STARTED_MARKER in line or ENDED_MARKER in line:
                continue

            file.write(line)
'''
# initialise data store
def init_db():
    # create "database" file if it does not exist yet
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # create table with data we want to save
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            duration_seconds INTEGER,
            completed_tasks TEXT,
            missed_tasks TEXT,
            failure_reason TEXT
        )
    ''')

    conn.commit()
    conn.close()

# log information from lockin session to the store
def log_session(duration, completed, missed, reason):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # get current date and time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # format tasks
    completed_str = ", ".join(completed)
    missed_str = ", ".join(missed)

    cursor.execute('''
        INSERT INTO sessions (timestamp, duration_seconds, completed_tasks, missed_tasks, failure_reason)
        VALUES (?, ?, ?, ?, ?)
    ''', (current_time, duration, completed_str, missed_str, reason))

    conn.commit()
    conn.close()


# session initiation
def start_session():
    
    init_db()

    action_choice = questionary.select(
        "What do you want to do?",
        choices = ["Overclock", "View my overclock data"]
    ).ask()

    if action_choice == "View my overclock data":
        print("\nOpening your dashboard...")
        time.sleep(1)
        webbrowser.open("http://127.0.0.1:5000")

    duration_choice = questionary.select(
        "For how long do you want to overclock?",
        choices = ["10 seconds", "30 minutes", "1 hour", "1.5 hours", "2 hours", "Custom"], 
    ).ask()

    # convert lockin time to seconds
    duration_map = {
        "10 seconds" : 10,
        "30 minutes" : 1800,
        "1 hour" : 3600,
        "1.5 hours" : 5400,
        "2 hours" : 7200
    }

    if duration_choice == "Custom":
        
        custom_duration = questionary.text("What is your custom overclock duration? (e.g 3 hours)").ask()

        # keep asking for custom duration until in correct format
        while True:
            # convert lockin time to seconds
            session_seconds = 0
            time_duration_str = ""
            time_type_str = ""
            for s in custom_duration:
                if s.isdigit():
                    time_duration_str += s
                elif s.isalpha():
                    time_type_str += s

            if time_type_str == "seconds" or time_type_str == "second":
                session_seconds = int(time_duration_str)
                break
            elif time_type_str == "minutes" or time_type_str == "minute":
                session_seconds = int(time_duration_str) * 60
                break
            elif time_type_str == "hours" or time_type_str == "hour":
                session_seconds = int(time_duration_str) * 3600 
                break
            else:
                custom_duration = questionary.text("Wrong duration format, try again (e.g. 2.5 hours)")
        # choose from the map
    else:
        session_seconds = duration_map[duration_choice]

    # select sites to block
    restricted_sites = questionary.checkbox(
        "Choose sites to block:",
        choices = [ "youtube.com",
                    "reddit.com",
                    "instagram.com",
                    "facebook.com",
                    "x.com",
                    "tiktok.com",
                    "netflix.com",
                    "twitch.tv",
                    "discord.com",
                    "pinterest.com",
                    "amazon.co.uk"]
        ).ask() or []
    #print(restricted_sites)

    # gather tasks to split later
    tasks = questionary.text(
        "What tasks do you want to complete? (use ';' to separate them)\n"
    ).ask()

    # separate each task without spaces at the start/end
    tasks_separated = [task.strip() for task in tasks.split(";")]


    print("\nInitialising overclock...")
    block_sites(restricted_sites)

    end_time = time.time() + session_seconds

    forced_exit_text = "q"#"i acknowledge that i am breaking focus for a valid emergency"

    try:
        # sleep until time is up or force exit when "ctrl C" is pressed
        while time.time() < end_time:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                print("\n\nForced exit")

                override = questionary.text(
                    f"Type this message to abort:\n\n '{forced_exit_text}'\n"
                ).ask()

                # allow exit only if message typed correctly
                if override == forced_exit_text:
                    print("\nSession is aborted")
                    break
                else:
                    print("\nTry again or get back to work")

        # if forced exit -> skip this
        if time.time() > end_time:
            print("\nSession complete")
            completed_tasks = questionary.checkbox(
                "What tasks have you finished?",
                choices = tasks_separated
            ).ask()
            # if user have not finished all tasks identify tasks missed and ask
            # for a reason why they did not finish them
            missed_tasks = list(set(tasks_separated) - set(completed_tasks))
            reason = "none"

            if missed_tasks:
                reason = questionary.select(
                    "Why haven't you finished all tasks?",
                    choices = ["Underestimated other tasks' duration and complexity", "Distractions or loss of focus slowed the progress", "Interruptions or outside dependencies caused delays", "Too much was planned or priorities changed", "Low energy, stress, or perfectionism made the progress harder"]
                ).ask()
                # use reasons later for the dashboard
            log_session(session_seconds, completed_tasks, missed_tasks, reason)
    # ensure sites are unblocked even when forcefully exited
    finally:

        unblock_sites()

        dashboard_view_choice = questionary.confirm("Would you like to view your overclock dashboard?").ask()

        if dashboard_view_choice:
            print("\nOpening your dashboard...")
            try:
                os.system("python dashboard.py")
                webbrowser.open_new("http://127.0.0.1:5000")
            except KeyboardInterrupt:
                print("\nExited dashboard")

if __name__ == "__main__":
    start_session()
    pass