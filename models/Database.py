import os
import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        """Ühendub SQLite andmebaasiga ja kontrollib, kas vajalikud tabelid on olemas."""
        self.db_path = "databases/hangman_2025.db"
        self.connect()
        self.create_tables()
        self.check_database()
        self.import_words_from_file()
        self.import_leaderboard_from_file()

    def connect(self):
        """Ühendub SQLite andmebaasiga või loob faili, kui see puudub."""
        if not os.path.exists("databases"):
            os.makedirs("databases")

        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        """Loob vajalikud tabelid, kui need ei ole olemas."""
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
        """Kontrollib, kas vajalikud tabelid on olemas ja kas words tabelis on andmeid."""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in self.cursor.fetchall()}

        if "words" not in tables or "leaderboard" not in tables:
            raise Exception("VIGA: Andmebaas on olemas, aga vajalikud tabelid puuduvad! Rakendus ei saa käivituda.")

        self.cursor.execute("SELECT COUNT(*) FROM words")
        count = self.cursor.fetchone()[0]

        if count == 0:
            raise Exception("VIGA: Tabel 'words' on tühi. Vähemalt üks sõna kategooriaga peab olema!")

    def import_words_from_file(self):
        """Impordib words.txt sisu andmebaasi, kui words tabel on tühi."""
        words_file_path = "databases/words.txt"

        self.cursor.execute("SELECT COUNT(*) FROM words")
        count = self.cursor.fetchone()[0]

        if count == 0 and os.path.exists(words_file_path):
            with open(words_file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()[1:]  # Jätame esimese rea (päise) vahele

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

    def import_words_from_file(self):
        """Impordib words.txt sisu andmebaasi, kui words tabel on tühi."""
        words_file_path = "databases/words.txt"

        # Kontrollime, kas words tabel on tühi
        self.cursor.execute("SELECT COUNT(*) FROM words")
        count = self.cursor.fetchone()[0]

        if count == 0:  # Ainult kui words tabel on tühi, impordime
            if os.path.exists(words_file_path):
                print(f"Leiti fail: {words_file_path}")  # Lisa see kontroll

                with open(words_file_path, "r", encoding="utf-8") as file:
                    lines = file.readlines()[1:]  # Jätame esimese rea vahele (päis)

                    words_data = []
                    for line in lines:
                        parts = line.strip().split(";")
                        if len(parts) == 2:
                            word, category = parts
                            words_data.append((word, category))

                    if words_data:
                        print(f"⚡ SQL lisamine: {words_data}")  # Lisa logi, et näha andmeid
                        self.cursor.executemany("INSERT INTO words (word, category) VALUES (?, ?)", words_data)
                        self.connection.commit()
                        print(f"Lisatud {len(words_data)} sõna `words` tabelisse!")
                    else:
                        print("⚠ `words.txt` fail on tühi või vales formaadis!")

            else:
                print(f"`words.txt` faili ei leitud kaustas {words_file_path}!")

    def import_leaderboard_from_file(self):
        """Impordib `leaderboard.txt` andmebaasi, kui leaderboard tabel on tühi."""
        leaderboard_file_path = "databases/leaderboard.txt"

        # Kontrollime, kas `leaderboard` tabel on tühi
        self.cursor.execute("SELECT COUNT(*) FROM leaderboard")
        count = self.cursor.fetchone()[0]

        if count == 0 and os.path.exists(leaderboard_file_path):
            with open(leaderboard_file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()[1:]  # Jätame päise vahele

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
                else:
                    print("⚠ `leaderboard.txt` fail on tühi või vales formaadis!")
        else:
            print("`leaderboard` tabelis on juba andmed, ei impordi uuesti.")

    def get_all_categories(self):
        """Tagastab kõik unikaalsed kategooriad words tabelist."""
        self.cursor.execute("SELECT DISTINCT category FROM words")
        return [row[0] for row in self.cursor.fetchall()]

    def get_random_word(self, category=None):
        """Tagastab juhusliku sõna kindlast kategooriast."""
        if category:
            self.cursor.execute("SELECT word, category FROM words WHERE category = ? ORDER BY RANDOM() LIMIT 1",
                                (category,))
        else:
            self.cursor.execute("SELECT word, category FROM words ORDER BY RANDOM() LIMIT 1")

        result = self.cursor.fetchone()
        return result if result else (None, None)  # Tagame, et alati tagastatakse kaks väärtust

    def get_leaderboard(self):
        """Tagastab edetabeli sisu."""
        self.cursor.execute("SELECT name, word, letters, game_length, game_time FROM leaderboard ORDER BY game_length ASC")
        return self.cursor.fetchall()

    def add_score(self, name, word, letters, game_length):
        """Lisab uue mängija tulemuse edetabelisse."""
        game_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.cursor.execute(
            "INSERT INTO leaderboard (name, word, letters, game_length, game_time) VALUES (?, ?, ?, ?, ?)",
            (name, word, letters, game_length, game_time)
        )
        self.connection.commit()

    def close(self):
        """Sulgeb andmebaasiühenduse."""
        self.connection.close()

# Testimiseks
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
        print(f"❌ {e}")
