import tkinter as tk
from tkinter import N, S, E, W, FLAT, VERTICAL, X, Y, END, HORIZONTAL, BOTTOM, RIGHT, FALSE, TRUE
from tkinter.ttk import *


class MultiListbox(Frame):
    def __init__(self, master, lists, height=None):
        Frame.__init__(self, master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.Select_index = None
        self.Select_iid = None
        self.b = []
        self.count = 0
        s = Style()
        s.configure("new.Treeview", font=("Ebrima", 9))
        s.configure("new.Treeview.Heading", font=("Arial Rounded MT Bold", 10))
        append = self.b.append
        for i in lists:
            append(i[0])
        if height is None:
            self.tree = Treeview(self, column=self.b, selectmode='browse', style="new.Treeview")
        else:
            self.tree = Treeview(self, column=self.b, selectmode='browse', style="new.Treeview", height=height)
        self.tree.grid(row=0, column=0, sticky=N + S + E + W)
        self.lists = []
        self.parent_elements = []
        tree = self.tree
        for l, w in lists:
            tree.column(l, width=w * 5)
            tree.heading(l, text=l)
        frame = Frame(self)
        frame.grid(row=0, column=1, sticky=N + S + E + W)
        bn = Label(frame, width=1, relief=FLAT)
        bn.pack(fill=X)
        xsb = Scrollbar(self, orient=HORIZONTAL, command=self.tree.xview)
        sb = Scrollbar(frame, orient=VERTICAL, command=self.tree.yview)
        sb.pack(side="right", expand=FALSE, fill=Y)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.configure(xscrollcommand=xsb.set)
        self.first_column("No", width=60)
        self.tree.bind('<1>', self.row_select)
        self.V = tk.StringVar()
        lbl = Label(self, relief=FLAT, textvariable=self.V, anchor=E, font=("Ebrima", 8), foreground="#fefefe")
        xsb.grid(row=3, column=0, columnspan=2, sticky=N+E+S+W)
        lbl.grid(row=4, column=0, columnspan=2, sticky=N + E + S + W, pady=0, padx=15)
        self.V.set("Number of Entries - %d" % (len(self.lists)))

    def row_select(self, event):
        inter = self.tree.identify_row(event.y)
        if inter == "":
            return 0
        self.Select_iid = inter
        self.Select_index = self.lists.index(inter)

    def first_column(self, head="", width=0, stretch=0):
        """Use To set the heading of the key column
           along with column width and stretchability
        """
        self.tree.column("#0", minwidth=0, width=width, stretch=stretch)
        self.tree.heading('#0', text=head)

    def true_parent(self, iid):
        piid = iid
        while piid != "":
            iid = piid
            piid = self.tree.parent(iid)
        return iid

    def delete(self, first, last=None):
        self.__dele(first, last)
        self.V.set("Number of Entries - %d" % self.count)
        if self.count < 1:
            self.Select_index = None

    def __dele(self, first, last):
        """delete a particular row"""
        if len(self.lists) == 0:
            return 0
        iid = self.lists[first]
        if last == END:
            self.count = 0
            niid = self.parent_elements[0]
            while niid != "":
                cdel = niid
                niid = self.tree.next(niid)
                self.tree.delete(cdel)
            self.parent_elements = []
            self.lists = []
            return None
        elif last is None:
            del self.lists[first]
            try:
                self.parent_elements.remove(iid)
            except ValueError:
                pass
            self.count -= 1
            return self.tree.delete(iid)

    def get(self, iid, column=None):
        """get value of the row if only iid is specified
           else if column is specified it gets the exact value of
           that row in the column
        """
        if iid is None:
            return 0
        iid = self.lists[iid]
        if column is None:
            l = range(len(self.b))
            d = self.tree.set(iid, column=column)
            bi = self.b.index

            def done(i):
                index = bi(i)
                l[index] = d[i]

            non = map(done, d.keys())
            del non
            return l
        else:
            return self.tree.set(iid, column=column)

    def set_value(self, iid, column, value):
        """set the value of the cell[iid][column]"""
        iid = self.lists[iid]
        return self.tree.set(iid, column=column, value=value)

    def row(self, iid, **options):
        """use to retrieve or set different values of
           row iid"""
        if type(iid) == int:
            iid = self.lists[iid]
        return self.tree.item(iid, **options)

    def column(self, iid, **options):
        """use to retrieve or set different values of a column"""
        if type(iid) == int:
            iid = self.b[iid]
        return self.tree.column(iid, **options)

    def index(self, iid):
        """Corresponding index of the id value"""
        return self.lists.index(iid)

    def insert(self, index, elements, fg='Black', bg=None, row_name=None, parent="", tag=None):
        """add a new row at the end of the table
        @param tag:
        @param parent:
        @param row_name:
        @param bg:
        @param fg:
        @param elements:
        @type index: object
        """
        tags = self.count
        if row_name is None:
            row_name = self.count + 1
        if parent != "":
            if tag is None:
                tags = 1
            else:
                tags = tag
        l = self.tree.insert(parent=parent, index=END, iid=None, values=elements, text=row_name, tags=tags)
        self.lists.append(l)
        if parent == "":
            self.parent_elements.append(l)
            self.count += 1
        if bg is None:
            bg = 'grey99'
            if tags % 2 == 0:
                bg = 'grey94'
        self.tree.tag_configure(tags, background=bg, foreground=fg)
        self.V.set("Number of Entries - %d" % self.count)
        return l

    def size(self):
        return len(self.lists)

    def see(self, iid):
        if type(iid) == int:
            iid = self.lists[iid]
        return self.tree.see(iid)
