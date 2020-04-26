from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.ttk import *
from src.TableTree import MultiListbox
from src.pcclass import InventoryDataBase

sty = N + S + E + W
db = InventoryDataBase()


class PurchaseLog(Frame):
    def __init__(self, master, db, **kw):
        Frame.__init__(self, master)
        super().__init__(master, **kw)
        self.master = master
        self.db = db
        self.date = {}
        self.d_frame = Frame(master)
        self.scrollbar_x = Scrollbar(self.d_frame, orient=HORIZONTAL)
        self.d_frame.grid(row=0, column=0, sticky=sty)
        self.d_frame.columnconfigure(0, weight=1)
        self.d_frame.rowconfigure(0, weight=1)
        self.for_invoice = Combobox(self.d_frame, postcommand=lambda: self.sales_invoice_combo_search(), width=35,
                                    height=18)
        self.for_invoice.grid(row=0, column=0, sticky=sty, padx=5, pady=5)
        self.for_invoice.bind('<<ComboboxSelected>>', self.call_sales_invoice_search)
        self.mlb = MultiListbox(self.d_frame, (("Purchase Date", 40), ("Product Name", 40), ("Quantity Brought", 20),
                                               ("Cost Price", 30), ("Lot", 20), ("Supplier", 30),
                                               ("Pentru factura", 20)))
        self.mlb.grid(row=1, column=0, sticky=sty, padx=5, pady=5)
        self.a_menu = Menu(master, tearoff=0)
        self.a_menu.add_command(label='Delete', command=self.delete)
        self.a_menu.add_command(label='Say Hello', command=self.hello)
        self.mlb.bind("<Button-3>", self.show_menu)
        self.assign()

    def call_sales_invoice_search(self, event):
        self.sales_invoice_search(self.for_invoice)

    def delete(self):
        pass

    def hello(self):
        pass

    def assign(self):
        row = self.db.sqldb.execute("""SELECT purchase_date,product_name,QTY,cost,lot,name,for_invoice FROM 
        purchase JOIN costs USING (cost_id) JOIN products on purchase.product_id=products.product_id join suppliers on 
        purchase.supplier_id=suppliers.id""").fetchall()
        for i in row:
            self.mlb.insert(END, i)

    def show_menu(self, event):
        print('show')
        self.iid = self.mlb.tree.identify_row(event.y)
        if self.iid:
            self.mlb.tree.selection_set(self.iid)
            self.a_menu.post(event.x_root, event.y_root)
        else:
            pass

    def sales_invoice_combo_search(self):
        inp = str(self.for_invoice.get())
        if inp == " ":
            inp = ""
        l = db.search_sales_invoice(inp)
        return self.add(self.for_invoice, l)
        # if l is not None:
        #     self.mlb.delete(0, END)
        #     for i in l:
        #         self.mlb.insert(END, i)

    def sales_invoice_search(self, inp):
        row = self.db.sqldb.execute("""SELECT purchase_date,product_name,QTY,cost,lot,name,for_invoice FROM 
        purchase JOIN costs USING (cost_id) JOIN products on purchase.product_id=products.product_id join suppliers on 
        purchase.supplier_id=suppliers.id WHERE for_invoice = "%%%s%%" """ % inp).fetchall()
        print(row)
        if row is not None:
            self.mlb.delete(0, END)
            for i in row:
                i = list(i)
                self.mlb.insert(END, i)
            self.for_invoice.delete(0, END)
        else:
            showinfo("Message", "There are no sales invoices that match")

    @staticmethod
    def add(obj, l):
        l = list(l)
        l.sort()
        obj["value"] = ""
        obj["value"] = list(l)
        print(obj['value'])
