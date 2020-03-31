from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.ttk import *

from Src.Cython.proWrd1 import Filter

sty = N + W + S + E


class NewSupplier(Frame):
    def __init__(self, master, tup, modify, db, id):
        print('si aici')
        Frame.__init__(self, master)
        self.id = id
        self.db = db
        self.tup = tup
        self.modify = modify
        bg = 'White'
        fg = "#3496ff"
        self.master = master
        self.f = Frame(self, style='me.TFrame')
        self.f.grid(row=0, column=0, sticky=sty)
        self.f.rowconfigure(1, weight=3)
        self.f.columnconfigure(0, weight=1)
        if modify:
            value = id
        else:
            value = "Supplier Name"
        self.name = Label(self.f, text=value, font=('Berlin Sans FB Demi', 40), foreground=fg)
        self.name.grid(row=0, column=0, sticky=sty)
        note = Notebook(self.f)
        note.grid(row=1, column=0, sticky=sty)
        note.rowconfigure(0, weight=1)
        note.columnconfigure(0, weight=1)
        self.notepage1(note, modify, tup, id)
        if modify:
            self.notepage15(note)
            self.notepage2(note)
            self.notepage3(note)

    def notepage15(self, note):
        pass

    def notepage2(self, note):
        pass

    def notepage3(self, note):
        pass

    def notepage1(self, note, modify, tup, id):
        app = Frame(note)
        app.grid(row=0, column=0)
        self.f.rowconfigure(0, weight=1)
        self.f.columnconfigure(0, weight=1)
        note.add(app, text='Detail')
        Label(app, text='Supplier Detail', font=('Berlin Sans FB Demi', 23), foreground="#3496ff").grid(row=0, column=0,
                                                                                                       columnspan=2,
                                                                                                       sticky=sty)

        Label(app, text='Supplier Name').grid(row=1, column=0, sticky=E, padx=10, pady=4)
        self.entry5 = Entry(app, width=65)
        self.entry5.grid(row=1, column=1, columnspan=2, sticky=sty, padx=10, pady=10)
        self.entry5.bind('<Any-KeyRelease>', self.update_name)

        Label(app, text="Supplier RO").grid(row=2, column=0, sticky=E, padx=10, pady=4)
        self.entry6 = Entry(app, width=65)
        self.entry6.grid(row=2, column=1, columnspan=2, sticky=sty, padx=10, pady=10)

        Label(app, text="Supplier CUI").grid(row=3, column=0, sticky=E, padx=10, pady=4)
        self.entry7 = Entry(app, width=65)
        self.entry7.grid(row=3, column=1, columnspan=2, sticky=sty, padx=10, pady=10)

        Label(app, text="Supplier Address").grid(row=4, column=0, sticky=E, padx=10, pady=4)
        self.textarea = Text(app, width=26, height=5, wrap=WORD, relief=FLAT)
        self.textarea.grid(row=4, column=1, columnspan=2, sticky=sty, padx=10, pady=10)
        self.textarea.configure(highlightthickness=1, highlightbackground="Grey")
        self.ef = self.textarea.configure()

        Label(app, text="Supplier Phone").grid(row=5, column=0, sticky=E, padx=10, pady=4)
        self.entry8 = Entry(app, width=65)
        self.entry8.grid(row=5, column=1, columnspan=2, sticky=sty, padx=10, pady=10)

        btn = Button(app, text="save", width=12, command=lambda: self.save(modify, self.tup), style="new.TButton")
        btn.grid(row=7, column=1, sticky=sty, padx=10, pady=10)
        copy = Button(app, text='save As Copy', command=lambda: self.save(False, self.tup), style='new.TButton')
        copy.grid(row=7, column=2, sticky=sty, padx=10, pady=10)
        if not modify:
            copy['state'] = DISABLED
        if modify:
            d = self.db.execute(""" select name, created_on from suppliers join purchase using (supplier_id) where 
            id="%s" """ % id).fetchone()

    def update_name(self, event):
        name = Filter(self.entry5.get()).title()
        if len(name) == 0:
            name = "Supplier Name"
        self.name.configure(text=name)

    def save(self, modify, tup):
        """entry5, entry6, entry7, textarea
                """
        name = Filter(self.entry5.get()).title()
        ro = Filter(self.entry6.get()).title()
        cui = Filter(self.entry7.get()).title()
        address = Filter(self.textarea.get(0.0, END)).title()
        phone = Filter(self.entry8.get()).title()
        if len(name.split()) == 0:
            return showinfo(title="Error", message="Supplier name must be specified", parent=self.master)
        if len(ro) == 0 and len(cui) == 0:
            return showinfo(title="Error", message="Either one of the RO or CUI must be specified", parent=self.master)
        if len(address) == 0:
            return showinfo(title="Error", message="You must specify the supplier's address", parent=self.master)
        if len(phone) == 0:
            return showinfo(title="Error", message="You must specify the supplier's phone", parent=self.master)
        vre = self.db.sqldb.get_supplier_id(ro)
        vre1 = self.db.sqldb.get_supplier_id(cui)
        if vre or vre1:
            return showinfo(title="Error", message="That supplier is already listed in the database",
                            parent=self.master)
        s_id = self.db.add_supplier(name, ro, cui, address, phone)
