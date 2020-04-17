import subprocess, sys
import os
import tkinter as tk
import tkinter.font as tkFont
from pathlib import Path

from tkinter.filedialog import askopenfilename, N, S, E, W, HORIZONTAL, asksaveasfilename
from tkinter.ttk import Style, Label, Frame, Combobox, Notebook, LabelFrame, Separator, Button, Entry, Spinbox, \
    Labelframe
from tkinter import DoubleVar, TOP, RIGHT, FLAT, LEFT, NORMAL, messagebox

import PIL.Image
import PIL.ImageTk
from reportlab import xrange

# TODO supplier multilistbox

from src.Cython.proWrd1 import Filter

import src.TableTree as tableTree
from src.Cato_Opt import Category
from src.NewCustomer import NewCustomer
from src.NewInvoice import ADDInvoice
from src.NewProduct import NewProduct, ProductVariant
from src.NewSupplier import NewSupplier
from src.PdfGenarator import pdf_document, nir_document
from src.PurchaseLog import PurchaseLog
from src.buttoncalender import CalendarButton, WORD, END
from src.pcclass import InventoryDataBase
from src.scroll_frame import SampleApp
from src.UnitsOfMeasure import UnitsOfMeasure
from src.Graph import Graph

# variable access by all

DB = InventoryDataBase()

# Window

root = tk.Tk()
root.title("Inventory Manager")
# root.iconbitmap('data/database_4.ico')
root.minsize(1024, 768)
root.grid()
root.rowconfigure(0, weight=1)
for h in range(12):
    root.columnconfigure(h, weight=1)
root.rowconfigure(2, weight=2)
root.wm_state('normal')
color = '#323232'
SEL_COLOR = '#273f5c'
FOREGROUND = "#cecece"
root['background'] = color

menubar = tk.Menu(root, background=color, activebackground=SEL_COLOR, foreground=FOREGROUND,
                  activeforeground="#FFFFFF")
filemenu = tk.Menu(menubar, tearoff=0, background=color, activebackground=SEL_COLOR, foreground=FOREGROUND,
                   activeforeground="#FFFFFF")
editmenu = tk.Menu(menubar, tearoff=0, background=color, activebackground=SEL_COLOR, foreground=FOREGROUND,
                   activeforeground="#FFFFFF")
menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Edit", menu=editmenu)
filemenu.add_command(label="  save Customer and Product", command=lambda: DB.Save(), bitmap='info', compound=LEFT)
filemenu.add_command(label="  Load database File", command=lambda: ask_dbfile(), bitmap='question', compound=LEFT)
filemenu.add_command(label="  Exit", command=lambda: call_save(), bitmap='error', compound=LEFT)
editmenu.add_command(label="Company Details", command=lambda: cdmp_del(), bitmap='info', compound=LEFT)
editmenu.add_command(label="Reset All", command=lambda: reset(), bitmap='info', compound=LEFT)
root.config(menu=menubar)

styl = Style()
styl.configure("r.TFrame", background=color)
styl.configure("r.TNotebook", background=color)
styl.configure("r.TButton", background=color)
styl.configure("r.TLabel", background=color)
styl.configure(".", background=color, font=("Arial Rounded MT Bold", 10))
styl.configure("r.TLabelframe", background=color)

# notebook
upnote = Frame(root, style='r.TFrame')
upnote.grid(row=0, column=0, columnspan=12, sticky=N + S + E + W)
upnote.columnconfigure(0, weight=1)
upnote.rowconfigure(0, weight=1)

note = Notebook(upnote, style='r.TNotebook')
note.grid(row=0, column=0, sticky=N + S + E + W)
note.rowconfigure(0, weight=1)
note.columnconfigure(0, weight=1)

btnnote = Notebook(root, style="r.TFrame")
btnnote.grid(row=3, column=0, columnspan=4, sticky=N + S + E + W)
btnnote.columnconfigure(0, weight=1)
btnnote.rowconfigure(0, weight=1)
saveico = os.path.normpath('data/floppy_disk_blue.png')
saveico = PIL.Image.open(saveico).resize((32, 32), PIL.Image.ANTIALIAS)
saveico = PIL.ImageTk.PhotoImage(image=saveico)
Button(btnnote, text="save", command=lambda: DB.save(), compound=TOP, image=saveico, width=1).grid(row=0, column=0,
                                                                                                   sticky=N + S + W + E)
NEW_ICO = os.path.normpath('data/new_file.png')
npico = PIL.Image.open(NEW_ICO).resize((32, 32), PIL.Image.ANTIALIAS)
npico = PIL.ImageTk.PhotoImage(image=npico)
productbtn = Button(btnnote, text="New Product", command=lambda: a_d_d__product(modify=False), image=npico,
                    compound=TOP,
                    width=1).grid(row=0, column=1, sticky=N + S + W + E)
NEW_USER_GROUP = os.path.normpath('data/user_group_new.png')
ncico = PIL.Image.open(NEW_USER_GROUP).resize((32, 32), PIL.Image.ANTIALIAS)
ncico = PIL.ImageTk.PhotoImage(image=ncico)
customerbtn = Button(btnnote, text="New Customer", command=lambda: a_d_d__customer(modify=False), image=ncico,
                     compound=TOP,
                     width=1).grid(row=0, column=2, sticky=N + S + W + E)
SETTINGS_ICO = os.path.normpath('data/settings_ico2.png')
setting_ico = PIL.Image.open(SETTINGS_ICO).resize((32, 32), PIL.Image.ANTIALIAS)
setting_ico = PIL.ImageTk.PhotoImage(image=setting_ico)
Button(btnnote, text="Edit Company Details", command=lambda: cdmp_del(),
       image=setting_ico, compound=TOP, width=1).grid(row=0,
                                                      column=3,
                                                      sticky=N + S + W + E)

app = Frame(note)
app.grid(row=0, column=0, sticky=N + S + E + W)
note.add(app, text='    Invoice    ')

app.columnconfigure(0, weight=1)
app.rowconfigure(1, weight=1)
app.rowconfigure(2, weight=5)

Label(app, text="Create Invoice And Sell Product", foreground="#3496ff",
      font=('Berlin Sans FB Demi', 20), background="#323232").grid(row=0, column=0, sticky=N + S + E + W)

add_together = Frame(app)
add_together.grid(row=1, column=0, sticky=N + E + S + W)
add_together.rowconfigure(0, weight=1)

for h in range(3):
    add_together.columnconfigure(h, weight=1)

Lf01 = LabelFrame(add_together, text="Customer Options", labelanchor=N, style="r.TLabelframe", width=2500)
Lf01.grid(row=0, column=0, sticky=N + E + S + W, padx=10, pady=10)
for h in range(3):
    Lf01.rowconfigure(h, weight=1)
for h in range(1, 2):
    Lf01.columnconfigure(h, weight=1)

# Customer name
lbl0 = Label(Lf01, text="Customer name", anchor=E)
lbl0.grid(row=0, column=0, sticky=N + E + S + W, pady=10, padx=5)

customer_name = Combobox(Lf01, postcommand=lambda: customer_name__search(), width=35)
customer_name.grid(row=0, column=1, sticky=N + E + S + W, pady=8, padx=10)

# Phone

lbl3 = Label(Lf01, text="Customer Contact No", anchor=E)
lbl3.grid(row=1, column=0, sticky=N + E + S + W, pady=10, padx=5)

customer_phone = Entry(Lf01, justify=RIGHT)
customer_phone.grid(row=1, column=1, sticky=N + S + E + W, pady=10, padx=10)

# Address


lbl1 = Label(Lf01, text="Customer Address", anchor=E)
lbl1.grid(row=2, column=0, sticky=N + E + W, pady=10, padx=5)

customer_address = tk.Text(Lf01, width=5, height=5, wrap=WORD, relief=FLAT)
customer_address.grid(row=2, column=1, sticky=N + E + S + W, pady=10, padx=10)
customer_address.configure(highlightthickness=1, highlightbackground="Grey", relief=FLAT)

#       Product name
Lf02 = LabelFrame(add_together, text="Product Options", labelanchor=N)
Lf02.grid(row=0, column=1, sticky=N + E + S + W, padx=5, pady=10)
Lf02.columnconfigure(1, weight=1)
for h in range(5):
    Lf02.rowconfigure(h, weight=1)

lbl6 = Label(Lf02, text="Product name", anchor=E)
lbl6.grid(row=0, column=0, sticky=N + E + S + W, padx=5, pady=10)

product_name = Combobox(Lf02, postcommand=lambda: product_name__search(), width=40)
product_name.grid(row=0, column=1, sticky=N + E + W + S, padx=5, pady=10)

# Product Detail
lbl8 = Label(Lf02, text="Product Description")
lbl8.grid(row=1, column=0, sticky=N + E, padx=5, pady=10)

product_detail = tk.Text(Lf02, width=4, height=2, wrap=WORD, relief=FLAT)
product_detail.grid(row=1, column=1, rowspan=2, sticky=N + E + S + W, pady=10, padx=5)
product_detail.configure(highlightthickness=1, highlightbackground="Grey", relief=FLAT)

# Product Price

lbl9 = Label(Lf02, text="Unit Price")
lbl9.grid(row=4, column=0, sticky=N + E, padx=5, pady=10)

product_price = Entry(Lf02, justify=RIGHT)
product_price.grid(row=4, column=1, sticky=N + E + S + W, padx=5, pady=10)

