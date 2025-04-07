import sqlite3
from models.Score import Score


class Leaderboard:
    def __init__(self):
        self.__db_path = "databases/hangman_2025.db"

    def read_leaderboard(self):
        leaderboard = []
        try:
            connection = sqlite3.connect(self.__db_path)
            cursor = connection.cursor()
            cursor.execute(
                "SELECT name, word, letters, game_length, game_time FROM leaderboard ORDER BY game_length ASC")
            rows = cursor.fetchall()
            connection.close()

            for row in rows:
                name, word, letters, game_length, game_time = row
                leaderboard.append(Score(name, word, letters, game_length, game_time))

            # Sorteeri: esmalt kestuse, siis valede tähtede arvu järgi
            leaderboard = sorted(leaderboard,
                                 key=lambda x: (x.game_length, len(x.letters.split(', ')) if x.letters else 0))

        except sqlite3.Error as e:
            print(f"Viga andmebaasist lugemisel: {e}")

        return leaderboard
