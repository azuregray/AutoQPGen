# LIBRARY IMPORTS
from flask import Flask, render_template, request, redirect, url_for, session, send_file, Response, jsonify
from pathlib import Path
import sqlite3
import os
from datetime import datetime
import secrets

# LOCAL IMPORTS
from models.QScanEngine import QScanExport
from models.QpprEmbedderEngine import QpprExport
from models.DocxDownloader import docxSaver
import kickstarter

# FLASK HEADSTART
app = Flask(__name__)
app.secret_key = 'no-cookie-implementation-yet'
app.config['UPLOAD_FOLDER'] = 'static/Uploads'


# GLOBAL VARIABLES START HERE
# With the implementation of global varaibles, I'd like to clarify that this project
# was never planned for parallel sessions (multiple users using it at the same time. You can try though :) )
global global_userId
global global_userName
global global_department
global global_priorityLevel
global global_paperId
global_userId = ""
global_userName = ""
global_department = ""
global_priorityLevel = ""
global_paperId = ""


# HELPER FUNCTIONS START HERE
def database_register_user(userId, userName, password, department, priorityLevel):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (userId, userName, password, department, priorityLevel)
            VALUES (?, ?, ?, ?, ?)
        ''', (userId, userName, password, department, priorityLevel))
        conn.commit()

def database_save_paper(userId, paperId, cieNumber, departmentName, semester, courseName, electiveChoice, date, timings, courseCode, maxMarks, mandatoryCount, q1a, co1a, lvl1a, marks1a, module1a, q1b, co1b, lvl1b, marks1b, module1b, q2a, co2a, lvl2a, marks2a, module2a, q2b, co2b, lvl2b, marks2b, module2b, q3a, co3a, lvl3a, marks3a, module3a, q3b, co3b, lvl3b, marks3b, module3b, q4a, co4a, lvl4a, marks4a, module4a, q4b, co4b, lvl4b, marks4b, module4b):
    status = "Paper was created."
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO papers (userId, paperId, status, cieNumber, departmentName, semester, courseName, electiveChoice, date, timings, courseCode, maxMarks, mandatoryCount, q1a, co1a, lvl1a, marks1a, module1a, q1b, co1b, lvl1b, marks1b, module1b, q2a, co2a, lvl2a, marks2a, module2a, q2b, co2b, lvl2b, marks2b, module2b, q3a, co3a, lvl3a, marks3a, module3a, q3b, co3b, lvl3b, marks3b, module3b, q4a, co4a, lvl4a, marks4a, module4a, q4b, co4b, lvl4b, marks4b, module4b)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (userId, paperId, status, cieNumber, departmentName, semester, courseName, electiveChoice, date, timings, courseCode, maxMarks, mandatoryCount, q1a, co1a, lvl1a, marks1a, module1a, q1b, co1b, lvl1b, marks1b, module1b, q2a, co2a, lvl2a, marks2a, module2a, q2b, co2b, lvl2b, marks2b, module2b, q3a, co3a, lvl3a, marks3a, module3a, q3b, co3b, lvl3b, marks3b, module3b, q4a, co4a, lvl4a, marks4a, module4a, q4b, co4b, lvl4b, marks4b, module4b))
        conn.commit()

def database_delete_paper(paperId):
    with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM papers WHERE paperId = ?', (paperId,))
            conn.commit()
    
    eventLogger(f"Paper with PaperID {paperId} was DELETED.")

def getEventLogTime():
    return datetime.now().strftime("%B %d, %Y %I:%M:%S %p")

def eventLogger(logText):
    logBook = './LogBook.txt'
    print(f"\n\n[EVENT] [{getEventLogTime()}] {logText}\n\n")
    first_entry = not os.path.exists(logBook) or os.stat(logBook).st_size == 0
    try:
        with open(logBook, "a") as f: # "a" mode for appending
            if not first_entry:
                f.write("\n\n")
            f.write(f'[EVENT] [{getEventLogTime()}] {logText}')
            f.write("\n")
    except Exception as e:
        print(f"An error occurred while writing to logbook: {e}")

def getPaper(paperId):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM papers WHERE paperId = ?', (paperId,))
        paperData = cursor.fetchone()

    return paperData

def deletePaperRemains(paperId):
    generatedPapersFolder = './static/GeneratedPapers'
    generatedDocxFolder = './static/GeneratedDocx'
    docxFileFound = search_for_file(generatedDocxFolder, paperId, '.docx')
    pdfFileFound = search_for_file(generatedPapersFolder, paperId, '.pdf')
    if docxFileFound is not None and os.path.exists(docxFileFound):
        os.remove(docxFileFound)
    if pdfFileFound is not None and os.path.exists(pdfFileFound):
        os.remove(pdfFileFound)
    eventLogger(f'DOCX and PDF Remains of PaperID {paperId} were cleared.')

def search_for_file(directory, keyword, extension):
    found = False
    for filename in os.listdir(directory):
        if filename.endswith(extension) and keyword in filename:
            found = True
            return filename
    if not found:
        return None

def deleteQBanks():
    uploadsFolder = './static/Uploads/'
    for filename in os.listdir(uploadsFolder):
        if filename.endswith('.pdf'):
            file_path = os.path.join(uploadsFolder, filename)
            os.remove(file_path)
    eventLogger('Uploaded Question banks have been cleared.')

def get_greeting():
    hourOfDay = datetime.now().hour
    if hourOfDay < 12:
        greeting = "Morning"
    elif 12 <= hourOfDay < 18:
        greeting = "Afternoon"
    else:
        greeting = "Evening"
    
    return greeting



## APP ROUTES START HERE
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userId = secrets.token_hex(5)
        userName = request.form['username']
        password = request.form['password']
        department = request.form['department']
        priorityLevel = request.form['priority']
        database_register_user(userId, userName, password, department, priorityLevel)

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global global_userId
    global global_userName
    global global_department
    global global_priorityLevel
    if request.method == 'POST':
        userName = request.form['username']
        password = request.form['password']
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE userName = ? AND password = ?', (userName, password))
            user = cursor.fetchone()
            if user:
                session['user_id'] = global_userId = user[1]
                global_userName = user[2]
                global_department = user[4]
                global_priorityLevel = user[5]
                return redirect(url_for('profile'))
            else:
                return jsonify({'message': 'Invalid Credentials. Please perform a valid login!'})
    return render_template('login.html')

@app.route('/profile')
def profile():
    if global_priorityLevel == 'MGMT':
        username_value = "Principal"
    elif global_priorityLevel == 'HOD':
        username_value = "Head of Department"
    else:
        username_value = "Professor"

    greeting = get_greeting()

    if not session['user_id']:
        return redirect(url_for('login'))

    return render_template('profile.html', username = username_value, greeting = greeting)

@app.route('/create_paper', methods=['GET', 'POST'])
# @login_required
def create_paper():
    if request.method == 'POST':
        question_bank = request.files['question_bank']
        question_bank_path = os.path.join(app.config['UPLOAD_FOLDER'], Path(question_bank.filename))
        question_bank.save(question_bank_path)
        
        # Extract additional information along with questions
        extracted_data = QScanExport(question_bank_path)
        
        # Assuming extracted_data is a dictionary with the following keys
        facultyName = extracted_data['facultyName']
        courseName = extracted_data['courseName']
        courseCode = extracted_data['courseCode']
        semester = extracted_data['semester']
        questionsList = extracted_data['questionsList']
        coList = extracted_data['coList']
        levelsList = extracted_data['levelsList']
        modulesList = extracted_data['modulesList']
        departmentName = global_department
        
        os.remove(question_bank_path) # Remove question bank after processing.
        
        return render_template('create_paper.html', facultyName=facultyName, subjectName=courseName, subjectCode=courseCode, semester=semester, departmentName=departmentName, questions=questionsList, co_list=coList, levels=levelsList, modules=modulesList)

    return render_template('create_paper.html')

@app.route('/download_pdf_without_paperId', methods=['POST'])
def download_pdf_without_paperId():
    global global_paperId
    directory = './static/GeneratedPapers'
    foundFileName = search_for_file(directory, global_paperId, '.pdf')
    if foundFileName is not None:
        pdf_output_path = os.path.join(directory, foundFileName)
    else:
        paperData = getPaper(global_paperId)
        pdf_output_path = QpprExport(paperData)
    return send_file(pdf_output_path, as_attachment=True)

@app.route('/download_pdf_with_paperId/<paperId>', methods=['POST'])
def download_pdf_with_paperId(paperId):
    directory = './static/GeneratedPapers'
    foundFileName = search_for_file(directory, paperId, '.pdf')
    if foundFileName is not None:
        pdf_output_path = os.path.join(directory, foundFileName)
    else:
        paperData = getPaper(paperId)
        pdf_output_path = QpprExport(paperData)
    return send_file(pdf_output_path, as_attachment=True)


@app.route('/savePaper', methods=['POST'])
def savePaper():
    global global_paperId
    global_paperId = secrets.token_hex(4)
    eventLogger(f"New PaperID generated: {global_paperId}")
    paperId = global_paperId
    userId = global_userId
    cieNumber = request.form['cieNumber']
    departmentName = request.form['departmentName']
    semester = request.form['semester']
    courseName = request.form['courseName']
    electiveChoice = request.form['electiveChoice']
    date = request.form['date']
    timings = request.form['timings']
    courseCode = request.form['courseCode']
    maxMarks = request.form['maxMarks']
    mandatoryCount = request.form['mandatoryCount']
    q1a = request.form['q1a']
    co1a = request.form['co1a']
    lvl1a = request.form['lvl1a']
    marks1a = request.form['marks1a']
    module1a = request.form['module1a']
    q1b = request.form['q1b']
    co1b = request.form['co1b']
    lvl1b = request.form['lvl1b']
    marks1b = request.form['marks1b']
    module1b = request.form['module1b']
    q2a = request.form['q2a']
    co2a = request.form['co2a']
    lvl2a = request.form['lvl2a']
    marks2a = request.form['marks2a']
    module2a = request.form['module2a']
    q2b = request.form['q2b']
    co2b = request.form['co2b']
    lvl2b = request.form['lvl2b']
    marks2b = request.form['marks2b']
    module2b = request.form['module2b']
    q3a = request.form['q3a']
    co3a = request.form['co3a']
    lvl3a = request.form['lvl3a']
    marks3a = request.form['marks3a']
    module3a = request.form['module3a']
    q3b = request.form['q3b']
    co3b = request.form['co3b']
    lvl3b = request.form['lvl3b']
    marks3b = request.form['marks3b']
    module3b = request.form['module3b']
    q4a = request.form['q4a']
    co4a = request.form['co4a']
    lvl4a = request.form['lvl4a']
    marks4a = request.form['marks4a']
    module4a = request.form['module4a']
    q4b = request.form['q4b']
    co4b = request.form['co4b']
    lvl4b = request.form['lvl4b']
    marks4b = request.form['marks4b']
    module4b = request.form['module4b']
    
    database_save_paper(userId, paperId, cieNumber, departmentName, semester, courseName, electiveChoice, date, timings, courseCode, maxMarks, mandatoryCount, q1a, co1a, lvl1a, marks1a, module1a, q1b, co1b, lvl1b, marks1b, module1b, q2a, co2a, lvl2a, marks2a, module2a, q2b, co2b, lvl2b, marks2b, module2b, q3a, co3a, lvl3a, marks3a, module3a, q3b, co3b, lvl3b, marks3b, module3b, q4a, co4a, lvl4a, marks4a, module4a, q4b, co4b, lvl4b, marks4b, module4b)
    deleteQBanks()
    return jsonify({'message': f'{courseCode} Paper with paperID {global_paperId} has been saved!'})
    # return ""

@app.route('/send_for_approval', methods=['POST'])
def send_for_approval():
    paperId = global_paperId
    eventLogger(f"PaperID {paperId} has been created and sent for HOD Approval.")
    status = "Forwarded for HOD Approval."
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE papers SET status = ? WHERE paperId = ?
        ''', (status, paperId))

    return redirect(url_for('profile'))