# QTY
lbl11 = Label(Lf02, text="Quantity")
lbl11.grid(row=3, column=0, sticky=N + E, padx=5, pady=10)

quantity = Entry(Lf02, justify=RIGHT)
quantity.grid(row=3, column=1, sticky=N + E + S + W, padx=5, pady=10)

# invoice option

Lf04 = LabelFrame(add_together, text="Invoice Options", labelanchor=N)
Lf04.grid(row=0, column=2, sticky=N + E + S + W, padx=5, pady=10)
Lf04.columnconfigure(1, weight=1)
for h in range(1, 10):
    Lf04.rowconfigure(h, weight=1)
# Invoice Date

Label(Lf04, text="Invoice Date", anchor=N + W).grid(row=0, column=0, sticky=N + E + W + S, padx=0, pady=0)

invoice_date = CalendarButton(Lf04)
invoice_date.grid(row=1, column=0, columnspan=2, sticky=N + E + S + W, padx=5, pady=0)

# Invoice Number
Label(Lf04, text="Invoice Number", anchor=N + W).grid(row=2, column=0, sticky=N + E + W + S, padx=5, pady=5)

invoice_number = Spinbox(Lf04, from_=0, to=10000, increment=1.0, wrap=True)
invoice_number.grid(row=2, column=1, sticky=N + E + W + S, padx=5, pady=5)
# +- Button

Cartindeldbnfram = Frame(Lf04)
Cartindeldbnfram.grid(row=9, column=0, columnspan=2, sticky=E + W + N + S, padx=0, pady=0)
Cartindeldbnfram.rowconfigure(0, weight=1)
Cartindeldbnfram.columnconfigure(0, weight=1)
Cartindeldbnfram.columnconfigure(1, weight=1)
ADD_TO_CART = os.path.normpath('data/cart_add.png')
tmp = PIL.Image.open(ADD_TO_CART).resize((25, 25), PIL.Image.ANTIALIAS)
tmp = PIL.ImageTk.PhotoImage(image=tmp)
Button(Cartindeldbnfram, text="Add To Cart", image=tmp,
       compound=LEFT, command=lambda: add_2_cart()).grid(row=0, column=0,
                                                         sticky=E + W + N + S,
                                                         padx=5,
                                                         pady=5)
REMOVE_FROM_CART = os.path.normpath('data/cart_remove.png')
tmp2 = PIL.Image.open(REMOVE_FROM_CART).resize((25, 25), PIL.Image.ANTIALIAS)
tmp2 = PIL.ImageTk.PhotoImage(image=tmp2)
Button(Cartindeldbnfram, text="Remove From Cart", image=tmp2,
       compound=LEFT, command=lambda: remove_from_cart()).grid(row=0, column=1,
                                                               sticky=E + W + N + S, padx=5,
                                                               pady=5)

# side

dframe = Frame(app)
dframe.grid(row=2, column=0, sticky=N + S + E + W)
dframe.columnconfigure(0, weight=1)
dframe.rowconfigure(0, weight=1)

# Amount
Lf03 = LabelFrame(dframe, text="Billing Options", labelanchor=N)
Lf03.grid(row=0, column=1, sticky=N + E + S + W)

Fon = tkFont.Font(family='Times', size=17)
Fon1 = tkFont.Font(family='Times', size=14)

# AMOUNT

lbl27 = Label(Lf03, text="Amount :", font=Fon1)
lbl27.grid(row=0, column=0, sticky=E + N + S, padx=10, pady=10)

Amt_var = tk.DoubleVar()

Amount = Label(Lf03, font=Fon1, textvariable=Amt_var)
Amount.grid(row=0, column=1, sticky=N + E + S + W, padx=10, pady=10)


# GST

def get_sgst():
    """ returns sgst """
    return DB.sqldb.get_company_details['sgst']


def get_cgst():
    """ gets cgst """
    return DB.sqldb.get_company_details['cgst']


def tax_update():
    """ UPDATE TAX """
    sgst_var.set(round(get_sgst() * (Amt_var.get() / 100), 2))
    cgst_var.set(round(get_cgst() * (Amt_var.get() / 100), 2))
    subtol_var.set(round(sgst_var.get() + cgst_var.get() + Amt_var.get(), 2))
    entry20.delete(0, END)
    entry20.insert(0, str(subtol_var.get()))
    Discount_var.set(0.0)
    Gtol_var.set(subtol_var.get())


Amt_var.trace('w', tax_update)

Label(Lf03, text="SGST @ " + str(get_sgst()) + "% : ", font=Fon1).grid(row=1, column=0, sticky=E + N + S, padx=10,
                                                                       pady=10)

sgst_var = tk.DoubleVar()

sgst = Label(Lf03, font=Fon1, textvariable=sgst_var)
sgst.grid(row=1, column=1, sticky=N + E + S + W, padx=10, pady=10)

Label(Lf03, text="CGST @ " + str(get_cgst()) + "% : ", font=Fon1).grid(row=2, column=0, sticky=E + N + S, padx=10,
                                                                       pady=10)

cgst_var = tk.DoubleVar()

cgst = Label(Lf03, font=Fon1, textvariable=cgst_var)
cgst.grid(row=2, column=1, sticky=N + E + S + W, padx=10, pady=10)

Separator(Lf03, orient=HORIZONTAL).grid(row=3, column=0, columnspan=2, sticky="ew", padx=8, pady=4)

# subtotal

Label(Lf03, text="Sub Total :", font=Fon1).grid(row=4, column=0, sticky=E + N + S, padx=10, pady=10)
subtol_var = tk.DoubleVar()
Label(Lf03, font=Fon1, textvariable=subtol_var).grid(row=4, column=1, sticky=W + N + S, padx=10, pady=10)

# Paid

lbl20 = Label(Lf03, text="Paid :", font=Fon1)
lbl20.grid(row=5, column=0, sticky=E + N + S, padx=10)

entry20 = Entry(Lf03)
entry20.grid(row=5, column=1, sticky=N + S + E + W, padx=5)

# Discount

lbl28 = Label(Lf03, text="Discount :", font=Fon1)
lbl28.grid(row=6, column=0, sticky=E + N + S, padx=10, pady=10)

Discount_var = DoubleVar()

Discount = Label(Lf03, font=Fon1, textvariable=Discount_var)
Discount.grid(row=6, column=1, sticky=W + N + S, padx=10, pady=10)

# Grand Total

Separator(Lf03, orient=HORIZONTAL).grid(row=7, column=0, columnspan=2, sticky="ew", padx=8, pady=4)

lbl25 = Label(Lf03, text="Grand Total :", font=Fon)
lbl25.grid(row=8, column=0, sticky=E + N + S, padx=10, pady=10)

Gtol_var = DoubleVar()

Gtol = Label(Lf03, font=Fon, textvariable=Gtol_var, width=10)
Gtol.grid(row=8, column=1, sticky=N + E + S + W, padx=10, pady=10)

# Generate
NEW_DOC = os.path.normpath('data/new_doc.png')
genico = PIL.Image.open(NEW_DOC).resize((32, 32), PIL.Image.ANTIALIAS)
genico = PIL.ImageTk.PhotoImage(image=genico)

butn_Gen = Button(Lf03, text="Generate Invoice", command=lambda: transfer(), image=genico, compound=LEFT)
butn_Gen.grid(row=9, column=0, columnspan=2, sticky=E + W + S + N, pady=10, padx=8)

# Table

mlb = tableTree.MultiListbox(dframe,
                             (("Cost ID", 20), ('Product', 35), ('Description', 45), ("QTY", 6), ("Unit Price", 9),
                              ("LOT", 35)))
mlb.grid(row=0, column=0, sticky=N + S + E + W, padx=10)


