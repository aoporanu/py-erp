import json
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.ttk import *

import requests

from src.Cython.proWrd1 import Filter

sty = N + W + S + E


class NewSupplier(Frame):
    """
    @param Frame frame:
    """
    def __init__(self, master, tup, modify, db, id):
        """

        @param master: root of this frame
        @param tup: values to be sent to the modify
        @param db: the database object
        @param id: the id to be modified|unused
        """
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
            value = "Nume Furnizor"
        self.name = Label(self.f,
                          text=value,
                          font=('Berlin Sans FB Demi', 40),
                          foreground=fg)
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
        """

        @param note: container for the widget
        @param modify: Boolean
        @param tup: the list containing the fields
        @param id: unused
        """
        app = Frame(note)
        app.grid(row=0, column=0)
        self.f.rowconfigure(0, weight=1)
        self.f.columnconfigure(0, weight=1)
        note.add(app, text='Detalii')
        Label(app,
              text='Detalii Furnizor',
              font=('Berlin Sans FB Demi', 23),
              foreground="#3496ff").grid(row=0,
                                         column=0,
                                         columnspan=2,
                                         sticky=sty)

        Label(app, text='Nume').grid(row=1,
                                     column=0,
                                     sticky=E,
                                     padx=10,
                                     pady=4)
        self.entry5 = Entry(app, width=65)
        self.entry5.grid(row=1,
                         column=1,
                         columnspan=2,
                         sticky=sty,
                         padx=10,
                         pady=10)
        self.entry5.bind('<Any-KeyRelease>', self.update_name)

        Label(app, text="RO").grid(row=2, column=0, sticky=E, padx=10, pady=4)
        self.entry6 = Entry(app, width=65)
        self.entry6.grid(row=2,
                         column=1,
                         columnspan=2,
                         sticky=sty,
                         padx=10,
                         pady=10)
        self.entry6.bind('<Any-KeyRelease>', self.get_by_ro)

        Label(app, text="CUI").grid(row=3, column=0, sticky=E, padx=10, pady=4)
        self.entry7 = Entry(app, width=65)
        self.entry7.grid(row=3,
                         column=1,
                         columnspan=2,
                         sticky=sty,
                         padx=10,
                         pady=10)
        # self.entry7.bind('<Any-KeyRelease>', self.get_by_ro)

        Label(app, text="Adresa").grid(row=4,
                                       column=0,
                                       sticky=E,
                                       padx=10,
                                       pady=4)
        self.textarea = Text(app, width=26, height=5, wrap=WORD, relief=FLAT)
        self.textarea.grid(row=4,
                           column=1,
                           columnspan=2,
                           sticky=sty,
                           padx=10,
                           pady=10)
        self.textarea.configure(highlightthickness=1,
                                highlightbackground="Grey")
        self.ef = self.textarea.configure()

        Label(app, text="Telefon").grid(row=5,
                                        column=0,
                                        sticky=E,
                                        padx=10,
                                        pady=4)
        self.entry8 = Entry(app, width=65)
        self.entry8.grid(row=5,
                         column=1,
                         columnspan=2,
                         sticky=sty,
                         padx=10,
                         pady=10)

        btn = Button(app,
                     text="salvare",
                     width=12,
                     command=lambda: self.save(modify, self.tup),
                     style="new.TButton")
        btn.grid(row=7, column=1, sticky=sty, padx=10, pady=10)
        copy = Button(app,
                      text='copiere',
                      command=lambda: self.save(False, self.tup),
                      style='new.TButton')
        copy.grid(row=7, column=2, sticky=sty, padx=10, pady=10)
        if not modify:
            copy['state'] = DISABLED
        if modify:
            d = self.db.sqldb.execute(
                """ select name, address, phone, cui, ro, created_on from suppliers where
            id="%s" """ % id).fetchone()
            if d[4] is '':
                self.entry6.insert(0, d[3])
            elif d[3] is '':
                self.entry7.insert(0, d[4])
            self.entry5.insert(0, d[0])
            self.entry6.insert(0, d[4])
            self.entry7.insert(0, d[3])
            self.entry8.insert(0, d[2])
            self.textarea.insert(0.0, d[1])

    def update_name(self, event):
        name = Filter(self.entry5.get()).title()
        if len(name) == 0:
            name = "Nume Furnizor"
        self.name.configure(text=name)

    def get_by_ro(self, event):
        cif = self.entry6.get()
        if cif == '':
            cif = self.entry7.get()
        company_details = self.db.sqldb.get_company_details
        headers = {'x-api-key': company_details['openapi_key']}
        response = requests.get('https://api.openapi.ro/api/companies/' + cif, headers=headers)
        if response.status_code == 200:
            resp = json.loads(response.content.decode('utf-8'))
            self.entry5.insert(0, resp['denumire'])
            self.textarea.insert(0.0, resp['adresa'])
            self.entry8.insert(0, resp['telefon'])

    def save(self, modify, tup):
        """
        entry5, entry6, entry7, textarea

        @param modify: Boolean
        @param tup the values to be saved
        @return Information
        """
        name = Filter(self.entry5.get()).title()
        ro = Filter(self.entry6.get()).title()
        cui = Filter(self.entry7.get()).title()
        address = Filter(self.textarea.get(0.0, END)).title()
        phone = Filter(self.entry8.get()).title()
        if len(name.split()) == 0:
            return showinfo(title="Eroare",
                            message="Trebuie un nume pentru furnizor",
                            parent=self.master)
        if len(ro) == 0 and len(cui) == 0:
            return showinfo(
                title="Eroare",
                message=
                "Trebuie sa introduci fie CUI-ul fie RO-ul furnizorului",
                parent=self.master)
        if len(address) == 0:
            return showinfo(title="Eroare",
                            message="Trebuie sa introduci adresa furnizorului",
                            parent=self.master)
        if len(phone) == 0:
            return showinfo(
                title="Eroare",
                message="Trebuie sa specifici telefonul furnizorului",
                parent=self.master)
        vre = self.db.sqldb.get_supplier_id(ro)
        vre1 = self.db.sqldb.get_supplier_id(cui)
        if vre or vre1:
            return showinfo(
                title="Eroare",
                message="Furnizorul este deja listat in baza de date",
                parent=self.master)
        s_id = self.db.add_supplier(name, ro, cui, address, phone)
        return s_id
