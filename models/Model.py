import glob
import os
from datetime import datetime
import random
from models.Database import Database
from models.FileObject import FileObject
from models.Leaderboard import Leaderboard


class Model:
    def __init__(self, db):
        self.db = db  # Kasuta andmebaasi objekti, ära kutsu seda funktsioonina
        self.__image_files = []  # tühi list piltide jaoks
        self.load_images('images')
        self.__categories = self.db.get_all_categories()  # Kategooriad SQLite andmebaasist
        self.titles = ['Poomismäng 2025', 'Kas jäid magama?', 'Ma ootan su käiku!', 'Sisesta juba see täht', 'Zzzzzzzz']

        # Mängu muutujad (määratakse `start_new_game` sees)
        self.__new_word = None
        self.__user_word = []
        self.__counter = 0
        self.__all_user_chars = []

    def load_images(self, folder):
        if not os.path.exists(folder):
            raise FileNotFoundError(f'Kausta {folder} ei ole.')

        images = glob.glob(os.path.join(folder, '*.png'))
        if not images:
            raise FileNotFoundError(f'Kaustas {folder} ei ole PNG laiendiga faile.')

        self.__image_files = images

    def start_new_game(self, category_id, category):

        if category_id == 0:
            category = None  # Kui kategooria ID on 0, võta suvaline sõna

        word_data = self.db.get_random_word(category)  # Kasutab valitud kategooriat

        if word_data:
            self.__new_word = word_data[0]  # Võtab ainult sõna, mitte kategooriat
        else:
            raise Exception("VIGA: Ei suutnud andmebaasist juhuslikku sõna laadida!")

        self.__user_word = ["_"] * len(self.__new_word)  # Peidame tähed
        self.__counter = 0
        self.__all_user_chars = []

    def get_user_input(self, user_input):

        if user_input:
            user_char = user_input[:1]  # Esimene märk sisestusest
            if user_char.lower() in self.__new_word.lower():
                self.change_user_input(user_char)  # Kui täht on olemas
            else:
                self.__counter += 1
                self.__all_user_chars.append(user_char.upper())  # Lisa valesti sisestatud täht
        else:
            self.__counter += 1

    def change_user_input(self, user_char):
        current_word = self.char_to_list(self.__new_word)
        for i, c in enumerate(current_word):
            if c.lower() == user_char.lower():
                self.__user_word[i] = user_char.upper()

    @staticmethod
    def char_to_list(word):
        """Muutke string listiks, nt `test` → `['t', 'e', 's', 't']`."""
        return list(word)

    def get_all_user_chars(self):
        return ', '.join(self.__all_user_chars)

    def save_player_score(self, name, seconds):
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Hetke kuupäev ja kell

        if not name.strip():  # Kui nimi puudub
            name = random.choice(['Teadmata', 'Tundmatu', 'Unknown'])

        letters = self.get_all_user_chars()  # Vigased tähed

        # Salvesta tulemus andmebaasi
        self.db.add_score(name, self.__new_word, letters, seconds)

        print(f"Skoor salvestatud: {name} - {self.__new_word} - {letters} - {seconds} sek - {today}")

    # Getters
    @property
    def image_files(self):
        """Tagastab piltide listi."""
        return self.__image_files

    @property
    def categories(self):
        """Tagastab kategooriate listi."""
        return self.__categories

    @property
    def user_word(self):
        """Tagastab kasutaja leitud tähed, need mis on õiged."""
        return self.__user_word

    @property
    def counter(self):
        """Tagastab vigade arvu."""
        return self.__counter