def purchase_product_frame():
    """ Build the Purchase frame """
    global product_name_search, qty_text, cost_price_text, btn64, selling_price_text, tmp4, tmp5, category_combo, \
        description_text, mlb21, supplier_combo_search, pentru_factura, lot_text
    #     note purchase product
    upf = Frame(note)
    upf.grid(row=0, column=0, sticky=N + W + S + E)
    note.add(upf, text="    Purchase    ")
    upf.columnconfigure(0, weight=1)
    upf.rowconfigure(1, weight=1)
    Label(upf, text="Products Purchase", foreground="#3496ff", font=('Berlin Sans FB Demi', 20)).grid(row=0, column=0,
                                                                                                      sticky=N + S +
                                                                                                             E + W)
    app6 = Frame(upf)
    app6.grid(row=1, column=0, sticky=N + W + S + E)
    for i in range(1):
        app6.columnconfigure(i, weight=1)
    for i in range(1, 5):
        if i == 2:
            continue
        app6.rowconfigure(i, weight=1)
    # Label(app6, background="Brown").grid(row=0, column=0, sticky=N + S + E + W)
    lfp = Frame(app6, padding="0.2i")
    lfp.grid(row=1, column=0, sticky=N + S + E + W)
    for i in range(1, 6):
        if i in (0, 2, 4):
            continue
        lfp.columnconfigure(i, weight=1)
    for i in range(0, 7):
        lfp.rowconfigure(i, weight=1)
    Label(lfp, text="Product name  ").grid(row=1, column=0, sticky=E, padx=10, pady=5)
    product_name_search = Combobox(lfp, postcommand=lambda: product_entry_search())
    product_name_search.grid(row=1, column=1, sticky=W + E, padx=10, pady=5)
    Label(lfp, text="Quantity  ").grid(row=3, column=0, sticky=E, padx=10, pady=5)
    qty_text = Entry(lfp)
    qty_text.grid(row=3, column=1, sticky=W + E, padx=10, pady=5)
    Label(lfp, text="Cost Price  ").grid(row=5, column=0, sticky=E, padx=10, pady=5)
    cost_price_text = Entry(lfp)
    cost_price_text.grid(row=5, column=1, sticky=W + E, padx=10, pady=5)
    Label(lfp, text="Purchase Date").grid(row=1, column=2, sticky=E, padx=10, pady=5)
    btn64 = CalendarButton(lfp)
    btn64.grid(row=1, column=3, sticky=W + E + S + N, padx=10, pady=5)
    Label(lfp, text="Selling Price  ").grid(row=3, column=2, sticky=E, padx=10, pady=5)
    selling_price_text = Entry(lfp)
    selling_price_text.grid(row=3, column=3, sticky=W + E, padx=10, pady=5)
    editbtnfram = Frame(lfp)
    editbtnfram.grid(row=5, column=3, sticky=N + E + S + W, padx=0, pady=0)
    editbtnfram.rowconfigure(0, weight=1)
    editbtnfram.columnconfigure(0, weight=1)
    editbtnfram.columnconfigure(1, weight=1)
    EDIT_ADD = os.path.normpath('data/edit_add.png')
    tmp4 = PIL.Image.open(EDIT_ADD).resize((25, 25), PIL.Image.ANTIALIAS)
    tmp4 = PIL.ImageTk.PhotoImage(image=tmp4)
    Button(editbtnfram, text="Add",
           image=tmp4, compound=LEFT,
           command=lambda: add2_purchase_table()).grid(row=0, column=0, sticky=N + E + S + W,
                                                       padx=10, pady=5)
    SYMBOL_REMOVE = os.path.normpath('data/symbol_remove.png')
    tmp5 = PIL.Image.open(SYMBOL_REMOVE).resize((25, 25), PIL.Image.ANTIALIAS)
    tmp5 = PIL.ImageTk.PhotoImage(image=tmp5)
    Button(editbtnfram, text="Remove",
           image=tmp5, compound=LEFT,
           command=lambda: delete_from_purchase_table()).grid(row=0, column=1,
                                                              sticky=N + W + S + E, padx=10,
                                                              pady=5)
    btn65 = Button(lfp, text=" Inventory Purchase Log ", width=20, command=lambda: ipurlog())
    btn65.grid(row=5, column=2, sticky=N + S + E + W, padx=10, pady=5)
    Label(lfp, text="Category  ").grid(row=1, column=4, sticky=E, padx=10, pady=5)
    category_combo = Combobox(lfp, postcommand=lambda: ckeys())
    category_combo.grid(row=1, column=5, sticky=W + E, padx=10, pady=5)
    Label(lfp, text="Description  ").grid(row=3, column=4, sticky=E + N, padx=10, pady=5)
    description_text = tk.Text(lfp, width=0, height=2, wrap=WORD, relief=FLAT)
    description_text.grid(row=3, column=5, rowspan=3, sticky=W + E + N + S, padx=10, pady=5)
    description_text.configure(highlightthickness=1, highlightbackground="Grey", relief=FLAT)
    Label(lfp, text="Pentru factura").grid(row=6, column=0, sticky=E, padx=5, pady=5)
    pentru_factura = Entry(lfp)
    pentru_factura.grid(row=6, column=1, sticky=W + E, padx=5, pady=5)
    Label(lfp, text="Supplier").grid(row=6, column=2, sticky=E, padx=10, pady=5)
    supplier_combo_search = Combobox(lfp, postcommand=lambda: supplier_keys(), width=40)
    supplier_combo_search.grid(row=6, column=3, sticky=N + E + W + S, padx=5, pady=10)
    Label(lfp, text="LOT   ").grid(row=6, column=4, sticky=E, padx=10, pady=5)
    lot_text = Entry(lfp)
    lot_text.grid(row=6, column=5, sticky=W + E, padx=10, pady=5)
    mlb21 = tableTree.MultiListbox(app6,
                                   (('Product name', 35), ("UM", 10), ("Cost Price", 25), ("Selling Price", 25), ("QTY",
                                                                                                                  15),
                                    ("Date", 35), ("LOT", 25), ("Pentru factura", 35)))
    mlb21.grid(row=3, column=0, columnspan=1, sticky=N + S + E + W)
    NEXT_ICO = os.path.normpath('data/next.png')
    tmp3 = PIL.Image.open(NEXT_ICO).resize((70, 70), PIL.Image.ANTIALIAS)
    tmp3 = PIL.ImageTk.PhotoImage(image=tmp3)
    btn62 = Button(app6, text="Complete Transaction", width=35,
                   image=tmp3, compound=LEFT,
                   command=lambda: add2_inventory())
    btn62.grid(row=8, column=0, sticky=N + E + S, pady=10)


purchase_product_frame()


# Label(app6, background="Brown").grid(row=5, column=0, sticky=N + S + E + W)
def inventory_product_list():
    """ Inventory frame """
    global h, product_search, tmp6, tmp7, tmp_modify, tmp_extra, uom_opt_event, mlb31
    # page 3
    # frame 3
    app2 = Frame(note)
    app2.grid(row=0, column=0)
    app2.columnconfigure(0, weight=1)
    app2.columnconfigure(1, weight=7)
    app2.rowconfigure(2, weight=1)
    note.add(app2, text='    Inventory    ')
    Label(app2, text='Inventory Product List',
          foreground="#3496ff", font=('Berlin Sans FB Demi', 20)).grid(row=0, column=0,
                                                                       columnspan=2,
                                                                       sticky=E + N + W + S,
                                                                       padx=10, pady=0)
    app2sub2 = Frame(app2)
    app2sub2.grid(row=1, column=0, sticky=N + S + W + E, padx=5, pady=0)
    app2sub2.columnconfigure(1, weight=1)
    app2sub2.columnconfigure(0, weight=5)
    app2sub2.rowconfigure(0, weight=1)
    lf3 = LabelFrame(app2sub2, text="Product Search Option")
    lf3.grid(row=0, column=0, sticky=N + S + W + E, padx=2, pady=10)
    for h in xrange(1, 3):
        lf3.columnconfigure(h, weight=1)
    for h in xrange(2):
        lf3.rowconfigure(h, weight=1)
    Label(lf3, text="Search KeyWord").grid(row=0, column=0, sticky=N + W + S + E, padx=5, pady=7)
    product_search = Combobox(lf3, width=35, postcommand=lambda: product__search())
    product_search.grid(row=0, column=1, columnspan=2, sticky=N + W + S + E, padx=5, pady=7)
    SEARCH_ICO = os.path.normpath('data/search.png')
    tmp6 = PIL.Image.open(SEARCH_ICO).resize((20, 20), PIL.Image.ANTIALIAS)
    tmp6 = PIL.ImageTk.PhotoImage(image=tmp6)
    Button(lf3, text="Search", width=15,
           image=tmp6,
           command=lambda: b_product__search()).grid(row=1, column=1, sticky=N + W + S + E,
                                                     padx=5, pady=5)
    VIEW_REFRESH_ICO = os.path.normpath('data/view_refresh.png')
    tmp7 = PIL.Image.open(VIEW_REFRESH_ICO).resize((20, 20), PIL.Image.ANTIALIAS)
    tmp7 = PIL.ImageTk.PhotoImage(image=tmp7)
    Button(lf3, text="refresh", width=15, image=tmp7,
           command=lambda: b_product__search(refresh=True)).grid(row=1, column=2,
                                                                 sticky=N + W + S + E, padx=5,
                                                                 pady=5)
    lf31 = LabelFrame(app2sub2, text="Product Edit Option")
    lf31.grid(row=0, column=1, sticky=N + W + S + E, padx=2, pady=10)
    for h in range(2):
        lf31.columnconfigure(h, weight=1)
    for h in range(2):
        lf31.rowconfigure(h, weight=1)
    Button(lf31, text="Add Product",
           image=tmp4, compound=LEFT,
           command=lambda: a_d_d__product(), width=20).grid(row=0, column=0, sticky=N + W + E + S,
                                                            padx=5, pady=5)
    Button(lf31, text="Remove Product",
           image=tmp5, compound=LEFT,
           command=lambda: remove__product(mlb31), width=20).grid(row=0, column=1,
                                                                  sticky=N + W + S + E, padx=5,
                                                                  pady=5)

    tmp_modify = PIL.Image.open(SETTINGS_ICO).resize((20, 20), PIL.Image.ANTIALIAS)
    tmp_modify = PIL.ImageTk.PhotoImage(image=tmp_modify)
    Button(lf31, text="Modify Product",
           image=tmp_modify, compound=LEFT,
           command=lambda: a_d_d__product(modify=True), width=20).grid(row=1, column=0,
                                                                       sticky=N + W + S + E,
                                                                       padx=5, pady=5)
    tmp_extra = PIL.Image.open(SETTINGS_ICO).resize((20, 20), PIL.Image.ANTIALIAS)
    tmp_extra = PIL.ImageTk.PhotoImage(image=tmp_extra)
    Button(lf31, text="Category Options",
           image=tmp_extra, compound=LEFT,
           command=lambda: category_opt_event(), width=20).grid(row=1, column=1,
                                                                sticky=N + W + S + E, padx=5,
                                                                pady=5)

    def uom_opt_event():
        rootd = tk.Toplevel(master=root)
        rootd.title("Unit of Measure Options")
        rootd.columnconfigure(0, weight=1)
        rootd.rowconfigure(0, weight=1)
        UnitsOfMeasure(rootd, DB)
        rootd.wait_window()
        return True

    Button(lf31, text="Unitati de masura", image=tmp_extra, compound=LEFT, command=lambda: uom_opt_event(),
           width=20).grid(row=2, column=0, sticky=N + W + S + E, padx=5, pady=5)
    mlb31 = tableTree.MultiListbox(app2,
                                   (('Product ID', 5), ('Product Name', 45), ('Category', 25), ('Description', 65),
                                    ("Unitate de masura", 10), ("QTY", 10)))
    mlb31.grid(row=2, column=0, columnspan=2, sticky=N + S + E + W)


