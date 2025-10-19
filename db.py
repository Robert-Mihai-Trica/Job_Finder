import sqlite3

DB_NAME = "jobs.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        company TEXT,
                        link TEXT UNIQUE
                      )''')
    conn.commit()
    conn.close()

def insert_job(title, company, link):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO jobs (title, company, link) VALUES (?, ?, ?)", 
                       (title, company, link))
        conn.commit()
    except sqlite3.IntegrityError:
        # job deja salvat (link duplicat)
        pass
    conn.close()

def get_all_jobs():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT title, company, link FROM jobs")
    rows = cursor.fetchall()
    conn.close()
    return rows