@app.route('/paper_status_approved/<paperId>', methods=['POST'])
def paper_status_approved(paperId):
    eventLogger(f"Question paper of PaperID {paperId} was APPROVED.")
    status = "Paper Approved ✅"
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE papers SET status = ? WHERE paperId = ?
        ''', (status, paperId))
    
    return redirect(url_for('status'))

@app.route('/paper_status_rejected/<paperId>', methods=['POST'])
def paper_status_rejected(paperId):
    eventLogger(f"Question paper of PaperID {paperId} was REJECTED.")
    status = "Paper Rejected ⛔"
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE papers SET status = ? WHERE paperId = ?
        ''', (status, paperId))

    return redirect(url_for('status'))

@app.route('/status')
# @login_required
def status():
    userId = global_userId
    priorityLevel = global_priorityLevel
    if priorityLevel == 'STAFF':
        if not userId:
            return redirect(url_for('login'))
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM papers WHERE userId = ?', (userId,))
            papers = cursor.fetchall()
        return render_template('status.html', papers=papers, priolvl=priorityLevel)
    elif priorityLevel == 'HOD':
        if not userId:
            return redirect(url_for('login'))
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM papers WHERE departmentName = ?', (global_department,))
            papers = cursor.fetchall()
        return render_template('status.html', papers=papers, priolvl=priorityLevel)
    else:
        if not userId:
            return redirect(url_for('login'))
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM papers')
            papers = cursor.fetchall()
        return render_template('status.html', papers=papers, priolvl=priorityLevel)

