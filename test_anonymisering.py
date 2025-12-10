import os
import sqlite3
import tempfile
import app   # Importerar din app.py

def test_anonymisering():
    # Skapa en temporär databasfil
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        os.environ["DATABASE_PATH"] = db_path

        # Initiera databasen med testpersoner
        app.init_database()

        # Kör anonymisering
        app.anonymize_data()

        # Läs resultatet
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM users")
        users = cursor.fetchall()
        conn.close()

        # Kontrollera varje användare
        for user_id, name, email in users:
            assert name == "Anonym Användare", "Namnet är inte anonymiserat!"
            assert email == f"anonym_{user_id}@anonym.se", "E-post är inte anonymiserad!"
