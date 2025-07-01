from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get all form values
    title = request.form['title']
    name = request.form['name']
    gender = request.form['gender']
    father = request.form['father']
    mother = request.form['mother']
    dob = request.form['dob']
    email = request.form['email']
    code = request.form['code']
    mobile = request.form['mobile']
    aadhaar = request.form['aadhaar']
    occupation = request.form['occupation']
    address = request.form['address']
    category = request.form.get('category', '')
    other = request.form.get('other', '')
    final_category = other if category == "Other" else category

    # Save to CSV
    file_exists = os.path.isfile('registrations.csv')
    with open('registrations.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow([
                'Title', 'Name', 'Gender', 'Father', 'Mother', 'DOB', 'Email',
                'Country Code', 'Mobile', 'Aadhaar', 'Occupation', 'Address', 'Sindhi Category'
            ])
        writer.writerow([
            title, name, gender, father, mother, dob, email,
            code, mobile, aadhaar, occupation, address, final_category
        ])

    return render_template('thankyou.html')

@app.route('/view')
def view():
    entries = []
    if os.path.exists('registrations.csv'):
        with open('registrations.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                entries.append({
                    'name': f"{row['Title']} {row['Name']}",
                    'category': row['Sindhi Category']
                })
    return render_template('view.html', entries=entries)

# For Render deployment
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
