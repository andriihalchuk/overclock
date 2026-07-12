# Overclock

Overclock is a terminal app that helps you focus by completely blocking distracting websites. It works by temporarily editing your system's `hosts` file, meaning you literally can't load those sites until your session is up. Afterwards, you can check your progress on a built-in local dashboard.

## Features

* **System-level blocking:** Reroutes distracting sites to `127.0.0.1` through your `hosts` file, making them impossible to reach.
* **Local analytics:** An offline dashboard lets you review your session lengths and track the reasons behind any missed tasks.
* **Emergency abort:** You can end a session early and unblock everything if you absolutely need to.
* **Cross-platform:** Runs natively on Windows, macOS, and Linux.

---

## Getting Started

You don't need to install Python to use Overclock. It comes as a standalone executable.

1. Go to the [Releases page](https://www.google.com/search?q=../../releases/latest).
2. Download the right file for your operating system:
* **Windows:** `overclock-windows.exe`
* **macOS:** `overclock-mac`
* **Linux:** `overclock-linux`



---

## !! Important OS Warnings & How to Run

Since Overclock needs to edit a system file (the `hosts` file) to do its job, your operating system will probably flag it as suspicious. This is completely normal for apps that do this kind of thing. Here is how to get it running:

### Windows

1. Double-click `overclock-windows.exe`.
2. **Windows SmartScreen** will likely pop up with "Windows protected your PC."
3. Click **More info**, then **Run anyway**.
4. When the User Account Control (UAC) prompts you for administrator privileges, click **Yes**.

### macOS

1. Open your terminal.
2. If you try to run it normally, Apple's **Gatekeeper** will block it, saying it's from an "unverified developer."
3. Head into **System Settings** > **Privacy & Security**, scroll down, and click **Allow Anyway** next to the prompt about Overclock.
4. Because it needs to edit `/etc/hosts`, you'll need to run it using `sudo`:
```bash
sudo /path/to/downloads/overclock-mac

```



### Linux

1. Open your terminal and make the file executable:
```bash
chmod +x /path/to/downloads/overclock-linux

```


2. Run it with root privileges so it can edit `/etc/hosts`:
```bash
sudo ./overclock-linux

```



---

## How to Use

1. Open the app and select **Start session**.
2. Type in the tasks you want to get done (separate them with a semicolon).
3. Choose your focus duration or set a custom time.
4. Tick the websites you want to block.
5. Get to work. The app will run in the background until your time is up.
6. Once finished, tick off your completed tasks and check your dashboard if you'd like.

---

## Privacy & Data

Overclock is entirely offline. All your session data, task history, and notes on missed tasks are saved locally on your own machine in an SQLite database (`overclock.db`).

* **Windows:** `AppData/Local/Overclock/`
* **macOS:** `~/Library/Application Support/Overclock/`
* **Linux:** `~/.local/share/Overclock/`

## Licence

This project is licensed under the MIT License.
