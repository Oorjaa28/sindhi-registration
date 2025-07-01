from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import csv
import os

app = Flask(__name__)
DB_NAME = "registrations.db"

# ✅ Create database table if not exists
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                name TEXT,
                gender TEXT,
                father_name TEXT,
                mother_name TEXT,
                dob TEXT,
                email TEXT,
                country_code TEXT,
                mobile TEXT,
                aadhaar TEXT,
                occupation TEXT,
                address TEXT,
                category TEXT
            )
        ''')
        conn.commit()

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        category_selected = request.form.get('category', '')
        category_final = request.form.get('other_category') if category_selected == 'Other' else category_selected

        data = (
            request.form['title'],
            request.form['name'],
            request.form['gender'],
            request.form['father_name'],
            request.form['mother_name'],
            request.form['dob'],
            request.form['email'],
            request.form['country_code'],
            request.form['mobile'],
            request.form['aadhaar'],
            request.form['occupation'],
            request.form['address'],
            category_final
        )

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO registrations (
                    title, name, gender, father_name, mother_name, dob, email,
                    country_code, mobile, aadhaar, occupation, address, category
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', data)
            conn.commit()

        return redirect(url_for('thankyou'))

    return render_template('form.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/view')
def view():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title, name, category FROM registrations")
        people = cursor.fetchall()
    return render_template('view.html', people=people)

@app.route('/download_csv')
def download_csv():
    csv_file = "registrations.csv"
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM registrations")
        rows = cursor.fetchall()
        headers = [description[0] for description in cursor.description]

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    return send_file(csv_file, as_attachment=True)

@app.route('/panchayat')
def panchayat():
    return render_template('panchayat.html')

if __name__ == '__main__':
    print("✅ Creating database and table if not exists...")
    init_db()

    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
