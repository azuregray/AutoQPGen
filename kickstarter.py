import sqlite3, os, shutil

def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userId TEXT UNIQUE NOT NULL,
                userName TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                department TEXT NOT NULL,
                priorityLevel TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS papers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userId INTEGER,
                paperId INTEGER,
                status TEXT,
                cieNumber TEXT,
                departmentName TEXT,
                semester TEXT,
                courseName TEXT,
                electiveChoice TEXT,
                date TEXT,
                timings TEXT,
                courseCode TEXT,
                maxMarks TEXT,
                mandatoryCount TEXT,
                q1a TEXT,
                co1a TEXT,
                lvl1a TEXT,
                marks1a TEXT,
                module1a TEXT,
                q1b TEXT,
                co1b TEXT,
                lvl1b TEXT,
                marks1b TEXT,
                module1b TEXT,
                q2a TEXT,
                co2a TEXT,
                lvl2a TEXT,
                marks2a TEXT,
                module2a TEXT,
                q2b TEXT,
                co2b TEXT,
                lvl2b TEXT,
                marks2b TEXT,
                module2b TEXT,
                q3a TEXT,
                co3a TEXT,
                lvl3a TEXT,
                marks3a TEXT,
                module3a TEXT,
                q3b TEXT,
                co3b TEXT,
                lvl3b TEXT,
                marks3b TEXT,
                module3b TEXT,
                q4a TEXT,
                co4a TEXT,
                lvl4a TEXT,
                marks4a TEXT,
                module4a TEXT,
                q4b TEXT,
                co4b TEXT,
                lvl4b TEXT,
                marks4b TEXT,
                module4b TEXT,
                FOREIGN KEY(userId) REFERENCES users(userId)
            )
        ''')
        conn.commit()


def init_dirs():
    generatedPapersFolder = './static/GeneratedPapers'
    uploadsFolder = './static/Uploads'
    generatedDocxFolder = './static/GeneratedDocx'
    
    if os.path.isdir(generatedPapersFolder):
        shutil.rmtree(generatedPapersFolder)
        os.mkdir(generatedPapersFolder)
    else:
        os.mkdir(generatedPapersFolder)
    
    if os.path.isdir(generatedDocxFolder):
        shutil.rmtree(generatedDocxFolder)
        os.mkdir(generatedDocxFolder)
    else:
        os.mkdir(generatedDocxFolder)
    
    if os.path.isdir(uploadsFolder):
        shutil.rmtree(uploadsFolder)
        os.mkdir(uploadsFolder)
    else:
        os.mkdir(uploadsFolder)


def init_logBook():
    logFilePath = 'LogBook.txt'
    if os.path.isfile(logFilePath):
        os.remove(logFilePath)
    logFileObject = open("LogBook.txt", "xt")
    logFileObject.close()

def init_pycache():
    pycache_app = './__pycache__'
    pycache_models = './models/__pycache__'
    if os.path.exists(pycache_app):
        shutil.rmtree(pycache_app)
    if os.path.exists(pycache_models):
        shutil.rmtree(pycache_models)

def readyApp():
    init_dirs()
    init_db()
    init_logBook()
    init_pycache()

def offloadApp():
    generatedPapersFolder = './static/GeneratedPapers'
    uploadsFolder = './static/Uploads'
    generatedDocxFolder = './static/GeneratedDocx'
    
    if os.path.isdir(generatedPapersFolder):
        shutil.rmtree(generatedPapersFolder)
    
    if os.path.isdir(generatedDocxFolder):
        shutil.rmtree(generatedDocxFolder)
    
    if os.path.isdir(uploadsFolder):
        shutil.rmtree(uploadsFolder)
    
    if os.path.isfile('database.db'):
        os.remove('database.db')
    
    if os.path.isfile('LogBook.txt'):
        os.remove('LogBook.txt')
    
    init_pycache()


if __name__ == '__main__':
    init_dirs()
    init_db()
    init_logBook()
