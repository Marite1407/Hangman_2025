import os
import sqlite3
from datetime import datetime

class Database:
    def __init__(self):

        self.db_path = "databases/hangman_2025.db"
        self.connect()
        self.create_tables()
        self.check_database()

    def connect(self):

        if not os.path.exists("databases"):
            os.makedirs("databases")

        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def create_tables(self):

        print("Kontrollime ja loome tabelid, kui neid pole...")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            category TEXT NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            word TEXT NOT NULL,
            letters TEXT,
            game_length INTEGER NOT NULL,
            game_time TEXT NOT NULL
        )
        """)

        self.connection.commit()
        print("Tabelid loodud või eksisteerivad juba!")

    def check_database(self):

        self.cursor.execute("SELECT COUNT(*) FROM words")
        word_count = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM leaderboard")
        score_count = self.cursor.fetchone()[0]

        if word_count == 0:
            print("Impordime sõnad failist, kuna tabel on tühi.")
            self.import_words_from_file()

        if score_count == 0:
            print("Impordime edetabeli failist, kuna tabel on tühi.")
            self.import_leaderboard_from_file()

    def import_words_from_file(self):

        words_file_path = "databases/words.txt"
        try:
            with open(words_file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()[1:]  # Jätame esimese rea vahele (päis)
                words_data = []
                for line in lines:
                    parts = line.strip().split(";")
                    if len(parts) == 2:
                        word, category = parts
                        words_data.append((word, category))
                if words_data:
                    self.cursor.executemany("INSERT INTO words (word, category) VALUES (?, ?)", words_data)
                    self.connection.commit()
                    print(f"Lisatud {len(words_data)} sõna `words` tabelisse!")
                    # Pärast edukat importi kustutame faili
                    os.remove(words_file_path)
                    print("`words.txt` eemaldati, kuna seda enam ei vajata.")
        except FileNotFoundError:
            print("Faili 'words.txt' ei leitud – impordi funktsioon jäi vahele.")

    def import_leaderboard_from_file(self):
        leaderboard_file_path = "databases/leaderboard.txt"
        try:
            with open(leaderboard_file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()[1:]
                leaderboard_data = []
                for line in lines:
                    parts = line.strip().split(";")
                    if len(parts) == 5:
                        name, word, letters, game_length, game_time = parts
                        leaderboard_data.append((name, word, letters, int(game_length), game_time))
                if leaderboard_data:
                    self.cursor.executemany(
                        "INSERT INTO leaderboard (name, word, letters, game_length, game_time) VALUES (?, ?, ?, ?, ?)",
                        leaderboard_data)
                    self.connection.commit()
                    print(f"Lisatud {len(leaderboard_data)} mängijat `leaderboard` tabelisse!")
                    # Pärast edukat importi kustutame faili
                    os.remove(leaderboard_file_path)
                    print("`leaderboard.txt` eemaldati, kuna seda enam ei vajata.")
        except FileNotFoundError:
            print("Faili 'leaderboard.txt' ei leitud – impordi funktsioon jäi vahele.")

    def get_all_categories(self):
        self.cursor.execute("SELECT DISTINCT category FROM words")
        return [row[0] for row in self.cursor.fetchall()]

    def get_random_word(self, category=None):
        if category:
            self.cursor.execute("SELECT word, category FROM words WHERE category = ? ORDER BY RANDOM() LIMIT 1",
                                (category,))
        else:
            self.cursor.execute("SELECT word, category FROM words ORDER BY RANDOM() LIMIT 1")
        result = self.cursor.fetchone()
        return result if result else (None, None)

    def get_leaderboard(self):
        self.cursor.execute("SELECT name, word, letters, game_length, game_time FROM leaderboard ORDER BY game_length ASC")
        return self.cursor.fetchall()

    def add_score(self, name, word, letters, game_length):
        game_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute(
            "INSERT INTO leaderboard (name, word, letters, game_length, game_time) VALUES (?, ?, ?, ?, ?)",
            (name, word, letters, game_length, game_time)
        )
        self.connection.commit()

    def close(self):
        self.connection.close()

if __name__ == "__main__":
    try:
        db = Database()
        print("Andmebaas ühendatud ja tabelid loodud!")
        categories = db.get_all_categories()
        print("Kategooriad:", categories)
        word = db.get_random_word()
        print("Juhuslik sõna:", word)
        leaderboard = db.get_leaderboard()
        print("Edetabel:", leaderboard)
    except Exception as e:
        print(f"Viga {e}")
