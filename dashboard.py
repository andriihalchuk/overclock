from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_session_data():
    conn = sqlite3.connect("overclock.db")
    cursor = conn.cursor()
    
    # get timestamp and duration for the first chart
    cursor.execute("SELECT timestamp, duration_seconds FROM sessions")
    rows = cursor.fetchall()
    conn.close()
    
    # two lists for the chart
    dates = []
    minutes = []
    
    for row in rows:
        dates.append(row[0].split(" ")[0]) 
        minutes.append(round(row[1] / 60, 2))
        
    return dates, minutes
    
@app.route("/")
def home():
    dates, minutes = get_session_data()

    return render_template(
        "index.html"
        , chart_labels=dates
        , chart_data=minutes
        )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
