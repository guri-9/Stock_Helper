import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g

app = Flask(__name__)
DATABASE = "stock.db"

STATUSES = ["Full", "Low", "Empty"]


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            aisle TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Full',
            leftover_boxes INTEGER NOT NULL DEFAULT 0,
            note TEXT DEFAULT '',
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    db.commit()
    db.close()


@app.route("/")
def index():
    view = request.args.get("view", "all")
    db = get_db()
    if view == "restock":
        # Shelf is low or empty and needs product from the back
        rows = db.execute(
            "SELECT * FROM items WHERE status IN ('Low', 'Empty') ORDER BY aisle, name"
        ).fetchall()
    elif view == "overstock":
        # Shelf is full but boxes are still left over
        rows = db.execute(
            "SELECT * FROM items WHERE status = 'Full' AND leftover_boxes > 0 ORDER BY aisle, name"
        ).fetchall()
    else:
        rows = db.execute("SELECT * FROM items ORDER BY aisle, name").fetchall()
    return render_template("index.html", items=rows, view=view, statuses=STATUSES)


@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"].strip()
    aisle = request.form["aisle"].strip()
    status = request.form["status"]
    boxes = int(request.form.get("leftover_boxes") or 0)
    note = request.form.get("note", "").strip()
    if name and aisle and status in STATUSES:
        db = get_db()
        db.execute(
            "INSERT INTO items (name, aisle, status, leftover_boxes, note) VALUES (?, ?, ?, ?, ?)",
            (name, aisle, status, boxes, note),
        )
        db.commit()
    return redirect(url_for("index"))


@app.route("/update/<int:item_id>", methods=["POST"])
def update(item_id):
    status = request.form["status"]
    boxes = int(request.form.get("leftover_boxes") or 0)
    if status in STATUSES:
        db = get_db()
        db.execute(
            "UPDATE items SET status = ?, leftover_boxes = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (status, boxes, item_id),
        )
        db.commit()
    return redirect(request.referrer or url_for("index"))


@app.route("/delete/<int:item_id>", methods=["POST"])
def delete(item_id):
    db = get_db()
    db.execute("DELETE FROM items WHERE id = ?", (item_id,))
    db.commit()
    return redirect(request.referrer or url_for("index"))


if __name__ == "__main__":
    init_db()
    # host 0.0.0.0 lets your phone open it over the same Wi-Fi
    app.run(host="0.0.0.0", port=5001, debug=True)
