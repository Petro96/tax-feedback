
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = "feedback.db"

# db init

def init_db():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        experience TEXT,
        rating INTEGER,
        comments TEXT,
        submitted_at TEXT,
        status TEXT DEFAULT 'New',
        review_notes TEXT    
    )
    """)

    conn.commit()
    conn.close()

# home page init

@app.route("/")
def home():
    return render_template("index.html")

# submit functionality

@app.route("/submit", methods=["POST"])
def submit():

    name = request.form["name"]
    email = request.form["email"]
    experience = request.form["experience"]
    rating = request.form["rating"]
    comments = request.form["comments"]
    submitted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO feedback(name,email,experience,rating,comments,submitted_at)
    VALUES(?,?,?,?,?,?)
    """, (name, email, experience, rating, comments, submitted_at))

    conn.commit()
    conn.close()

    return render_template("thank_you.html", submitted_at=submitted_at)

# display all submitted feedbacks

@app.route("/admin")
def admin():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""    
    SELECT  id,
            name,
           email,
           experience,
           rating,
           comments,
           submitted_at,status,review_notes
    FROM feedback
    ORDER BY submitted_at DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        feedback=rows
    )

# review functionality

@app.route("/review/<int:id>", methods=["POST"])
def review(id):

    status = request.form["status"]
    review_notes = request.form["review_notes"]

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE feedback
    SET status=?,
        review_notes=?
    WHERE id=?
    """,
    (status,
     review_notes,
     id))

    conn.commit()
    conn.close()

    return redirect(url_for("admin"))





if __name__ == "__main__":
    init_db()
    app.run(debug=True)