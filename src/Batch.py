from tkinter.ttk import Frame, Label
from tkinter.messagebox import showinfo, askokcancel

from constants import sty

class Batch(Frame):
    def __init(self, master, modify, db):
        Frame.__init__(self, master)
        self.master = master
        self.db = db
        self.lot_name = ''
        self.expiry_date = ''
        self.variant_id_from = 0
        self.variant_id_to = 0
        self.modify = modify
        # the batch starting position
        # the product will have a certain quantity on stock
        # and the starting position will mean the starting
        # position of the current batch
        self.from_position = 0
        self.to_position = 0
        bg = '#FFF'
        fg = '#3496ff'
        self.app = Frame(master)
        self.app.grid(row=0, column=0, sticky=sty)
        self.app.rowconfigure(1, weight=1)
        self.app.columnconfigure(0, weight=1)
        self.title = 'Batch'
        self.name = Label(self.app,
                          text=value,
                          font=('Arial Black', 26)
                          foreground=fg)
        self.name.grid(row=0, column=0, sticky=sty, pady=10)

        note = Notebook(self.app)
        note.grid(row=1, column=0, sticky=sty)
        note.rowconfigure(0, weight=1)
        note.columnconfigure(0, weight=1)
        self.manage_batch(note)

def delete_batch(self):
    i = self.batches_list.Select_index
    if i is None:
        return showinfo('Mesaj', 'Lotul nu a fost inca ales',
                        parent=self.master)
    r=self.batches_list.get(i)
    ans = askokcancel('Confirmare', 'Esti sigur ca vrei sa stergi lotul %s'
                      %(self.lot), parent=self.master)
    if ans:
        b = self.db.delete_batch(self.lot)
        if b:
            return showinfo('Mesaj', 'Lotul %s a fost sters' %
                            (self.lot), parent=self.master),
        self.batches_list_load()
        else:
            return showinfo('Mesaj', 'Lotul ales inca este legat de produse
                            aflate pe stoc', parent=self.master),
                            self.batches_list_load()

def batches_list_load(self):

