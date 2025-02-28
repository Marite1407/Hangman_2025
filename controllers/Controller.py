import random
from tkinter import DISABLED, NORMAL, simpledialog, messagebox
from models.Leaderboard import Leaderboard
from models.Stopwatch import Stopwatch
from models.Timer import Timer


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.stopwatch = Stopwatch(self.view.lbl_time)

        #ajasti loomine TODO Sellega on mingi jama
        self.timer = Timer(scheduled_callback=self.view.after,
                           cancel_callback=self.view.after_cancel,
                           interval=5000, #5 sek
                           callback=self.change_title,)

        #nuppude callback seaded
        self.btn_new_callback()
        self.btn_cancel_callback()
        self.btn_send_callback()
        self.view.set_timer_reset_callback(self.reset_timer)
        self.btn_scoreboard_callback()

        #enter klahvi funktsionaalsus
        self.view.bind('<Return>', lambda b: self.btn_send_click())

    def buttons_for_game(self): #nupud mängu jaoks
        self.view.btn_new['state'] = DISABLED #uue mängu nuppu uuesti vajutada ei saa kui mäng käib
        self.view.btn_send['state'] = NORMAL
        self.view.btn_cancel['state'] = NORMAL
        self.view.char_input['state'] = NORMAL
        self.view.char_input.focus()
        self.view.cmb_category['state'] = DISABLED

    def buttons_for_not_game(self):
        self.view.btn_new['state'] = NORMAL
        self.view.btn_send['state'] = DISABLED
        self.view.btn_cancel['state'] = DISABLED
        self.view.char_input.delete(0, 'end') #tühjenda sisestuskast
        self.view.char_input['state'] = DISABLED
        self.view.cmb_category['state'] = NORMAL

    def btn_new_callback(self):
        self.view.set_btn_new_callback(self.btn_new_click) #meetod ilma sulgudeta

    def btn_cancel_callback(self):
        self.view.set_btn_cancel_callback(self.btn_cancel_click)

    def btn_send_callback(self):
        self.view.set_btn_send_callback(self.btn_send_click)

    def btn_scoreboard_callback(self):
        self.view.set_btn_scoreboard_callback(self.btn_scoreboard_click)

    def btn_new_click(self):
        self.buttons_for_game()
        #seadistab juhusliku sõna kategooria järgi ja asendab tähed
        self.model.start_new_game(self.view.cmb_category.current(), self.view.cmb_category.get()) #id, sõna
        #näita "sõna" kasutajale
        self.view.lbl_result.config(text=self.model.user_word)
        #vigaste tähtede resettimine
        self.view.lbl_error.config(text='Vigased tähed', fg='black')
        #muuda pilti
        self.view.change_image(self.model.counter) #või 0 sulgudesse
        self.timer.start() #käivita title juhuslikkus (5 sek)
        self.stopwatch.reset() #eelmine mäng
        self.stopwatch.start() #käivita aeg

    def btn_cancel_click(self):
        self.buttons_for_not_game()
        self.stopwatch.stop()
        self.timer.stop() #peata title juhuslikkus (5 sek)
        self.view.lbl_result.config(text=self.model.user_word)
        self.view.title(self.model.titles[0])  # esimene element title listist

    def btn_send_click(self):
        self.model.get_user_input(self.view.char_input.get().strip()) #saada sisestus
        self.view.lbl_result.config(text=self.model.user_word) #uuenda tulemust
        self.view.lbl_error.config(text=f'Vigased tähed: {self.model.get_all_user_chars()}')
        self.view.char_input.delete(0, 'end') #tühjenda sisestuskast
        if self.model.counter > 0:
            self.view.lbl_error.config(fg='red') #muuda vigane tekst punaseks
            self.view.change_image(self.model.counter) #muuda pilti
        self.is_game_over()

    def btn_scoreboard_click(self):
        lb = Leaderboard()
        data = lb.read_leaderboard()
        popup_window = self.view.create_popup_window()
        self.view.generate_scoreboard(popup_window, data)

    def is_game_over(self):
        if self.model.counter >= 11 or '_' not in self.model.user_word:
            self.stopwatch.stop() #peata stopper
            self.buttons_for_not_game() #nupu majandus
            player_name = simpledialog.askstring('Mäng on läbi', 'Kuidas on mängija nimi? ', parent=self.view)
            messagebox.showinfo('Teade', 'Oled lisatud edetabelisse')
            self.model.save_player_score(player_name, self.stopwatch.seconds)
            self.view.title(self.model.titles[0]) #esimene element title listist

    def change_title(self):
        new_title = random.choice(self.model.titles)
        self.view.title(new_title)

    def reset_timer(self):
        self.timer.start()