inventory_product_list()


# page 4
# listing

def customer_database_list():
    """ Customer listing """
    global h, customer_search, mlb41
    app3 = Frame(note)
    app3.grid(row=0, column=0)
    app3.columnconfigure(0, weight=1)
    app3.columnconfigure(1, weight=5)
    app3.rowconfigure(2, weight=1)
    note.add(app3, text="    Customers    ")
    Label(app3, text='Customer database List',
          foreground="#3496ff", font=('Berlin Sans FB Demi', 20)).grid(row=0, column=0,
                                                                       columnspan=2,
                                                                       sticky=E + N + W + S,
                                                                       padx=10, pady=0)
    df = Frame(app3)
    df.grid(row=1, column=0, sticky=N + S + W + E)
    df.columnconfigure(0, weight=5)
    df.columnconfigure(1, weight=1)
    lf41 = LabelFrame(df, text="Customer Search Options")
    lf41.grid(row=0, column=0, sticky=N + S + W + E, padx=2, pady=0)
    lf41.columnconfigure(1, weight=1)
    lf41.columnconfigure(2, weight=1)
    for h in xrange(2):
        lf41.rowconfigure(h, weight=1)
    Label(lf41, text="Search KeyWord").grid(row=0, column=0, sticky=N + S + E, padx=5, pady=5)
    customer_search = Combobox(lf41, postcommand=lambda: customer__search(), width=35)
    customer_search.grid(row=0, column=1, columnspan=2, sticky=N + W + S + E, padx=5, pady=5)
    Button(lf41, text="Search", width=15, image=tmp6,
           command=lambda: b_customer__search()).grid(row=1, column=1, sticky=N + W + S + E,
                                                      padx=5, pady=5)
    Button(lf41, text="refresh", width=15, image=tmp7,
           command=lambda: b_customer__search(refresh=True)).grid(row=1, column=2,
                                                                  sticky=N + W + S + E,
                                                                  padx=5, pady=5)
    lf42 = LabelFrame(df, text="Customer Edit Options")
    lf42.grid(row=0, column=1, sticky=N + W + S + E, padx=2, pady=0)
    lf42.columnconfigure(0, weight=1)
    lf42.columnconfigure(1, weight=1)
    for h in xrange(2):
        lf42.rowconfigure(h, weight=1)
    Button(lf42, text="Add Customer", width=20,
           image=tmp4, compound=LEFT,
           command=lambda: a_d_d__customer()).grid(row=0, column=0, sticky=N + W + S + E,
                                                   padx=5, pady=5)
    Button(lf42, text="Remove Customer", width=20,
           image=tmp5, compound=LEFT,
           command=lambda: remove__customer(mlb41)).grid(row=0, column=1,
                                                         sticky=N + W + S + E,
                                                         padx=5, pady=5)
    Button(lf42, text="Modify Customer", width=20,
           image=tmp_modify, compound=LEFT,
           command=lambda: a_d_d__customer(modify=True)).grid(row=1, column=0,
                                                              sticky=N + W + E + S,
                                                              padx=5, pady=5)
    Button(lf42, text="Invoice Option", width=20,
           image=tmp_extra, compound=LEFT,
           command=lambda: invoice_opt_event()).grid(row=1, column=1,
                                                     sticky=N + W + E + S, padx=5,
                                                     pady=5)
    mlb41 = tableTree.MultiListbox(app3,
                                   (('Customer ID', 5), ('Customer Name', 40), ('Phone No', 15), ('Address', 70),
                                    ("Email", 30)))
    mlb41.grid(row=2, column=0, columnspan=2, sticky=N + S + E + W, pady=10)


customer_database_list()


# Page  5

def import_export():
    """ import export function """
    global h, entry51, entry52, entry53
    app4 = Frame(note)
    app4.grid(row=0, column=0)
    for h in range(8):
        app4.columnconfigure(h, weight=1)
    app4.columnconfigure(24, weight=1)
    note.add(app4, text="    Imports and Exports    ")
    Label(app4, text='Import and Export CSV',
          foreground="#3496ff", font=('Berlin Sans FB Demi', 20)).grid(row=0, column=0,
                                                                       sticky=E + N + W + S,
                                                                       padx=10, pady=0)
    lf2 = LabelFrame(app4, text="Import Option")
    lf2.grid(row=2, column=0, rowspan=5, columnspan=6, sticky=N + W + S + E, padx=10, pady=10)
    for h in range(7):
        lf2.columnconfigure(h, weight=1)
    lbl54 = Label(lf2, text="Import Product List From   ")
    lbl54.grid(row=2, column=1, sticky=N + E + S + W, padx=10, pady=10)
    entry51 = Entry(lf2, width=35)
    entry51.grid(row=2, column=2, columnspan=2, sticky=N + E + S + W, padx=10, pady=10)
    btn51 = Button(lf2, text="Browse File", command=lambda: brow__file(entry51))
    btn51.grid(row=2, column=5, sticky=N + E + S + W, padx=10, pady=10)
    C51 = tk.Canvas(app4, width=350, height=350, bg="White")
    C51.grid(row=2, rowspan=15, column=8, columnspan=15, sticky=N + E + W + S, padx=10, pady=10)
    Fon3 = tkFont.Font(family='Times', size=24)
    Fon4 = tkFont.Font(family='Times', size=16)
    ir3 = C51.create_text(205, 280, text="Total Solution To Inventory \n                         Management", font=Fon4)
    ir = C51.create_text(150, 50, text="     Inventory   Manager", font=Fon3)
    ir1 = C51.create_text(220, 90, text="         Powered by", font=Fon4)
    ir2 = C51.create_text(127, 215, text="Das \n      Enterprise", font=Fon3)
    lbl58 = Label(lf2, text="Import Customer List From   ")
    lbl58.grid(row=4, column=1, sticky=N + E + S + W, padx=10, pady=10)
    entry52 = Entry(lf2, width=35)
    entry52.grid(row=4, column=2, columnspan=2, sticky=N + E + S + W, padx=10, pady=10)
    btn52 = Button(lf2, text="Browse File", command=lambda: brow__file(entry52))
    btn52.grid(row=4, column=5, sticky=N + E + S + W, padx=10, pady=10)
    btn55 = Button(lf2, text="Import", command=lambda: import_csv(entry51.get(), entry52.get()))
    btn55.grid(row=6, column=4, columnspan=2, sticky=N + E + S + W, padx=10, pady=10)
    # LabelFrame Export Option
    lf1 = LabelFrame(app4, text="Export Option")
    lf1.grid(row=8, column=0, rowspan=9, columnspan=6, sticky=N + W + S + E, padx=10, pady=10)
    for h in range(7):
        lf1.columnconfigure(h, weight=1)
    lbl511 = Label(lf1, text="Export To  Folder ")
    lbl511.grid(row=8, column=1, sticky=N + E + S + W, padx=10, pady=10)
    entry53 = Entry(lf1, width=35)
    entry53.grid(row=8, column=2, columnspan=2, sticky=N + E + S + W, padx=10, pady=10)
    btn53 = Button(lf1, text="Choose File", command=lambda: save__as__file(entry53))
    btn53.grid(row=8, column=5, sticky=N + E + S + W, padx=10, pady=10)
    btn55 = Button(lf1, text="Export", command=lambda: export(entry53))
    btn55.grid(row=12, column=4, columnspan=2, sticky=N + E + S + W, padx=10, pady=10)


import_export()


