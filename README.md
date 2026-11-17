# Smart Task Hub - Python Full Stack Demo
Flask (Python) + SQLite (SQL) + HTML / CSS / JavaScript. Built for VS Code.

## 1. One-time setup
1. Install Python 3.10+ (python.org). On Windows tick "Add Python to PATH".
2. Install VS Code (code.visualstudio.com) and its "Python" extension.
3. Unzip this folder. In VS Code: File > Open Folder > choose `task_hub_flask`.
4. Open the terminal: Terminal > New Terminal. Run:

    python -m venv venv
    venv\Scripts\activate            (Windows)
    source venv/bin/activate         (Mac/Linux)
    pip install -r requirements.txt

(Windows PowerShell blocked the activate script? Run:
 Set-ExecutionPolicy -Scope Process Bypass   and try again.)

## 2. Run the project
    python reset_db.py     # creates tasks.db with sample tasks (run before every demo)
    python app.py

Open http://127.0.0.1:5000 in your browser. Press Ctrl+C in the terminal to stop.

## 3. Files and what to say about each
- schema.sql          : SQL - creates the tasks table and sample rows (database layer)
- app.py              : Python Flask backend - REST API (/api/tasks) and SQLite queries
- static/index.html   : page structure (HTML)
- static/style.css    : styling (CSS)
- static/app.js       : JavaScript - calls the API with fetch() and updates the page
- reset_db.py         : resets demo data

## 4. Demo script (about 5 minutes)
1. Show the folder in VS Code and explain the 3 layers (frontend / backend / database).
2. Open schema.sql: "This is the SQL table design."
3. Open app.py: show one route, e.g. create_task, and its INSERT query.
4. Open app.js: show the fetch() call that talks to the API.
5. Run `python app.py`, open the browser.
6. Dashboard: point out Total / Pending / Completed counters.
7. Add a task (title, priority, due date). Counter updates instantly.
8. Edit the task (Edit button), then Update.
9. Click Done: title is struck through, counters change.
10. Use the filters (All / Pending / Done) and the Search box.
11. Try adding an empty title: show the validation error.
12. Delete a task and confirm.
13. Bonus: open http://127.0.0.1:5000/api/tasks to show the raw JSON the backend returns.
14. Bonus: press F12 > Network tab, add a task, and show the POST request.

## 5. If something goes wrong
- "python not found": use `py` instead of `python` (Windows) or `python3` (Mac/Linux).
- "No module named flask": the venv is not active. Activate it and run pip install again.
- Port busy: change the last line of app.py to app.run(debug=True, port=5001).
- Messy data: run python reset_db.py and restart.
- Take screenshots beforehand as a backup for the "Output Screens" slide.
