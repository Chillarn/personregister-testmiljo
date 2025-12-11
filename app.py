import sqlite3
import os

def init_database():
    db_path = os.getenv('DATABASE_PATH', 'test_users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
    ''')
 
    cursor.execute('SELECT COUNT(*) FROM users')
    count = cursor.fetchone()[0]
 
    if count == 0:
        test_users = [
            ('Hugo Svensson', 'hugo@exempel.se'),
            ('Jim Karlsson', 'jim@exempel.se')
        ]
        cursor.executemany('INSERT INTO users (name, email) VALUES (?, ?)', test_users)
        print("Databas klar med testpersoner")
    else:
        print(f"Databasen har redan {count} personer")
 
    conn.commit()
    conn.close()
 
def display_users():
    db_path = os.getenv('DATABASE_PATH', 'test_users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
 
    print("\nPersoner i databasen:")
    for user in users:
        print(f"ID: {user[0]}, Namn: {user[1]}, E-post: {user[2]}")
 
    conn.close()
 
def clear_test_data():
    db_path = os.getenv('DATABASE_PATH', 'test_users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users')
    conn.commit()
    conn.close()
    print("All data är borttagen (GDPR följs)")
 
def anonymize_data():
    db_path = os.getenv('DATABASE_PATH', 'test_users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
 
    cursor.execute('SELECT id FROM users')
    users = cursor.fetchall()
 
    for user in users:
        user_id = user[0]
        anonym_email = f"anonym_{user_id}@anonym.se"
 
        cursor.execute(
            "UPDATE users SET name = ?, email = ? WHERE id = ?",
            ("Anonym Användare", anonym_email, user_id)
        )
 
    conn.commit()
    conn.close()
    print("Alla namn och e-postadresser har anonymiserats (GDPR följs)")
 
if __name__ == "__main__":
    init_database()
    display_users()
    print("\nContainern är igång. Tryck Ctrl+C för att stoppa.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nAvslutar...")