def suppliers_frame():
    """ Suppliers frame """
    global h, supplier_combo_search, mlb51
    # Suppliers frame
    app5 = Frame(note)
    app5.grid(row=0, column=0)
    for h in range(8):
        app5.columnconfigure(h, weight=1)
    app5.columnconfigure(24, weight=1)
    note.add(app5, text="    Suppliers    ")
    Label(app5, text='Manage Suppliers',
          foreground="#3496ff", font=('Berlin Sans FB Demi', 20)).grid(row=0, column=0,
                                                                       sticky=E + N + W + S,
                                                                       padx=10, pady=0)
    ef = Frame(app5)
    ef.grid(row=1, column=0, sticky=N + S + W + E)
    ef.columnconfigure(0, weight=5)
    ef.columnconfigure(1, weight=1)
    lf51 = LabelFrame(ef, text="Supplier search Options")
    lf51.grid(row=0, column=0, sticky=N + S + W + E, padx=2, pady=0)
    lf51.columnconfigure(1, weight=1)
    lf51.columnconfigure(2, weight=1)
    for h in xrange(2):
        lf51.rowconfigure(h, weight=1)
    Label(lf51, text="Search Keyword").grid(row=0, column=0, sticky=N + S + E, padx=5, pady=5)
    supplier_combo_search = Combobox(lf51, postcommand=lambda: supplier_search(), width=35)
    supplier_combo_search.grid(row=0, column=1, columnspan=2, sticky=N + W + S + E, padx=5, pady=5)
    Button(lf51, text="Search", width=15, image=tmp6, command=lambda: b_supplier_search()).grid(row=1, column=1,
                                                                                                sticky=N + W + S + E,
                                                                                                padx=5, pady=5)
    Button(lf51, text="refresh", width=15, image=tmp7, command=lambda: b_supplier_search(refresh=True)).grid(row=1,
                                                                                                             column=2,
                                                                                                             sticky=N
                                                                                                                    + W
                                                                                                                    +
                                                                                                                    S +
                                                                                                                    E,
                                                                                                             padx=5,
                                                                                                             pady=5)
    lf52 = Labelframe(ef, text="Supplier Edit Options")
    lf52.grid(row=0, column=1, sticky=N + W + S + E, padx=2, pady=0)
    lf52.columnconfigure(0, weight=1)
    lf52.rowconfigure(0, weight=1)
    for h in xrange(2):
        lf52.rowconfigure(h, weight=1)
    Button(lf52, text="Add Supplier", width=20, image=tmp4, compound=LEFT, command=lambda: add_supplier()).grid(row=0,
                                                                                                                column=0,
                                                                                                                sticky=N
                                                                                                                       +
                                                                                                                       W
                                                                                                                       +
                                                                                                                       S
                                                                                                                       +
                                                                                                                       E,
                                                                                                                padx=5,
                                                                                                                pady=5)
    Button(lf52, text="Remove Supplier", width=20, image=tmp5, compound=LEFT,
           command=lambda: remove_supplier(mlb51)).grid(
        row=0, column=1,
        sticky=N + W + S + E,
        padx=5, pady=5)
    Button(lf52, text="Modify Supplier", width=20, image=tmp_modify, compound=LEFT, command=lambda: add_supplier(
        modify=True)).grid(row=1, column=0,
                           sticky=N + W + E + S,
                           padx=5, pady=5)
    mlb51 = tableTree.MultiListbox(app5, (("Supplier ID", 5), ("Supplier Name", 40), ("Supplier RO", 12), ("Supplier "
                                                                                                           "Address",
                                                                                                           70)))
    mlb51.grid(row=2, column=0, columnspan=2, sticky=N + S + E + W, pady=10)


suppliers_frame()

from Graph import Graph

app72 = Graph(note, 'RON', DB)
app72.grid(row=0, column=0, sticky=N + S + E + W)
note.add(app72, text='    Statistics   ')
app72.columnconfigure(0, weight=6)
app72.columnconfigure(1, weight=1)
app72.rowconfigure(0, weight=1)


# function
def supplier_search(refresh=False):
    inp = Filter(supplier_combo_search.get())
    if inp == " ":
        inp = ""
    l = supplier_name_search(inp)
    return add(supplier_combo_search, l)


def print_supplier_table(fst_l):
    lists = list(fst_l)
    lists.sort()
    mlb51.delete(0, END)
    for item in lists:
        tup = DB.sqldb.execute(""" select id, name, ro, address from suppliers""").fetchall()
        for p in tup:
            p = list(p)
            bg = None
            mlb51.insert(END, p, 'Black')
    supplier_combo_search.delete(0, END)
    return 1


def b_supplier_search(refresh=False):
    if not refresh:
        fst = split_reconstruct(str(supplier_combo_search.get()).split())
        BP_log1[0] = fst
    else:
        fst = BP_log1[0]
    fst_l = set(DB.search_supplier(fst))
    return print_supplier_table(fst_l)


def ckeys():
    category_combo['values'] = DB.categorylist
    return None


def supplier_keys():
    """

    @return:
    """
    supplier_combo_search["values"] = DB.get_supplier_names
    return None


def ipurlog():
    """

    """
    root23 = tk.Tk()
    root23.grid()
    root23.title("Purchase Log")
    root23.rowconfigure(0, weight=1)
    root23.columnconfigure(0, weight=1)
    p = PurchaseLog(root23, DB)
    p.grid(row=0, column=0, sticky=N + S + E + W)
    root23.mainloop()


def product_entry_search():
    """

    @return:
    """
    inp = str(product_name_search.get())
    if inp == " ":
        inp = ""
    l = product_name_search_func(inp)
    return add(product_name_search, l)


def call_purchase_search(event):
    """

    @param event:
    """
    product_entry_search()


def call_supplier_search(event):
    supplier_search()


def special_purchase_search(event):
    """

    @param event:
    @return:
    """
    inp = str(product_name_search.get())
    l = DB.sqldb.execute("""SELECT cost,price,category_name,product_description FROM costs JOIN products USING (
    product_id)
                JOIN category USING (category_id) WHERE product_name =  "%s" """ % (inp.title())).fetchone()
    if l is None:
        l = DB.sqldb.execute("""SELECT category_name,product_description FROM  products
                JOIN category USING (category_id) WHERE product_name =  "%s" """ % (inp.title())).fetchone()
        category = l[0]
        des = l[1]
        qty_text.delete(0, END)
        qty_text.insert(0, "1.0")
        category_combo.delete(0, END)
        description_text.delete(0.0, END)
        category_combo.insert(0, str(category))
        description_text.insert(0.0, str(des))
        return 1
    cost = l[0]
    price = l[1]
    category = l[2]
    des = l[3]
    qty_text.delete(0, END)
    cost_price_text.delete(0, END)
    selling_price_text.delete(0, END)
    category_combo.delete(0, END)
    description_text.delete(0.0, END)
    qty_text.insert(0, "1.0")
    cost_price_text.insert(0, str(cost))
    selling_price_text.insert(0, str(price))
    category_combo.insert(0, str(category))
    description_text.insert(0.0, str(des))


def get_um_for_product(pid):
    """

    @param pid:
    @return:
    """
    return DB.sqldb.get_um_for_product(pid)


def add2_purchase_table():
    """

    @return:
    """
    name = Filter(product_name_search.get()).title()
    qty = Filter(qty_text.get()).title()
    cost = Filter(cost_price_text.get()).title()
    date = Filter(btn64.get()).title()
    price = Filter(selling_price_text.get()).title()
    cat = Filter(category_combo.get()).title()
    des = split_reconstruct(description_text.get(0.0, END).split(" ")).title()
    lot = Filter(lot_text.get()).title()
    supplier = Filter(supplier_combo_search.get()).title()
    for_invoice = Filter(pentru_factura.get()).title()
    if len(qty.split()) == 0:
        return messagebox.showinfo("Input Error", "The Quantity provided Is Not Valid", parent=root)
    if len(date.split()) == 0:
        return messagebox.showinfo("Input Error", "The Date provided Is Not Valid", parent=root)
    if len(cat.split()) == 0:
        return messagebox.showinfo("Input Error", "The Category provided Is Not Valid", parent=root)
    if len(cost.split()) == 0:
        return messagebox.showinfo(title="Input Error", message='Product Cost Must Be Specified', parent=root)
    if len(price.split()) == 0:
        price = cost
    try:
        price = float(price)
        cost = float(cost)
        qty = float(qty)
    except ValueError:
        return messagebox.showinfo(title="Input Error", message='Product Quantity or Cost Price or Selling price Must '
                                                                'Be Numbers',
                                   parent=root)
    pid = DB.sqldb.getproductID(name)
    if pid is None:
        aut = messagebox.askokcancel("Authenticate", "The Product is not in the Product list \nLike To Add IT ?",
                                     parent=root)
        if not aut:
            return 0
        pid = DB.addproduct(name, cat, des)
    costid = DB.sqldb.getcostID(pid, cost, price)
    if costid is None:
        DB.addcost(name, cost, price)
    um = get_um_for_product(pid)[1]
    lopp = [name, um, cost, price, qty, date, lot, for_invoice, supplier]
    mlb21.insert(END, lopp)
    product_name_search.delete(0, END)
    qty_text.delete(0, END)
    cost_price_text.delete(0, END)
    selling_price_text.delete(0, END)
    category_combo.delete(0, END)
    description_text.delete(0.0, END)
    lot_text.delete(0, END)
    # We shouldn't delete the pentru factura and supplier_combo text
    # because we're adding products from an invoice, and one invoice
    # has one supplier and one invoice number
    # pentru_factura.delete(0, END)
    # instead
    pentru_factura.configure(state="readonly")
    # supplier_combo_search.delete(0, END)
    supplier_combo_search.configure(state="DISABLED")
    # btn64.configure(state="DISABLED")
    return 1


def delete_from_purchase_table():
    """

    @return:
    """
    index = mlb21.Select_index
    if index is None or index > mlb21.size():
        return messagebox.showinfo('Error', 'Nothing is Selected To Remove')
    mlb21.delete(index)


