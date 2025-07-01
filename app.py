from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB_FILE = "registrations.db"

# Create table if it doesn't exist
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                name TEXT,
                gender TEXT,
                father TEXT,
                mother TEXT,
                dob TEXT,
                email TEXT,
                code TEXT,
                mobile TEXT,
                aadhaar TEXT,
                occupation TEXT,
                address TEXT,
                category TEXT
            )
        ''')

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    data = (
        request.form['title'],
        request.form['name'],
        request.form['gender'],
        request.form['father'],
        request.form['mother'],
        request.form['dob'],
        request.form['email'],
        request.form['code'],
        request.form['mobile'],
        request.form['aadhaar'],
        request.form['occupation'],
        request.form['address'],
        request.form['other'] if request.form['category'] == "Other" else request.form['category']
    )

    # Save to database
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            INSERT INTO registrations (
                title, name, gender, father, mother, dob, email, code, mobile, aadhaar, occupation, address, category
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)

    return render_template('thankyou.html')

@app.route('/view')
def view():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute('SELECT title, name, category FROM registrations')
        entries = [{'name': f"{row[0]} {row[1]}", 'category': row[2]} for row in cursor]
    return render_template('view.html', entries=entries)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

if __name__ == '__main__':
    init_db()  # ✅ Creates the database if it doesn't exist
    ...

