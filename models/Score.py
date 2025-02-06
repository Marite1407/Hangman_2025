class Score:

    def __init__(self, name, word, letters, game_length, game_time):
        self.name = name
        self.word = word
        self.letters = letters
        self.game_length = game_length
        self.game_time = game_time

    def __str__(self):
        return f'{self.name} {self.word} {self.letters} {self.game_length} {self.game_time}'