def add2_inventory():
    """

    @return:
    """
    tup_not_for = []
    if not mlb21.tree.get_children():
        return messagebox.showinfo("Error", "The purchase list is empty")
    for item in mlb21.tree.get_children():
        tup = mlb21.tree.item(item)
        name = tup['values'][0]
        cost = round(float(tup['values'][2]), 2)
        price = round(float(tup['values'][3]), 2)
        qty = round(float(tup['values'][4]))
        date = tup['values'][5]
        pid = DB.sqldb.getproductID(name)
        costid = DB.sqldb.getcostID(pid, cost, price)
        lot = tup['values'][6]
        for_factura = tup['values'][7]
        supplier = tup["values"][8]
        um = get_um_for_product(pid)

        # tup.insert(9, um)
        # tup.append(9)
        # tup[9] = um
        try:
            pur_id = DB.addpurchase(pid, costid, date, qty, lot, for_factura, supplier)
            tup_not_for.append(tup["values"])
            nir_document(tup_not_for, pur_id, supplier)
        except ValueError:
            ans = messagebox.askokcancel("Purchase already listed",
                                         "The purchase is already Listed \nLike to increase the product Quantity ?")
            if ans:
                pur_i_d = DB.sqldb.getpurchaseID(costid, date, qty)
                qty += DB.sqldb.get_cell("purchase", "purchase_id", "QTY", "\"" + pur_i_d + "\"")

                DB.sqldb.edit_purchase(pur_i_d, 2, qty)
    mlb21.delete(0, END)
    # make nir
    return messagebox.showinfo("Info", "All Products Has Been Added to the Inventory")


def reset():
    """

    @return:
    """
    s = messagebox.askokcancel("Warning", "Are you sure you want to reset every thing ?")
    if s:
        reset_coform()
    return 1


def reset_coform():
    """

    @return:
    """
    DB.sqldb.resetdatabase()
    return None


def remove__product(obj):
    """

    @param obj:
    @return:
    """
    del_row = obj.Select_index
    if del_row is None or del_row > obj.size():
        return messagebox.showinfo('Error', 'Nothing is Selected To Remove')
    tup = obj.get(del_row)
    ans = messagebox.askokcancel('WARNING', "Do You Really Want To delete " + tup[1] + " ?")
    if ans:
        ie = DB.deleteproduct(tup[0])
        if ie:
            messagebox.showinfo('Info', tup[1] + ' Successfully Deleted')
        else:
            messagebox.showinfo('Error', 'Sorry Cannot delete, Product is attached to Invoices or Purchase. delete '
                                         'Them '
                                         'first.')
    return b_product__search(refresh=True)


def remove__customer(obj):
    """

    @param obj:
    @return:
    """
    del_row = obj.Select_index
    if del_row is None or del_row > obj.size():
        return messagebox.showinfo('Error', 'Nothing is Selected To Remove')
    tup = obj.get(del_row)
    ans = messagebox.askokcancel('WARNING', "Do You Really Want To delete " + tup[1] + " ?")
    if ans:
        ie = DB.deletecustomer(tup[0])
        if ie:
            messagebox.showinfo('Info', tup[1] + 'Has Been Deleted')
        else:
            messagebox.showinfo('Error', 'Sorry Cannot delete, Customer is attached to invoices')
        return b_customer__search(refresh=True)
    else:
        return b_customer__search(refresh=True)


BC_log1 = [""]
BP_log1 = [""]


def b_product__search(refresh=False):
    """

    @param refresh:
    @return:
    """
    if not refresh:
        fst = split_reconstruct(str(product_search.get()).split())
        BP_log1[0] = fst
    else:
        fst = BP_log1[0]
    fst_l = set(DB.searchproduct(fst))
    return print__p_table(fst_l)


def print__p_table(lists):
    """

    @param lists:
    @return:
    """
    lists = list(lists)
    lists.sort()
    mlb31.delete(0, END)
    for item in lists:
        tup = DB.sqldb.execute(""" SELECT product_id,product_name,category_name,product_description,
        units_of_measure.name FROM
        products
                        JOIN category USING (category_id) join units_of_measure on products.um_id=units_of_measure.id
                        WHERE
                        product_name =
                        "%s" """ % item).fetchall()
        for p in tup:
            p = list(p)
            qty = float(DB.sqldb.get_quantity(p[0]))
            p.append(qty)
            bg = None
            colour = "White"
            if float(qty) > 0:
                colour = "Black"
            elif float(qty) == 0:
                colour = "Red"
            if float(qty) < 0:
                bg = "Brown"
            mlb31.insert(END, p, colour, bg)
    product_search.delete(0, END)
    return 1


def b_customer__search(refresh=False):
    """

    @param refresh:
    @return:
    """
    if not refresh:
        fst = Filter(str(customer_search.get()))
        BC_log1[0] = fst
    else:
        fst = BC_log1[0]
    fst_l = set(DB.searchcustomer(fst))
    return print__c_table(fst_l)


def print__c_table(lists):
    """

    @param lists:
    @return:
    """
    lists = list(lists)
    lists.sort()
    mlb41.delete(0, END)
    for item in lists:
        tup = DB.sqldb.execute("""SELECT customer_id,customer_name,phone_no,customer_address,customer_email
                       FROM customers JOIN contacts USING (customer_id)  WHERE customer_name = "%s" """ % (
            item)).fetchall()
        for c in tup:
            guiid = mlb41.insert(END, c, bg=None, tag="ta")
            tup1 = DB.sqldb.execute("""SELECT invoice_id,invoice_no,invoice_date,paid
                           FROM invoices WHERE customer_id = "%s" ORDER BY invoice_no """ % (c[0])).fetchall()
            mlb41.insert(END, ("Invoice ID", "Invoice No", "Invoice Time Stamp", "Paid"), parent=guiid,
                         row_name="",
                         bg='grey93', fg='Red', tag="lo")
            for p in tup1:
                mlb41.see(mlb41.insert(END, p, parent=guiid, row_name="", bg='White', fg='Blue', tag="lol"))
            tup2 = DB.sqldb.execute(""" select id, name, cnp, car_no from delegates where customer_id = "%s" order by
            id """ % (
                c[0])).fetchall()
            mlb41.insert(END, ("Delegate ID", "Delegate Name", "Delegate CNP", "# Auto"), parent=guiid, row_name="",
                         bg="grey93", fg="Green", tag="lo")
            for d in tup2:
                mlb41.see(mlb41.insert(END, d, parent=guiid, row_name="", bg="White", fg="Brown", tag="lol"))
    mlb41.see("")
    customer_search.delete(0, END)
    return 1


def special__p_search(event):
    """

    @param event:
    """
    st = str(product_name.get())
    l = DB.sqldb.execute("""SELECT product_description,price FROM costs JOIN products USING (product_id)
                 WHERE product_name =  "%s" """ % st).fetchone()
    des = l[0]
    price = l[1]
    qty = 1.00
    product_detail.delete(0.0, END)
    product_detail.insert(0.0, des)
    product_price.delete(0, END)
    product_price.insert(0, price)
    quantity.delete(0, END)
    quantity.insert(0, qty)


def special__c_search(event):
    """

    @param event:
    """
    st = str(customer_name.get())
    l = DB.sqldb.execute("""SELECT customer_address,phone_no FROM customers JOIN contacts USING (customer_id)
                 WHERE customer_name =  "%s" """ % st).fetchone()
    add_inner = l[0]
    phn = l[1]
    customer_address.delete(0.0, END)
    customer_address.insert(0.0, add_inner)
    customer_phone.delete(0, END)
    customer_phone.insert(0, phn)


def call__pn_search(event):
    """

    @param event:
    """
    product_name__search()


def product_name_search_func(string):
    """

    @param string:
    @return:
    """
    return DB.searchproduct(string.title())


def customer_name_search(string):
    return DB.searchcustomer(string.title())


def supplier_name_search(string):
    return DB.search_supplier(string.title())


def unit_name_search(string):
    return DB.search_um(string.title())


def invoice_no_search(string):
    return DB.searchinvoice(string.title())


def category_name_search(string):
    return DB.searchcategory(string.title())


def product_name__search():
    inp = str(product_name.get())
    if inp == " ":
        inp = ""
    l = product_name_search_func(inp)
    return add(product_name, l)


def call__cn_search(event):
    customer_name__search()


def customer_name__search():
    inp = Filter(customer_name.get())
    if inp == " ":
        inp = ""
    l = customer_name_search(inp)
    return add(customer_name, l)


def call__cu_search(event):
    customer__search()


# def call__i_search(event):
#     invoice__search()


def customer__search():
    inp = str(customer_search.get())
    if inp == " ":
        inp = ""
    l = customer_name_search(inp)
    return add(customer_search, l)


# def invoice__search():
#     inp = str(invoice_search.get())
#     if inp == " ":
#         inp = ""
#     l = invoice_no_search(inp)
#     return add(invoice_search, l)


def call__c_search(event):
    category__search()


def category__search():
    inp = str(category_combo.get())
    if inp == " ":
        inp = ""
    l = category_name_search(inp)
    return add(category_combo, l)


def product__search():
    inp = str(product_search.get())
    if inp == " ":
        inp = ""
    l = product_name_search_func(inp)
    return add(product_search, l)


def call__p_search(event):
    product__search()


def add(obj, l):
    l = list(l)
    l.sort()
    obj["value"] = ""
    obj["value"] = list(l)


