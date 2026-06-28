from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_session_data():
    conn = sqlite3.connect("overclock.db")
    cursor = conn.cursor()
    
    # get timestamp and duration for the first chart
    cursor.execute("SELECT timestamp, duration_seconds FROM sessions")
    rows = cursor.fetchall()
    
    # two lists for the chart
    dates = []
    minutes = []
    
    for row in rows:
        dates.append(row[0].split(" ")[0]) 
        minutes.append(round(row[1] / 60, 2))
        
    return dates, minutes
    
def get_failure_data():
    conn = sqlite3.connect("overclock.db")
    cursor = conn.cursor()
    
    # get failure reasons
    cursor.execute("SELECT failure_reason FROM sessions WHERE failure_reason != 'none'")
    rows = cursor.fetchall()
    conn.close()

    reason_counts = {}
    for row in rows:
        reason = row[0]
        if reason in reason_counts:
            reason_counts[reason] += 1
        else:
            reason_counts[reason] = 1

    labels = list(reason_counts.keys())
    counts = list(reason_counts.values())
    
    return labels, counts

@app.route("/")
def home():
    dates, minutes = get_session_data()
    reasons, counts = get_failure_data()

    return render_template(
        "index.html"
        , chart_labels = dates
        , chart_data = minutes
        , pie_labels = reasons
        , pie_data = counts
        )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