@app.route('/docxDownload', methods=['POST'])
def docxDownload():
    paperId = global_paperId
    directory = './static/GeneratedDocx/'
    foundFileName = search_for_file(directory, paperId, '.docx')
    if foundFileName is not None:
        docxOutputPath = os.path.join(directory, foundFileName)
    else:
        paperData = getPaper(paperId)
        docxOutputPath = docxSaver(paperData)
    return send_file(docxOutputPath, as_attachment=True)

@app.route('/discardPaper', methods=['POST'])
def discardPaper():
    paperId = global_paperId
    database_delete_paper(paperId)
    deletePaperRemains(paperId)
    return redirect(url_for('profile'))

@app.route('/deletePaper_with_paperID/<paperId>', methods=['POST'])
def deletePaper_with_paperID(paperId):
    usePaperId = paperId
    database_delete_paper(usePaperId)
    deletePaperRemains(usePaperId)
    return jsonify({'message': f'Paper {usePaperId} and all its remains have been deleted.'})

@app.route('/logout')
def logout():
    return redirect(url_for('index'))



# ACTUAL EXECUTION STARTS HERE
if __name__ == '__main__':
    kickstarter.init_db() # Works only when the session is never previously run (when the database does not exist) (DOES NOT INITIALIZE THE DATABASE!!)
    kickstarter.init_dirs() # Clears all the materials uploaded or created during previous session operations.
    kickstarter.init_logBook() # Clears ./LogBook.txt to clear all Logs.
    # kickstarter.init_pycache()
    
    # To run the app server on specified IPv4 Address and port (FOR REMOTE ACCESS):
    # app.run(host="Powershell::ipconfig::IPv4Address", port=5000, debug=True)
    app.run(debug=True) # This by default runs the app server on localhost 127.0.0.1:5000