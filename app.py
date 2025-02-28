import sys
from tkinter import Tk, messagebox

from controllers.Controller import Controller
from models.Database import Database
from models.Model import Model
from views.View import View

def show_popup_error(message):
    root = Tk()
    root.withdraw() #peidab loodava akna
    messagebox.showerror(title="Viga", message=f'{message}')
    root.destroy()

if __name__ == '__main__':
    try:
        db = Database()
        model = Model(db) #loo mudel
        view = View(model) #loo view andes kaasa model
        Controller(model, view) #loo controller
        view.mainloop() #viimane rida koodis
    except ValueError as error:
        #print(f'Viga: {error}')
        View.show_message(error)
        sys.exit(1) #koos lõpetab töö
    except Exception as error:
        #print(f'Tekkis ootamatu viga: {error}')
        View.show_message(error)
        sys.exit(1)