from flask import Flask, render_template, request, redirect, url_for, session, send_file
from pathlib import Path
from models.question_generator import extract_questions_from_pdf
from models.QpprEmbedder import QpprEmbedder
from fpdf import FPDF
import sqlite3
import os
from datetime import datetime
import secrets, random

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
global global_user_id
global global_username
global global_department
global global_priolvl
global global_digisign
global global_paper_id

global_user_id = ""
global_username = ""
global_department = ""
global_priolvl = ""
global_digisign = ""
global_paper_id = 0

def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userid TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                department TEXT NOT NULL,
                priolvl TEXT NOT NULL,
                signature_path TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS papers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                paper_id INTEGER,
                status TEXT,
                cie_number TEXT,
                dept_name TEXT,
                semester TEXT,
                course_name TEXT,
                elective_choice TEXT,
                date TEXT,
                time TEXT,
                course_code TEXT,
                max_marks TEXT,
                mandatory_count TEXT,
                q1a TEXT,
                co1a TEXT,
                lvl1a TEXT,
                marks1a TEXT,
                q1b TEXT,
                co1b TEXT,
                lvl1b TEXT,
                marks1b TEXT,
                q2a TEXT,
                co2a TEXT,
                lvl2a TEXT,
                marks2a TEXT,
                q2b TEXT,
                co2b TEXT,
                lvl2b TEXT,
                marks2b TEXT,
                q3a TEXT,
                co3a TEXT,
                lvl3a TEXT,
                marks3a TEXT,
                q3b TEXT,
                co3b TEXT,
                lvl3b TEXT,
                marks3b TEXT,
                q4a TEXT,
                co4a TEXT,
                lvl4a TEXT,
                marks4a TEXT,
                q4b TEXT,
                co4b TEXT,
                lvl4b TEXT,
                marks4b TEXT,
                FOREIGN KEY(user_id) REFERENCES users(userid)
            )
        ''')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = secrets.token_hex(5)
        username = request.form['username']
        password = request.form['password']
        department = request.form['department']
        priolvl = request.form['priority']

        # Save signature and template
        signature = request.files['signature']
        print(signature)
        signature_path = os.path.join(app.config['UPLOAD_FOLDER'], Path(signature.filename))    # should not get from UPLOAD_FOLDER
        signature.save(signature_path)

        # Store user in the database
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (userid, username, password, department, priolvl, signature_path)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, username, password, department, priolvl, signature_path))
            conn.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global global_user_id
    global global_username
    global global_department
    global global_priolvl
    global global_digisign
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user = cursor.fetchone()
            if user:
                session['user_id'] = user[0]
                global_user_id = user[1]
                global_username = user[2]
                global_department = user[4]
                global_priolvl = user[5]
                global_digisign = user[6]
                return redirect(url_for('profile'))
            else:
                return 'Invalid credentials'
    return render_template('login.html')

@app.route('/profile')
def profile():
    now = datetime.now().hour
    greeting = ""
    if now < 12:
        greeting = "Morning"
    elif 12 <= now < 18:
        greeting = "Afternoon"
    else:
        greeting = "Evening"
    
    if global_priolvl == 'PRINCIPAL':
        username_value = "Principal"
    elif global_priolvl == 'HOD':
        username_value = "Head of Department"
    else:
        username_value = "Professor"
    
    if not session['user_id']:
        return redirect(url_for('login'))
    return render_template('profile.html', username = username_value, greeting = greeting)

@app.route('/create_paper', methods=['GET', 'POST'])
def create_paper():
    if request.method == 'POST':
        question_bank = request.files['question_bank']
        question_bank_path = os.path.join(app.config['UPLOAD_FOLDER'], Path(question_bank.filename))
        question_bank.save(question_bank_path)
        
        # Extract additional information along with questions
        extracted_data = extract_questions_from_pdf(question_bank_path)
        
        # Assuming extracted_data is a dictionary with the following keys
        faculty_name = extracted_data['faculty_name']
        subject_name = extracted_data['subject_name']
        subject_code = extracted_data['subject_code']
        semester = extracted_data['semester']
        questions = extracted_data['final_8questions']
        co_list = extracted_data['final_8co_list']
        levels = extracted_data['final_8levels_list']
        
        return render_template('create_paper.html', faculty_name=faculty_name, subject_name=subject_name, subject_code=subject_code, semester=semester, questions=questions, co_list=co_list, levels=levels)
    
    return render_template('create_paper.html')

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    global global_paper_id
    if global_paper_id == 0:
        global_paper_id += random.randint(1, 10)
        print(f"\n\nnew paper id generated: {global_paper_id}\n\n")
    paper_id = global_paper_id
    print(f"\n\npaper id after assign: {paper_id}\n\n")
    user_id = global_user_id
    cie_number = request.form['cie_number']
    dept_name = request.form['dept_name']
    semester = request.form['semester']
    course_name = request.form['course_name']
    elective_choice = request.form['elective_choice']
    date = request.form['date']
    timings = request.form['timings']
    course_code = request.form['course_code']
    max_marks = request.form['max_marks']
    mandatory_count = request.form['mandatory_count']
    q1a = request.form['q1a']
    co1a = request.form['co1a']
    lvl1a = request.form['lvl1a']
    marks1a = request.form['marks1a']
    q1b = request.form['q1b']
    co1b = request.form['co1b']
    lvl1b = request.form['lvl1b']
    marks1b = request.form['marks1b']
    q2a = request.form['q2a']
    co2a = request.form['co2a']
    lvl2a = request.form['lvl2a']
    marks2a = request.form['marks2a']
    q2b = request.form['q2b']
    co2b = request.form['co2b']
    lvl2b = request.form['lvl2b']
    marks2b = request.form['marks2b']
    q3a = request.form['q3a']
    co3a = request.form['co3a']
    lvl3a = request.form['lvl3a']
    marks3a = request.form['marks3a']
    q3b = request.form['q3b']
    co3b = request.form['co3b']
    lvl3b = request.form['lvl3b']
    marks3b = request.form['marks3b']
    q4a = request.form['q4a']
    co4a = request.form['co4a']
    lvl4a = request.form['lvl4a']
    marks4a = request.form['marks4a']
    q4b = request.form['q4b']
    co4b = request.form['co4b']
    lvl4b = request.form['lvl4b']
    marks4b = request.form['marks4b']
    
    with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO papers (user_id, paper_id, cie_number, dept_name, semester, course_name, elective_choice, date, time, course_code, max_marks, mandatory_count, q1a, co1a, lvl1a, marks1a, q1b, co1b, lvl1b, marks1b, q2a, co2a, lvl2a, marks2a, q2b, co2b, lvl2b, marks2b, q3a, co3a, lvl3a, marks3a, q3b, co3b, lvl3b, marks3b, q4a, co4a, lvl4a, marks4a, q4b, co4b, lvl4b, marks4b)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, paper_id, cie_number, dept_name, semester, course_name, elective_choice, date, timings, course_code, max_marks, mandatory_count, q1a, co1a, lvl1a, marks1a, q1b, co1b, lvl1b, marks1b, q2a, co2a, lvl2a, marks2a, q2b, co2b, lvl2b, marks2b, q3a, co3a, lvl3a, marks3a, q3b, co3b, lvl3b, marks3b, q4a, co4a, lvl4a, marks4a, q4b, co4b, lvl4b, marks4b))
            conn.commit()
    
    pdf_output_path = QpprEmbedder(cie_number, dept_name, semester, course_name, elective_choice, date, timings, course_code, max_marks, mandatory_count, q1a, co1a, lvl1a, marks1a, q1b, co1b, lvl1b, marks1b, q2a, co2a, lvl2a, marks2a, q2b, co2b, lvl2b, marks2b, q3a, co3a, lvl3a, marks3a, q3b, co3b, lvl3b, marks3b, q4a, co4a, lvl4a, marks4a, q4b, co4b, lvl4b, marks4b)
    return send_file(pdf_output_path, as_attachment=True)

@app.route('/send_for_approval', methods=['POST'])
def send_for_approval():
    paper_id = global_paper_id
    print(f"\n\npaper id at send_for_approval: {paper_id}\n\n")
    status = "Pending Approval"
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE papers SET status = ? WHERE paper_id = ?
        ''', (status, paper_id))

    # Redirect to the approval page with the paper ID
    return redirect(url_for('approve_paper', paper_id=paper_id))

