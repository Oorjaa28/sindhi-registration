# app.py
from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

DATA_FILE = 'registrations.csv'

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    title = request.form.get('title')
    name = request.form.get('name').strip()
    gender = request.form.get('gender')
    father = request.form.get('father')
    mother = request.form.get('mother')
    dob = request.form.get('dob')
    email = request.form.get('email')
    code = request.form.get('code')
    mobile = request.form.get('mobile')
    aadhaar = request.form.get('aadhaar')
    occupation = request.form.get('occupation')
    address = request.form.get('address')
    category = request.form.get('category')
    other = request.form.get('otherCategory')

    category_value = other if category == 'Other' else category

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Title', 'Name', 'Gender', 'Father', 'Mother', 'DOB', 'Email', 'Code', 'Mobile', 'Aadhaar', 'Occupation', 'Address', 'Category'])

    with open(DATA_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([title, name, gender, father, mother, dob, email, code, mobile, aadhaar, occupation, address, category_value])

    return redirect(url_for('thank_you'))

@app.route('/thank-you')
def thank_you():
    return render_template('thankyou.html')

@app.route('/view')
def view():
    people = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            for row in reader:
                people.append({'fullName': f"{row[0]} {row[1]}", 'category': row[-1]})
    return render_template('view.html', people=people)

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
