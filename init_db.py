import sqlite3, os, shutil

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
        conn.commit()


def init_dirs():
    generated_papers_dir = 'D:/Darshan/Documents/AutoQPGen/Phase03/static/GeneratedPapers'
    uploaded_docs_dir = 'D:/Darshan/Documents/AutoQPGen/Phase03/static/uploads'
    shutil.rmtree(generated_papers_dir)
    os.mkdir(generated_papers_dir)
    shutil.rmtree(uploaded_docs_dir)
    os.mkdir(uploaded_docs_dir)
    
if __name__ == '__main__':
    init_dirs()
    init_db()