@app.route('/approve_paper/<int:paper_id>', methods=['GET', 'POST'])
def approve_paper(paper_id):
    global global_priolvl
    priolvl = global_priolvl
    print(f"\n\npriolvl at approve_paper: {priolvl}\n\n")
    if request.method == 'POST':
        action = request.form['action']
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            if action == 'forward_to_hod':
                cursor.execute('UPDATE papers SET status = ? WHERE paper_id = ?', ('Pending for HOD Approval', paper_id))
            elif action == 'discard':
                cursor.execute('DELETE FROM papers WHERE paper_id = ?', (paper_id,))
            elif action == 'selfsign_hod':
                cursor.execute('UPDATE papers SET status = ? WHERE paper_id = ?', ('Signed by HOD', paper_id))
            elif action == 'reject_by_hod':
                cursor.execute('UPDATE papers SET status = ? WHERE paper_id = ?', ('Rejected by HOD', paper_id))
            conn.commit()
        return redirect(url_for('profile'))
    
    return render_template('approval.html', paper_id=paper_id, global_priolvl=priolvl)

@app.route('/status')
def status():
    user_id = global_user_id
    priolvl = global_priolvl
    if priolvl == 'STAFF':
        if not user_id:
            return redirect(url_for('login'))
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM papers WHERE user_id = ?', (user_id,))
            papers = cursor.fetchall()
        return render_template('status.html', papers=papers)
    elif priolvl == 'HOD':
        if not user_id:
            return redirect(url_for('login'))
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM papers WHERE dept_name = ?', (global_department,))
            papers = cursor.fetchall()
        return render_template('status.html', papers=papers)
    else:
        if not user_id:
            return redirect(url_for('login'))
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM papers')
            papers = cursor.fetchall()
        return render_template('status.html', papers=papers)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
