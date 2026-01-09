import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Ensure we have a static folder for CSS/JS
app.static_folder = 'static'

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def init_db():
    conn = sqlite3.connect('capsules.db')
    c = conn.cursor()
    # Note: open_date will now store ISO format 'YYYY-MM-DDTHH:MM'
    c.execute('''
        CREATE TABLE IF NOT EXISTS capsules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient_email TEXT NOT NULL,
            message TEXT NOT NULL,
            filename TEXT,
            open_date TEXT NOT NULL,
            status TEXT DEFAULT 'locked'
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    # In a real app, check credentials here
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('capsule.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/forgot_password')
def forgot_password():
    # Matches the actual filename
    return render_template('ForgetPassword.html')

@app.route('/submit_time_capsule', methods=['POST'])
def submit_capsule():
    recipient = request.form['recipient_email']
    message = request.form['capsule_message']
    date = request.form['open_date']
    
    filename = None
    if 'capsule_file' in request.files:
        file = request.files['capsule_file']
        if file.filename != '':
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    conn = sqlite3.connect('capsules.db')
    c = conn.cursor()
    c.execute("INSERT INTO capsules (recipient_email, message, filename, open_date) VALUES (?, ?, ?, ?)",
              (recipient, message, filename, date))
    conn.commit()
    conn.close()

    return "<h1>Capsule Secured. Timer Initiated.</h1><br><a href='/dashboard'>Back</a>"

if __name__ == '__main__':
    app.run(debug=True)