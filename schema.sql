-- Smart Task Hub database schema (SQLite)
DROP TABLE IF EXISTS tasks;

CREATE TABLE tasks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    priority    TEXT    NOT NULL DEFAULT 'Medium'
                CHECK (priority IN ('Low', 'Medium', 'High')),
    due_date    TEXT,
    is_done     INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Sample rows for the demo
INSERT INTO tasks (title, priority, due_date, is_done) VALUES
    ('Finish internship report', 'High',   date('now', '+2 day'), 0),
    ('Prepare presentation slides', 'High', date('now', '+1 day'), 1),
    ('Practice project demo', 'Medium',    date('now', '+3 day'), 0),
    ('Revise Python and SQL basics', 'Low', NULL, 0);
