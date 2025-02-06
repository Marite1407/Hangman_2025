import time


class Stopwatch:
    def __init__(self, lbl_time):
        self.__lbl_time = lbl_time
        self.__seconds = 0 #aeg sekundites
        self.__running = False #aeg käib/seisab

    def start(self):
        self.__running = True
        self.update()

    def update(self):
        if self.__running:
            if self.__seconds == 0:
                display = '00:00:00'
            else:
                #https: // www.studytonight.com / python - howtos / how - to - convert - seconds - to - hours - minutes - and -seconds - in -python
                display = time.strftime('%H:%M:%S', time.gmtime(self.__seconds))

            self.__lbl_time['text'] = display #muuda aeg labelil
            self.__lbl_time.after(1000, self.update) #oota sekund ja kutsu ennast uuesti välja
            self.__seconds += 1 #suurenda sekundeid ühe võrra

    def stop(self):
        """peata stopper"""
        self.__running = False

    def reset(self):
        self.__seconds = 0
        self.__lbl_time['text'] = '00:00:00'

    @property
    def seconds(self):
        """tagasta mänguaja sekundid"""
        return self.__seconds