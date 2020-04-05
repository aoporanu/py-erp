from tkinter import *
from tkinter.ttk import *
from Src.TableTree import MultiListbox

sty = N + S + E + W


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
        self.for_invoice = Combobox(self.d_frame, postcommand=lambda: self.search_invoice(), width=35, height=18)
        self.for_invoice.grid(row=0, column=0, sticky=sty, padx=5, pady=5)
        self.mlb = MultiListbox(self.d_frame, (("Purchase Date", 40), ("Product Name", 40), ("Quantity Brought", 20),
                                              ("Cost Price", 30), ("Lot", 20), ("Supplier", 30),
                                              ("Pentru factura", 20)))
        self.mlb.grid(row=1, column=0, sticky=sty, padx=5, pady=5)
        self.a_menu = Menu(master, tearoff=0)
        self.a_menu.add_command(label='Delete', command=self.delete)
        self.a_menu.add_command(label='Say Hello', command=self.hello)
        self.mlb.bind("<Button-3>", self.show_menu)
        self.assign()

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

    def search_invoice(self):
        pass