def ask_dbfile():
    fname = askopenfilename(filetypes=(('Inventory Manager database File', "*.ic"), ('All File', "*.*")))
    try:
        ds = open(fname, 'r')
    except IOError:
        messagebox.showinfo("No File", "No File With Such name Found !")
        return 0
    del ds
    boo = DB.load(fname)
    b_customer__search(refresh=True)
    b_product__search(refresh=True)
    if not boo:
        return messagebox.showinfo("Message", "Loading of product Not Completed")
    return messagebox.showinfo("Message", "Loading of product successful")


def export(objentry1):
    from src.ImportExport import ExportCsv
    ans = messagebox.askokcancel("WARNING", "2 FILES WILL BE EXPORTED SURE YOU WANT EXPORT IN THIS FOLDER ?")
    if not ans:
        return False
    exportfile1 = Filter(str(objentry1.get()))
    if len(str(exportfile1).split()) == 0:
        pass
    else:
        ec = ExportCsv(exportfile1, DB)
        if ec.returns:
            objentry1.delete(0, END)
        del ec
    return messagebox.showinfo("Message", "Your File Has Been Exported Successfully")


def brow__file(obj):
    """Should alawys use entry widget as obj"""
    from tkinter.filedialog import askopenfilename
    try:
        fname = askopenfilename(filetypes=(('Csv File', "*.csv"), ('All File', "*.*")))
    except[IOError]:
        fname = ""
        messagebox.showinfo("File Error", "Choose Again")
    if len(fname) == 0:
        messagebox.showinfo("File Error", "You Must Choose a Csv File For Your Inventory")
        return None
    obj.delete(0, END)
    obj.insert(0, fname)
    return 1


def save__as__file(obj):
    """Should always use entry widget as obj"""
    try:
        fname = asksaveasfilename(defaultextension='.csv', filetypes=[('Csv File', "*.csv"), ('TEXT File', "*.txt")])
    except[IOError]:
        fname = ""
        messagebox.showinfo("File Error", "You must Export And Have A Backup")
    if len(fname) == 0:
        messagebox.showinfo("File Error", "You Must Choose a Csv File For Your Inventory")
        return None
    obj.delete(0, END)
    obj.insert(0, fname)
    return 1


def import_csv(objentry1, objentry2):
    """

    @param objentry1:
    @param objentry2:
    @return:
    """
    from src.ImportExport import ImportCsv
    importfile1 = Filter(str(objentry1))
    importfile2 = Filter(str(objentry2))
    if len(str(importfile1).split()) == 0:
        pass
    else:
        ic = ImportCsv(importfile1, "Product", DB)
        if ic.returns:
            entry51.delete(0, END)
        del ic
    if len(str(importfile2).split()) == 0:
        pass
    else:
        ic = ImportCsv(importfile2, "Customer", DB)
        if ic.returns:
            entry52.delete(0, END)
        del ic
    return 1


def invoice_opt_event():
    invoice__option()


def invoice__option():
    rootn = tk.Toplevel(master=root)
    rootn.title("Invoice Options")
    rootn.columnconfigure(0, weight=1)
    rootn.rowconfigure(0, weight=1)
    ADDInvoice(rootn, DB)
    rootn.wait_window()
    return 1


def category_opt_event():
    category__opt()
    return 1


def category__opt():
    rootd = tk.Toplevel(master=root)
    rootd.title("Category Options")
    rootd.columnconfigure(0, weight=1)
    rootd.rowconfigure(0, weight=1)
    Category(rootd, DB)
    rootd.wait_window()
    return True


def d_click__on__list(event):
    cur_item = mlb31.tree.focus()
    index = int(mlb31.tree.identify_column(event.x)[1])
    id = mlb31.tree.item(cur_item)
    arg = id["values"][0]

    if index == 3:
        return category_opt_event()
    elif 1 < index < 6:
        return a_d_d__product(arg, modify=True)
    else:
        return 0


def d_click__on__c_list(event):
    index = int(mlb41.tree.identify_column(event.x)[1])
    if index == 5:
        return invoice_opt_event()
    elif 7 > index > 1:
        return a_d_d__customer(modify=True)
    else:
        return 0


def get_pdf_date(timestamp):
    p = timestamp.split()
    del p[3]
    return " ".join(p)


product_search.bind('<Any-KeyRelease>', call__p_search)
customer_search.bind('<Any-KeyRelease>', call__cu_search)
customer_name.bind('<Any-KeyRelease>', call__cn_search)
product_name.bind('<Any-KeyRelease>', call__pn_search)
customer_name.bind('<<ComboboxSelected>>', special__c_search)
product_name.bind('<<ComboboxSelected>>', special__p_search)
mlb41.tree.bind('<Double-Button-1>', d_click__on__c_list)
mlb31.tree.bind('<Double-Button-1>', d_click__on__list)
product_name_search.bind('<Any-KeyRelease>', call_purchase_search)
product_name_search.bind('<<ComboboxSelected>>', special_purchase_search)
supplier_combo_search.bind('<Any-KeyRelease>', call_supplier_search)


def process_cart(invid):
    no_of_product = 0
    for item in mlb.tree.get_children():
        tup = mlb.tree.item(item)
        no_of_product += float(tup['values'][3])
    discount_per_product = float(Discount_var.get()) / no_of_product
    lik = []
    i = 1
    for item in mlb.tree.get_children():
        r = mlb.tree.item(item)
        costid = str(r['values'][0])
        product_name2 = str(r['values'][1])
        product_description = str(r['values'][2])
        product_qty = float(r['values'][3])
        product_price2 = float(r['values'][4])
        product_amount = product_qty * product_price2
        product_info = product_name2 + ' ' + product_description
        listsw = [i, product_info, product_qty, product_price2, str(product_amount)]
        lik.append(listsw)
        sold_price = product_price2 - discount_per_product
        DB.addsells(costid, sold_price, invid, product_qty)
        i += 1
    mlb.delete(0, END)
    return lik


def generate__invoice(product__list_forpdf, custup, invoicetup, detail):
    invoi_num = invoicetup[1]
    invoice__date2 = invoicetup[0]
    # Discount = invoicetup[4]
    # Amount = invoicetup[3]
    grand_total = invoicetup[2]
    cust_name = custup[1]
    cust_address = custup[2]
    cust_phone = custup[3]
    Company = detail['comp_name']
    Company_Adress = detail['comp_add']
    email = detail['comp_email']
    phone = detail['comp_phn']
    Detail_top = detail['detail_top']
    Extra_Info = detail['extra']
    Currency = detail['curry']

    PDfCompany_Adress = Company_Adress + "\n" + Detail_top + "\n" + email + "\n" + phone
    pdfcust_address = cust_address + "\n" + cust_phone
    delegate = DB.sqldb.get_delegate_for(custup[0])
    pdf_document(delegate,
                 pic_add="logo.png",
                 inv_no=str(invoi_num),
                 company_name=str(Company),
                 date=get_pdf_date(invoice__date2),
                 company_add=str(PDfCompany_Adress),
                 cus_name=str(cust_name),
                 cus_add=str(pdfcust_address),
                 plist=product__list_forpdf,
                 grand_total=str(grand_total),
                 bottom_detail=str(Extra_Info),
                 currency=Currency,
                 total_amt=Amt_var.get(),
                 s_g_s_t=sgst_var.get(),
                 c_g_s_t=cgst_var.get(),
                 discount=Discount_var.get(),
                 sub_total=subtol_var.get()
                 )
    fileline = "Invoice   " + invoi_num + ".pdf"
    p = Path('Invoices')
    p.mkdir(exist_ok=True)

    try:
        if sys.platform is "win32":
            os.startfile(fileline)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, fileline])
    except:
        fileline = askopenfilename(
            filetypes=(('Microsoft Word Document File', "*.docx"), ("Portable Document File", "*.pdf")))
        if sys.platform is "win32":
            os.startfile(fileline)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, fileline])
    return None


def transfer():
    Invoi_num = invoice__maintain()
    detail = DB.sqldb.get_company_details
    if Invoi_num is None:
        return 1
    alooas = DB.sqldb.get_invoice_ID(Invoi_num)
    if alooas is not None:
        return messagebox.showinfo("Error", "Invoice Number Already Exists And Assigned To another Customer",
                                   parent=root)
    if mlb.size() == 0:
        messagebox.showinfo("Input Error", "You Should Choose a Product", parent=root)
        return 1
    custup = pre_inv()
    if custup is None:
        return messagebox.showinfo("Error", "Customer Detail Incomplete", parent=root)
    if len(detail['comp_name']) == 0 or len(detail['comp_add']) == 0 or len(detail['comp_phn']) == 0:
        messagebox.showinfo("Input Error", "Company Detail Incomplete", parent=root)
        return 1
    ctmid, cust_name, cust_address, cust_phone = custup
    invoice__date2 = str(invoice_date.get())
    discount = str(Discount_var.get())
    amount = str(Amt_var.get())
    Grand_total = str(Gtol_var.get())
    invid = DB.addinvoice(ctmid, Invoi_num, Grand_total, invoice__date2)
    Product_List_forpdf = process_cart(invid)
    invoicetup = (invoice__date2, Invoi_num, Grand_total, amount, discount)
    generate__invoice(Product_List_forpdf, custup, invoicetup, detail)
    Discount_var.set(0.0)
    Amt_var.set(0.0)
    Gtol_var.set(0.0)
    customer_name.delete(0, END)
    customer_address.delete(0.0, END)
    customer_phone.delete(0, END)
    invoice_num()
    return 1


