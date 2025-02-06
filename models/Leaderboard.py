import os
from models.Score import Score


class Leaderboard:
    def __init__(self):
        self.__file_path = os.path.join('databases', 'leaderboard.txt')
        self.check_file() #kontrolli faili olemasolu ja kui pole, siis tee

    def check_file(self):
        if not os.path.exists(self.__file_path):
            self.create_leaderboard()

    def create_leaderboard(self):
        header = ['name', 'word', 'letters', 'game length', 'game time']
        with open(self.__file_path, 'a', encoding='utf-8') as f:
            f.write(';'.join(header) + '\n')

    def read_leaderboard(self):
        leaderboard = []
        with open(self.__file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines() #kõik read listi

            if not lines: #ridu ei ole failis
                return[] #tühi list

            for line in lines[1:]: #alates teisest reast
                line = line.strip() #korrastame rea
                name, word, letters, game_length, game_time = line.split(';')
                leaderboard.append(Score(name, word, letters, int(game_length), game_time))
            leaderboard = sorted(leaderboard, key=lambda x: (x.game_length, len(x.letters.split(', ')))) #sorteeri kestvuse järgi ja valede tähtede järgi

        return leaderboard

    @property
    def file_path(self):
        return self.__file_path #failinimi koos kaustaga databases/ leaderboard.txt