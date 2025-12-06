import sqlite3

def init_db():
    conn = sqlite3.connect("student_db.db")
    cursor = conn.cursor()

    cursor.execute(    
    """
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        assigned_team INT
    )
    """
    )

    conn.commit()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        available_slots INTEGER NOT NULL   )          
    """)
    conn.commit()

    conn.execute("insert into teams (available_slots) values (4)")
    conn.execute("insert into teams (available_slots) values (4)")
    conn.execute("insert into teams (available_slots) values (4)")
    conn.commit()
  

init_db()