def split_reconstruct(item):
    lists = []
    for r in item:
        q = ""
        for w in r:
            if w == "\n" and r == item[0]:
                continue
            elif w == "\n" and r == item[(len(item) - 1)]:
                continue
            else:
                q = q + w
        lists.append(q)
    wrd = ""
    for item in range(len(lists)):
        if lists[item] == "" or lists[item] == " ":
            continue
        elif lists[item] == "\n" and lists[(item - 1)] == "":
            n = 0
            for e in range(0, item):
                if lists[e] != "":
                    n = n + 1
                    if 0 < n <= 1:
                        wrd = wrd + lists[item]
                    else:
                        continue
                else:
                    continue
            continue
        elif lists[item] == "\n" and lists[(item + 1)] == "":
            n = 0
            for e in range(item, len(lists)):
                if lists[e] != "":
                    n = n + 1
                    if 0 < n <= 1:
                        wrd = wrd + lists[item]
                    else:
                        continue
                else:
                    continue
            continue
        else:
            wrd = wrd + lists[item] + " "
    wrd = wrd[:(len(wrd) - 1)]
    return wrd


def invoice__maintain():
    detail = DB.sqldb.get_company_details
    x = Filter(str(invoice_number.get()))
    if not x.isdigit():
        messagebox.showinfo("Warning", "Invoice Number have to be Number and Nothing else")
        return None
    detail['inv_start'] = str(x)
    DB.sqldb.save_company_details(detail)
    return detail['inv_start']


def invoice_num():
    detail = DB.sqldb.get_company_details
    num = detail['inv_start']
    num = int(num) + 1
    invoice_number['state'] = NORMAL
    invoice_number.delete(0, END)
    invoice_number.insert(0, str(num))
    invoice_number['state'] = 'readonly'
    return 0


def invoice__date():
    invoice_date.insert(invoice_date.get_time_stamp())
    return 1


def remove_from_cart():
    index = mlb.Select_index
    if index is None or index > mlb.size():
        return messagebox.showinfo(title='Error', message='Nothing is Selected To Remove')
    tup = mlb.get(index)
    a = float(tup[3]) * float(tup[4])
    amount = float(Amt_var.get()) - a
    Amt_var.set(amount)
    mlb.delete(index)


def add_discount(event):
    paid = Filter(entry20.get())
    if len(paid) == 0:
        return 1
    if not paid.isdigit():
        try:
            paid = float(paid)
        except ValueError:
            messagebox.showinfo("Entry Error", "Discount Must Be Numbers Before ADDING The Discount")
            return 1
    paid = float(paid)
    dis = float(subtol_var.get()) - paid
    Discount_var.set(str(dis))
    Gtol_var.set(str(paid))


entry20.bind('<Any-KeyRelease>', add_discount)


def add_2_cart():
    product = Filter(str(product_name.get()))
    p_de = Filter(str(product_detail.get(0.0, END)))
    p_price = Filter(str(product_price.get()))
    qty = Filter(str(quantity.get()))
    if len(product) == 0:
        messagebox.showinfo("Empty Entry Error", "Product name Must Be Filled Before ADDING The Product")
        return 1
    if len(p_price) == 0:
        messagebox.showinfo("Empty Entry Error", "Product Price Must Be Filled Before ADDING The Product")
        return 1
    try:
        p_price = float(p_price)
    except ValueError:
        messagebox.showinfo("Empty Entry Error", "Product Price Must Be Numbers Before ADDING The Product")
        return 1
    if len(qty) == 0:
        messagebox.showinfo("Empty Entry", "Product Quantity Must Be Filled Before ADDING The Product")
        return 1
    try:
        qty = float(qty)
    except ValueError:
        messagebox.showinfo("Empty Entry Error", "Product quantity Must Be Numbers Before ADDING The Product")
        return 1
    PID = DB.sqldb.getproductID(product)
    if PID is None:
        return messagebox.showinfo("Empty Entry Error", "Product Not Listed Try ADDING The Product")
    costid = DB.getanycostid(PID, p_price)
    if costid is None:
        return messagebox.showinfo("Error", "No Purchase has Been Made For This Product, The Product Is Not In Stock")
    boo = False
    for ITEM in xrange(int(mlb.size())):
        r = mlb.get(ITEM)
        if costid == r[0]:
            newqty = float(r[3]) + float(qty)
            mlb.set_value(ITEM, "QTY", newqty)
            boo = True
    if not boo:
        tup = (costid, product, p_de, float(qty), p_price)
        mlb.insert(END, tup)
    a = float(p_price) * float(qty)
    amount = float(Amt_var.get())
    amount += a
    Amt_var.set(amount)
    product_name.delete(0, END)
    product_detail.delete(0.0, END)
    product_price.delete(0, END)
    quantity.delete(0, END)
    return None


def pre_inv():
    name = Filter(str(customer_name.get()))
    address = Filter(str(customer_address.get(0.0, END)))
    phone = Filter(str(customer_phone.get()))
    if len(name) == 0 or len(address) == 0 or len(phone) == 0:
        messagebox.showinfo("Empty Entry", "You Should Enter Every Detail")
        return None
    if not phone.isdigit():
        messagebox.showinfo(title="Error", message='Not a Valid Phone Number', parent=root)
        return None
    ctmid = DB.sqldb.get_customer_ID(phone)
    if ctmid is None:
        ctmid = DB.addcustomer(name, address, phone, "")
    else:
        dbcmname = DB.sqldb.get_cell("customers", "customer_id", "customer_name", ctmid)
        if dbcmname != name:
            messagebox.showinfo("Error", "Phone Number Already registerd in %s's Name" % dbcmname)
            return None
    return ctmid, name, address, phone


def make_sure_path_exist(path):
    import os
    filepath = os.getcwd()
    if not os.path.exists(filepath + "\\" + path):
        os.mkdir(filepath + "\\" + path)
    else:
        pass
    return 1


def a_d_d__product(id=False, modify=False):
    tup = []
    if not modify:
        titlel = "New Product"
    else:
        titlel = "Modify Product"
        index = mlb31.Select_index
        tup = mlb31.get(index)
        cur_item = mlb31.tree.focus()
        arg = mlb31.tree.item(cur_item)
        id = arg["values"][0]
        if index is None or index > mlb31.size():
            return messagebox.showinfo(title='Error', message='Nothing is Selected To Modify')
    root12 = tk.Toplevel(master=root)
    root12.title(titlel)
    root12.grid()
    root12.focus()
    root12.rowconfigure(0, weight=1)
    root12.columnconfigure(0, weight=1)
    np = NewProduct(root12, tup, modify, DB, id)
    np.grid(row=0, column=0, sticky=N + S + W + E)
    np.rowconfigure(0, weight=1)
    np.columnconfigure(0, weight=1)
    root12.wait_window()
    return b_product__search(refresh=True)


def a_d_d__customer(modify=False):
    tup = []
    if not modify:
        titlel = "New Customer"
    else:
        titlel = "Modify Customer"
        index = mlb41.Select_index
        if index is None or index > mlb41.size():
            return messagebox.showinfo('Error', 'Nothing is Selected To Modify')
        cur_item = mlb41.tree.focus()
        arg = mlb41.tree.item(cur_item)
        tup = arg["values"]
    root13 = tk.Toplevel(master=root)
    root13.title(titlel)
    root13.focus()
    root13.grid()
    root13.rowconfigure(0, weight=1)
    root13.columnconfigure(0, weight=1)
    nc = NewCustomer(root13, modify, tup, DB)
    nc.grid(row=0, column=0, sticky=N + W + S + E)
    nc.rowconfigure(0, weight=1)
    nc.columnconfigure(0, weight=1)
    root13.wait_window()
    return b_customer__search(refresh=True)


def call_save():
    """ this is called each time we quit the application """
    ans = messagebox.askokcancel("WARNING", "Do You Want To save All Changes")
    if ans:
        DB.save()
        root.destroy()
    else:
        root.destroy()


def cdmp_del():
    sapp = SampleApp(root, DB)
    sapp.load__de()


def add_supplier(id=False, modify=False):
    """ method that is called upon button call """
    tup = []
    if not modify:
        title = "New Supplier"
    else:
        title = "Modify Supplier"
        index = mlb51.Select_index
        piid = mlb51.true_parent(mlb51.Select_iid)
        index = mlb51.index(piid)
        tup = mlb51.get(index)
        cur_item = mlb51.tree.focus()
        arg = mlb51.tree.item(cur_item)
        id = arg["values"][0]
        if index is None or index > mlb51.size():
            return messagebox.showinfo("Error", "Nothing is selected to modify")
    root13 = tk.Toplevel(master=root)
    root13.title(title)
    root13.focus()
    root13.grid()
    root13.rowconfigure(0, weight=1)
    root13.columnconfigure(0, weight=1)
    ns = NewSupplier(root13, modify, tup, DB, id)
    ns.grid(row=0, column=0, sticky=N + W + S + E)
    ns.rowconfigure(0, weight=1)
    ns.columnconfigure(0, weight=1)
    root13.wait_window()
    return b_supplier_search(refresh=True)


def remove_supplier(mlb51):
    pass


invoice__date()
invoice_num()
b_product__search(refresh=True)
b_customer__search(refresh=True)
b_supplier_search(refresh=True)
make_sure_path_exist("invoice")
make_sure_path_exist("data")
root.protocol(name="WM_DELETE_WINDOW", func=call_save)

root.mainloop()