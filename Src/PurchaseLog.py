from tkinter import *
from tkinter.ttk import *
from Src.TableTree import MultiListbox

sty = N + S + E + W


class PurchaseLog(Frame):
    def __init__(self, master, db):
        Frame.__init__(self, master)
        self.master = master
        self.db = db
        self.date = {}
        self.mlb = MultiListbox(master, (("Purchase Date", 40), ("Product Name", 40), ("Quantity Brought", 20),
                                         ("Cost Price", 30), ("Lot", 20), ("Supplier", 30)))
        self.mlb.grid(row=0, column=0, sticky=sty)
        self.assign()

    def assign(self):
        row = self.db.sqldb.execute("""SELECT purchase_date,product_name,QTY,cost,lot FROM 
        purchase JOIN costs USING (cost_id) JOIN products on purchase.product_id=products.product_id join suppliers on 
        purchase.supplier_id=suppliers.id""").fetchall()
        print(row)
        for i in row:
            self.mlb.insert(END, i)
