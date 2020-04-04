from tkinter import Frame, Label, N, W, S, E
from tkinter.ttk import Notebook

sty = N + W + S + E

class NewDelegate(Frame):
    def __init__(self, master, tup, modify, db, id):
        Frame.__init__(self, master)
        self.id = id
        self.db = db
        self.tup = tup
        self.modify = modify
        self.master = master
        self.f = Frame(self, style="me.TFrame")
        self.f.grid(row=0, column=0, sticky=sty)
        self.f.rowconfigure(1, weight=3)
        self.f.columnconfigure(0, weight=1)
        if modify:
            value = id
        else:
            value = "Supplier Name"
        self.name = Label(self.f, text=value, font=("Berlin Sans FB Demi", 40, foreground="#3496ff"))
        self.name.grid(row=0, column=0, sticky=sty)
        note = Notebook(self.f)
        note.grid(row=1, column=0, sticky=sty)
        note.rowconfigure(0, weight=1)
        note.columnconfigure(0, weight=1)
        self.notepage1(note, modify, tup, id)

    def notepage1(self, note, modify, tup, id):
        pass