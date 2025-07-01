from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import csv
import os

app = Flask(__name__)
DB_FILE = 'registrations.db'

# Initialize DB
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
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
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
        request.form.get('category') or request.form.get('otherCategory')
    )

    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            INSERT INTO registrations (title, name, gender, father, mother, dob, email, code, mobile, aadhaar, occupation, address, category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)

    return render_template('thankyou.html')

@app.route('/view')
def view():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title, name, category FROM registrations")
        entries = cursor.fetchall()
    return render_template('view.html', entries=entries)

@app.route('/download')
def download_csv():
    filename = 'registrations_export.csv'
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT title, name, category FROM registrations')
        rows = cursor.fetchall()

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Title', 'Name', 'Category'])
        writer.writerows(rows)

    return send_file(filename, as_attachment=True)

@app.route('/panchayat')
def panchayat():
    members = [
        ['श्री झूलेलाल सेवा समिति', 'श्री प्रताप राय चूग', 'अध्यक्ष', '+91 9928058058'],
        ['श्री झूलेलाल सेवा समिति', 'श्री मनोज कटारिया', 'महासचिव', '+91 9414263312'],
        ['सिंधी सेंट्रल युवा सेवा समिति', 'श्री विजय आहूजा', 'अध्यक्ष', '+91 9982134777'],
        ['सिंधी सेंट्रल युवा सेवा समिति', 'श्री मुकेश खिलवानी', 'महासचिव', '+91 9772734476']
    ]
    return render_template('panchayat.html', members=members)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
