"""Smart Task Hub - Python full stack demo
Backend : Flask (Python) + SQLite (SQL)
Frontend: HTML + CSS + JavaScript (fetch API)
"""
import sqlite3
from pathlib import Path

from flask import Flask, g, jsonify, request, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "tasks.db"
PRIORITIES = ("Low", "Medium", "High")

app = Flask(__name__, static_folder="static", static_url_path="/static")


# ---------- database helpers ----------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Run schema.sql to (re)create the table with sample data."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript((BASE_DIR / "schema.sql").read_text())


def row_to_dict(row):
    d = dict(row)
    d["is_done"] = bool(d["is_done"])
    return d


# ---------- pages ----------
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


# ---------- REST API ----------
@app.get("/api/tasks")
def list_tasks():
    status = request.args.get("status", "all")
    search = request.args.get("q", "").strip()

    sql = "SELECT * FROM tasks WHERE 1=1"
    params = []
    if status == "pending":
        sql += " AND is_done = 0"
    elif status == "done":
        sql += " AND is_done = 1"
    if search:
        sql += " AND title LIKE ?"
        params.append(f"%{search}%")
    sql += " ORDER BY is_done ASC, id DESC"

    rows = get_db().execute(sql, params).fetchall()
    stats = get_db().execute(
        "SELECT COUNT(*) AS total, COALESCE(SUM(is_done), 0) AS done FROM tasks"
    ).fetchone()
    return jsonify(
        tasks=[row_to_dict(r) for r in rows],
        total=stats["total"],
        done=stats["done"],
        pending=stats["total"] - stats["done"],
    )


@app.post("/api/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    priority = data.get("priority", "Medium")
    due_date = data.get("due_date") or None
    if not title:
        return jsonify(error="Title is required"), 400
    if priority not in PRIORITIES:
        return jsonify(error="Invalid priority"), 400

    db = get_db()
    cur = db.execute(
        "INSERT INTO tasks (title, priority, due_date) VALUES (?, ?, ?)",
        (title, priority, due_date),
    )
    db.commit()
    row = db.execute("SELECT * FROM tasks WHERE id = ?", (cur.lastrowid,)).fetchone()
    return jsonify(row_to_dict(row)), 201


@app.put("/api/tasks/<int:task_id>")
def update_task(task_id):
    data = request.get_json(silent=True) or {}
    db = get_db()
    row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        return jsonify(error="Task not found"), 404

    title = (data.get("title", row["title"]) or "").strip()
    priority = data.get("priority", row["priority"])
    due_date = data.get("due_date", row["due_date"]) or None
    is_done = int(bool(data.get("is_done", row["is_done"])))
    if not title:
        return jsonify(error="Title is required"), 400
    if priority not in PRIORITIES:
        return jsonify(error="Invalid priority"), 400

    db.execute(
        "UPDATE tasks SET title=?, priority=?, due_date=?, is_done=? WHERE id=?",
        (title, priority, due_date, is_done, task_id),
    )
    db.commit()
    row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return jsonify(row_to_dict(row))


@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id):
    db = get_db()
    cur = db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    if cur.rowcount == 0:
        return jsonify(error="Task not found"), 404
    return jsonify(deleted=task_id)


if __name__ == "__main__":
    if not DB_PATH.exists():
        init_db()
    app.run(debug=True)
