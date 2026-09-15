import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from database import init_db

app = Flask(__name__)

# Ensure database tables exist on startup
init_db()

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    campaigns = conn.execute("SELECT * FROM campaigns").fetchall()
    auto_replies = conn.execute("SELECT * FROM auto_replies").fetchall()
    conn.close()
    return render_template("dashboard.html", campaigns=campaigns, auto_replies=auto_replies)

@app.route("/campaign/add", methods=["POST"])
def add_campaign():
    name = request.form["name"]
    channel_id = request.form["channel_id"]
    message = request.form["message"]
    interval = request.form["interval"]

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO campaigns (name, channel_id, message, interval, active) VALUES (?, ?, ?, ?, 1)",
        (name, channel_id, message, interval)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/campaign/delete/<int:id>", methods=["POST"])
def delete_campaign(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM campaigns WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/autoreply/add", methods=["POST"])
def add_auto_reply():
    keyword = request.form["keyword"]
    response = request.form["response"]

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO auto_reply (keyword, response) VALUES (?, ?)" if False else "INSERT INTO auto_replies (keyword, response) VALUES (?, ?)",
        (keyword, response)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/autoreply/delete/<int:id>", methods=["POST"])
def delete_auto_reply(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM auto_replies WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
