import tkinter as tk
from tkinter import N, W, S, E, END

from src.Cython.proWrd1 import Filter
from src.MultiListbox import MultiListbox
from tkinter.ttk import *
from tkinter.messagebox import showinfo
from tkinter.messagebox import askokcancel


# from proWrd import Filter


class Category:
    def __init__(self, master, db):
        self.value = []
        self.db = db
        self.master = master
        self.f = Frame(master)
        self.f.grid(row=0, column=0, sticky=N + W + S + E)
        self.f.columnconfigure(0, weight=1)
        self.f.rowconfigure(1, weight=1)
        Label(self.f, text="Category List", foreground="#3496ff", font=('Berlin Sans FB Demi', 20)).grid(row=0,
                                                                                                         column=0,
                                                                                                         sticky=N + S +
                                                                                                         E + W)
        self.mlb1 = MultiListbox(self.f, (('Category Name', 35), ('No of Product', 45), ('Category ID', 30)), height=20)
        self.mlb1.grid(row=1, column=0, columnspan=4, sticky=N + W + S + E)
        self.Del = Button(self.f, text="delete", command=lambda: self.delete())
        self.Del.grid(row=2, column=3)
        self.Add = Button(self.f, text="ADD", command=lambda: self.add_category())
        self.Add.grid(row=2, column=1)
        self.Edit = Button(self.f, text="Edit", command=lambda: self.add_category(edit=True))
        self.Edit.grid(row=2, column=2)
        self.insert()

    def delete(self):
        index = self.mlb1.Select_index
        if index is None or index > self.mlb1.size():
            return showinfo('Select Error', 'Noting Is Selected', parent=self.master)
        tup = self.mlb1.get(index)
        s = askokcancel('Confirm', 'Are You Sure You Want To delete %s ?' % tup[0], parent=self.master)
        if s:
            self.db.delete_category(tup[0])
        return self.refresh(), showinfo('Successful', 'Successfully Deleted', parent=self.master)

    def insert(self):
        self.mlb1.delete(0, END)
        row = self.db.sqldb.execute("""SELECT * FROM category ORDER BY category_name """).fetchall()
        for i in row:
            row2 = self.db.sqldb.execute("""SELECT product_id,product_name FROM products JOIN category USING (
            category_id)
                                            WHERE category_id = "%s"  ORDER BY product_name """ % (i[0])).fetchall()
            iid = self.mlb1.insert(END, (i[1], len(row2), i[0]))
            self.mlb1.insert(END, ["Product ID", "Product Name", "Qty"], parent=iid, row_name="", bg='grey93', fg='Red',
                             tag="lo")
            for p in row2:
                qty = float(self.db.sqldb.get_quantity(p[0]))
                self.mlb1.insert(END, [p[0], p[1], qty], parent=iid, row_name="", bg='grey95', fg='Blue', tag="lol")
        return 1

    def add_category(self, edit=False):
        tup = []
        if edit:
            index = self.mlb1.Select_index
            if index is None or index > self.mlb1.size():
                return showinfo('Select Error', 'Noting Is Selected', parent=self.master)
            piid = self.mlb1.true_parent(self.mlb1.Select_iid)
            index = self.mlb1.index(piid)
            tup = self.mlb1.get(index)
        self.t = tk.Toplevel(master=self.master)
        self.t.title('Add Category')
        if edit:
            self.t.title('Edit Category')
        self.t['bg'] = 'white'
        Label(self.t, text="Category Name", background='white').grid(row=1, column=0, padx=5, pady=5)
        self.e = Entry(self.t)
        self.e.grid(row=1, column=1, sticky=E + S + W + N, padx=5, pady=5)
        btn = Button(self.t, text="save Category", command=lambda: self.acat(edit, tup))
        btn.grid(row=2, column=1, sticky=E + S + W + N, padx=5, pady=5)
        if edit:
            Label(self.t, text="Category ID : ", background='white').grid(row=0, column=0, padx=5, pady=5)
            Label(self.t, text=tup[2], background='white').grid(row=0, column=1, padx=5, pady=5)
            self.e.delete(0, END)
            self.e.insert(0, tup[0])
        self.t.mainloop()
        return 1

    def acat(self, edit, tup):
        cname = Filter(self.e.get()).title()
        catid = self.db.sqldb.getcategory_id(cname)
        if catid is not None:
            return showinfo('Type Error', 'Category Name Is Already Listed', parent=self.t)
        if len(cname.split()) == 0:
            return showinfo('Type Error', 'Category Name Must Be Specified', parent=self.t)
        if edit:
            self.db.edit_category_name(tup[0], cname)
        else:
            self.db.add_category(cname)
        self.t.destroy()
        self.refresh()
        return showinfo('Successful', 'Changes Saved', parent=self.master)

    def refresh(self):
        return self.insert()
