import sys
import os

from src.const import color, SEL_COLOR, FOREGROUND, saveico, NEW_ICO, SETTINGS_ICO, NEXT_ICO, \
    ncico, tmp, tmp2, genico, tmp4, tmp6, tmp7, tmp_modify, tmp_extra

try:
    import Tkinter as tk
except:
    import tkinter as tk
try:
    from tkinter.font import Font
except:
    import tkinter.font as tkFont

from tkinter.filedialog import askopenfilename, N, S, E, W, HORIZONTAL, asksaveasfilename
from tkinter.ttk import Style, Label, Frame, Combobox, Notebook, LabelFrame, Separator, Button, Entry, Spinbox, \
    Labelframe
from tkinter import DoubleVar, TOP, RIGHT, FLAT, LEFT, NORMAL, messagebox
import time as t

import PIL.Image
import PIL.ImageTk
from reportlab import xrange

from src.Cython.proWrd1 import Filter

import src.TableTree as tableTree
from src.Cato_Opt import Category
from src.NewCustomer import NewCustomer
from src.NewInvoice import ADDInvoice
from src.NewProduct import NewProduct
from src.NewSupplier import NewSupplier
from src.PdfGenarator import pdf_document, nir_document
from src.PurchaseLog import PurchaseLog
from src.buttoncalender import CalendarButton, WORD, END
from src.pcclass import InventoryDataBase
from src.scroll_frame import SampleApp
from src.UnitsOfMeasure import UnitsOfMeasure

# from src.Graph import Graph

# variable access by all

DB = InventoryDataBase()
var_string = ''
# Window

root = tk.Tk()
root.title("FitoGest")
# root.iconbitmap(ICON)
root.minsize(1024, 768)
root.grid()
root.rowconfigure(0, weight=1)
for h in range(12):
    root.columnconfigure(h, weight=1)
root.rowconfigure(2, weight=2)
root.wm_state('normal')
root['background'] = color

menubar = tk.Menu(root,
                  background=color,
                  activebackground=SEL_COLOR,
                  foreground=FOREGROUND,
                  activeforeground="#FFFFFF")
filemenu = tk.Menu(menubar,
                   tearoff=0,
                   background=color,
                   activebackground=SEL_COLOR,
                   foreground=FOREGROUND,
                   activeforeground="#FFFFFF")
editmenu = tk.Menu(menubar,
                   tearoff=0,
                   background=color,
                   activebackground=SEL_COLOR,
                   foreground=FOREGROUND,
                   activeforeground="#FFFFFF")
menubar.add_cascade(label="Fisier", menu=filemenu)
menubar.add_cascade(label="Editare", menu=editmenu)
filemenu.add_command(label="  Salvare modificari",
                     command=lambda: DB.Save(),
                     bitmap='info',
                     compound=LEFT)
filemenu.add_command(label="  Incarca o baza de date",
                     command=lambda: ask_db_file(),
                     bitmap='question',
                     compound=LEFT)
filemenu.add_command(label="  Iesire",
                     command=lambda: call_save(),
                     bitmap='error',
                     compound=LEFT)
editmenu.add_command(label="Detalii Firma",
                     command=lambda: cdmp_del(),
                     bitmap='info',
                     compound=LEFT)
editmenu.add_command(label="Resetare",
                     command=lambda: reset(),
                     bitmap='info',
                     compound=LEFT)
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
btnnote.grid(row=3, column=0, columnspan=8, sticky=N + S + E + W)
btnnote.columnconfigure(0, weight=1)
# btnnote.rowconfigure(0, weight=1)
saveico = PIL.Image.open(saveico).resize((32, 32), PIL.Image.ANTIALIAS)
saveico = PIL.ImageTk.PhotoImage(image=saveico)
Button(btnnote,
       text="Salvare",
       command=lambda: DB.save(),
       compound=TOP,
       image=saveico,
       width=15).grid(row=0, column=0, sticky=N + S + W + E)
npico = PIL.Image.open(NEW_ICO).resize((32, 32), PIL.Image.ANTIALIAS)
npico = PIL.ImageTk.PhotoImage(image=npico)
productbtn = Button(btnnote,
                    text="Produs Nou",
                    command=lambda: a_d_d__product(modify=False),
                    image=npico,
                    compound=TOP,
                    width=15).grid(row=0, column=1, sticky=N + S + W + E)
ncico = PIL.ImageTk.PhotoImage(image=ncico)
customerbtn = Button(btnnote,
                     text="Client nou",
                     command=lambda: a_d_d__customer(modify=False),
                     image=ncico,
                     compound=TOP,
                     width=15).grid(row=0, column=2, sticky=N + S + W + E)
setting_ico = PIL.Image.open(SETTINGS_ICO).resize((32, 32),
                                                  PIL.Image.ANTIALIAS)
setting_ico = PIL.ImageTk.PhotoImage(image=setting_ico)
Button(btnnote,
       text="Editare detalii firma",
       command=lambda: cdmp_del(),
       image=setting_ico,
       compound=TOP,
       width=18).grid(row=0, column=3, sticky=N + S + W + E)

app = Frame(note)
app.grid(row=0, column=0, sticky=N + S + E + W)
note.add(app, text='    Factura    ')

app.columnconfigure(0, weight=1)
app.rowconfigure(1, weight=1)
app.rowconfigure(2, weight=5)

Label(app,
      text="Creare facturi de iesire bunuri",
      foreground="#3496ff",
      font=('Berlin Sans FB Demi', 20),
      background="#323232").grid(row=0, column=0, sticky=N + S + E + W)

add_together = Frame(app)
add_together.grid(row=1, column=0, sticky=N + E + S + W)
add_together.rowconfigure(0, weight=1)

for h in range(3):
    add_together.columnconfigure(h, weight=1)

Lf01 = LabelFrame(add_together,
                  text="Optiuni clienti",
                  labelanchor=N,
                  style="r.TLabelframe",
                  width=2500)
Lf01.grid(row=0, column=0, sticky=N + E + S + W, padx=10, pady=10)
for h in range(3):
    Lf01.rowconfigure(h, weight=1)
for h in range(1, 2):
    Lf01.columnconfigure(h, weight=1)

# Customer name
lbl0 = Label(Lf01, text="Nume", anchor=E)
lbl0.grid(row=0, column=0, sticky=N + E + S + W, pady=10, padx=5)

customer_name = Combobox(Lf01,
                         postcommand=lambda: customer_name__search(),
                         width=35, height=10)
customer_name.grid(row=0, column=1, sticky=N + E + S + W, pady=8, padx=10)

# Phone

lbl3 = Label(Lf01, text="Telefon client", anchor=E)
lbl3.grid(row=1, column=0, sticky=N + E + S + W, pady=10, padx=5)

customer_phone = Entry(Lf01, justify=RIGHT)
customer_phone.grid(row=1, column=1, sticky=N + S + E + W, pady=10, padx=10)

# Address

lbl1 = Label(Lf01, text="Adresa", anchor=E)
lbl1.grid(row=2, column=0, sticky=N + E + W, pady=10, padx=5)

customer_address = tk.Text(Lf01, width=5, height=5, wrap=WORD, relief=FLAT)
customer_address.grid(row=2, column=1, sticky=N + E + S + W, pady=10, padx=10)
customer_address.configure(highlightthickness=1,
                           highlightbackground="Grey",
                           relief=FLAT)

#       Product name
Lf02 = LabelFrame(add_together, text="Optiuni produs", labelanchor=N)
Lf02.grid(row=0, column=1, sticky=N + E + S + W, padx=5, pady=10)
Lf02.columnconfigure(1, weight=1)
for h in range(5):
    Lf02.rowconfigure(h, weight=1)

lbl6 = Label(Lf02, text="Nume", anchor=E)
lbl6.grid(row=0, column=0, sticky=N + E + S + W, padx=5, pady=10)

product_name = Combobox(Lf02,
                        postcommand=lambda: product_name__search(),
                        width=40, height=10)
product_name.grid(row=0, column=1, sticky=N + E + W + S, padx=5, pady=10)

# Product Detail
lbl8 = Label(Lf02, text="Descriere")
lbl8.grid(row=1, column=0, sticky=N + E, padx=5, pady=10)

product_detail = tk.Text(Lf02, width=4, height=2, wrap=WORD, relief=FLAT)
product_detail.grid(row=1,
                    column=1,
                    rowspan=2,
                    sticky=N + E + S + W,
                    pady=10,
                    padx=5)
product_detail.configure(highlightthickness=1,
                         highlightbackground="Grey",
                         relief=FLAT)

# QTY
lbl11 = Label(Lf02, text="Cantitate")
lbl11.grid(row=3, column=0, sticky=N + E, padx=5, pady=10)

quantity = Entry(Lf02, justify=RIGHT)
quantity.grid(row=3, column=1, sticky=N + E + S + W, padx=5, pady=10)

# Product Price

lbl9 = Label(Lf02, text="Pret Unitar")
lbl9.grid(row=4, column=0, sticky=N + E, padx=5, pady=10)

product_price = Entry(Lf02, justify=RIGHT)
product_price.grid(row=4, column=1, sticky=N + E + S + W, padx=5, pady=10)

lbl10 = Label(Lf02, text="Lot")
lbl10.grid(row=5, column=0, sticky=N + E, padx=5, pady=10)


def lot_search():
    if product_name.get() == '':
        return messagebox.showerror('Eroare produs',
                                    'Alege un produs de mai sus pentru a vedea in ce loturi este prins', parent=root)
    lots = DB.sqldb.get_lots_for_product(product_name.get())
    for i in lots:
        # variants_combo['values'] = (*variants_combo['values'], v[1])

        lot["values"] = (*lot["values"], i[1])
        var_combo["values"] = (*var_combo["values"], i[7])


lot = Combobox(Lf02, postcommand=lambda: lot_search(), width=40)
lot.grid(row=5, column=1, sticky=N + E, padx=5, pady=10)

var_label = Label(Lf02, text="Variante")
var_label.grid(row=6, column=0, sticky=N + E, padx=5, pady=10)

var_combo = Combobox(Lf02, width=40)
var_combo.grid(row=6, column=1, sticky=N + E, padx=5, pady=10)

# invoice option

Lf04 = LabelFrame(add_together, text="Optiuni factura", labelanchor=N)
Lf04.grid(row=0, column=2, sticky=N + E + S + W, padx=5, pady=10)
Lf04.columnconfigure(1, weight=1)
for h in range(1, 10):
    Lf04.rowconfigure(h, weight=1)
# Invoice Date

Label(Lf04, text="Data facturare", anchor=N + W).grid(row=0,
                                                      column=0,
                                                      sticky=N + E + W + S,
                                                      padx=0,
                                                      pady=0)

invoice_date = CalendarButton(Lf04)
invoice_date.grid(row=1,
                  column=0,
                  columnspan=2,
                  sticky=N + E + S + W,
                  padx=5,
                  pady=0)

# Invoice Number
Label(Lf04, text="Numar factura", anchor=N + W).grid(row=2,
                                                     column=0,
                                                     sticky=N + E + W + S,
                                                     padx=5,
                                                     pady=5)

invoice_number = Spinbox(Lf04, from_=0, to=10000, increment=1.0, wrap=True)
invoice_number.grid(row=2, column=1, sticky=N + E + W + S, padx=5, pady=5)
# +- Button

Cartindeldbnfram = Frame(Lf04)
Cartindeldbnfram.grid(row=9,
                      column=0,
                      columnspan=2,
                      sticky=E + W + N + S,
                      padx=0,
                      pady=0)
Cartindeldbnfram.rowconfigure(0, weight=1)
Cartindeldbnfram.columnconfigure(0, weight=1)
Cartindeldbnfram.columnconfigure(1, weight=1)
tmp = PIL.ImageTk.PhotoImage(image=tmp)
Button(Cartindeldbnfram,
       text="Adaugare in cos",
       image=tmp,
       compound=LEFT,
       command=lambda: add_2_cart()).grid(row=0,
                                          column=0,
                                          sticky=E + W + N + S,
                                          padx=5,
                                          pady=5)
tmp2 = PIL.ImageTk.PhotoImage(image=tmp2)
Button(Cartindeldbnfram,
       text="Stergere din cos",
       image=tmp2,
       compound=LEFT,
       command=lambda: remove_from_cart()).grid(row=0,
                                                column=1,
                                                sticky=E + W + N + S,
                                                padx=5,
                                                pady=5)

# side

dframe = Frame(app)
dframe.grid(row=2, column=0, rowspan=9, sticky=N + S + E + W)
dframe.columnconfigure(0, weight=1)
dframe.rowconfigure(0, weight=2)

# Amount
Lf03 = LabelFrame(dframe, text="Optiuni incasare", labelanchor=N)
Lf03.grid(row=0, column=1, sticky=N + E + S + W)

Fon = Font(family='Times', size=17)
Fon1 = Font(family='Times', size=14)

# AMOUNT

lbl27 = Label(Lf03, text="Suma :", font=Fon1)
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


def tax_update(a, b, c):
    """ UPDATE TAX """
    sgst_var.set(round(get_sgst() * (Amt_var.get() / 100), 2))
    cgst_var.set(round(get_cgst() * (Amt_var.get() / 100), 2))
    subtol_var.set(round(sgst_var.get() + cgst_var.get() + Amt_var.get(), 2))
    entry20.delete(0, END)
    entry20.insert(0, str(subtol_var.get()))
    Discount_var.set(0.0)
    Gtol_var.set(subtol_var.get())


# DONE Amt_var is empty
Amt_var.trace('w', tax_update)

Label(Lf03, text="Adaos @ " + str(get_sgst()) + "% : ",
      font=Fon1).grid(row=1, column=0, sticky=E + N + S, padx=10, pady=10)

sgst_var = tk.DoubleVar()

sgst = Label(Lf03, font=Fon1, textvariable=sgst_var)
sgst.grid(row=1, column=1, sticky=N + E + S + W, padx=10, pady=10)

Label(Lf03, text="TVA @ " + str(get_cgst()) + "% : ",
      font=Fon1).grid(row=2, column=0, sticky=E + N + S, padx=10, pady=10)

cgst_var = tk.DoubleVar()

cgst = Label(Lf03, font=Fon1, textvariable=cgst_var)
cgst.grid(row=2, column=1, sticky=N + E + S + W, padx=10, pady=10)

Separator(Lf03, orient=HORIZONTAL).grid(row=3,
                                        column=0,
                                        columnspan=2,
                                        sticky="ew",
                                        padx=8,
                                        pady=4)

# subtotal

Label(Lf03, text="Sub Total :", font=Fon1).grid(row=4,
                                                column=0,
                                                sticky=E + N + S,
                                                padx=10,
                                                pady=10)
subtol_var = tk.DoubleVar()
Label(Lf03, font=Fon1, textvariable=subtol_var).grid(row=4,
                                                     column=1,
                                                     sticky=W + N + S,
                                                     padx=10,
                                                     pady=10)

# Paid

lbl20 = Label(Lf03, text="De plata :", font=Fon1)
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

Separator(Lf03, orient=HORIZONTAL).grid(row=7,
                                        column=0,
                                        columnspan=2,
                                        sticky="ew",
                                        padx=8,
                                        pady=4)

lbl25 = Label(Lf03, text="Total:", font=Fon)
lbl25.grid(row=8, column=0, sticky=E + N + S, padx=10, pady=10)

Gtol_var = DoubleVar()

Gtol = Label(Lf03, font=Fon, textvariable=Gtol_var, width=10)
Gtol.grid(row=8, column=1, sticky=N + E + S + W, padx=10, pady=10)

# Generate
genico = PIL.ImageTk.PhotoImage(image=genico)

butn_Gen = Button(Lf03,
                  text="Generare factura",
                  command=lambda: transfer(),
                  image=genico,
                  compound=LEFT)
butn_Gen.grid(row=9,
              column=0,
              columnspan=2,
              sticky=E + W + S + N,
              pady=10,
              padx=8)

# Table

mlb = tableTree.MultiListbox(dframe, (("ID Pret", 20), ('Produs', 35),
                                      ('Descriere', 45), ("Cantitate", 6),
                                      ("Pret Unitar", 9), ("LOT", 35), ("Varianta", 40)))
mlb.grid(row=0, column=0, sticky=N + S + E + W, padx=10)


def supplier_keys():
    """

    @return:
    """

    return DB.get_supplier_names


def purchase_product_frame():
    """ Build the Purchase frame """
    global product_name_search, qty_text, cost_price_text, btn64, selling_price_text, tmp4, tmp5, category_combo, \
        description_text, product_purchase_listbox, supplier_combo_search_purchase, pentru_factura, lot_text, app6, \
        discount_text, tva_entry, btn66, variants_frame
    #     note purchase product
    upf = Frame(note)
    upf.grid(row=0, column=0, sticky=N + W + S + E)
    note.add(upf, text="    Achizitii    ")
    upf.columnconfigure(0, weight=1)
    upf.rowconfigure(1, weight=1)
    Label(upf,
          text="Achizitie Produse",
          foreground="#3496ff",
          font=('Berlin Sans FB Demi', 20)).grid(row=0,
                                                 column=0,
                                                 sticky=N + S + E + W)
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
    Label(lfp, text="Nume").grid(row=1, column=0, sticky=E, padx=10, pady=5)
    product_name_search = Combobox(lfp,
                                   postcommand=lambda: product_entry_search())
    product_name_search.grid(row=1, column=1, sticky=W + E, padx=10, pady=5)
    Label(lfp, text="Cantitate").grid(row=3,
                                      column=0,
                                      sticky=E,
                                      padx=10,
                                      pady=5)
    qty_text = Entry(lfp)
    qty_text.grid(row=3, column=1, sticky=W + E, padx=10, pady=5)
    Label(lfp, text="Pret Achizitie").grid(row=5,
                                           column=0,
                                           sticky=E,
                                           padx=10,
                                           pady=5)
    cost_price_text = Entry(lfp)
    cost_price_text.grid(row=5, column=1, sticky=W + E, padx=10, pady=5)
    Label(lfp, text="Data achizitie").grid(row=1,
                                           column=2,
                                           sticky=E,
                                           padx=10,
                                           pady=5)
    btn64 = CalendarButton(lfp)
    btn64.grid(row=1, column=3, sticky=W + E + S + N, padx=10, pady=5)
    Label(lfp, text="Pret comercializare").grid(row=3,
                                                column=2,
                                                sticky=E,
                                                padx=10,
                                                pady=5)
    selling_price_text = Entry(lfp)
    selling_price_text.grid(row=3, column=3, sticky=W + E, padx=10, pady=5)
    variants_frame = Frame(lfp)
    variants_frame.grid(row=0, column=0, sticky=N + E + S + W, padx=0, pady=0, columnspan=6)
    variants_frame.rowconfigure(0, weight=1)
    variants_frame.columnconfigure(1, weight=1)
    editbtnfram = Frame(lfp)
    editbtnfram.grid(row=10, column=3, sticky=N + E + S + W, padx=0, pady=0, columnspan=3)
    editbtnfram.rowconfigure(0, weight=1)
    editbtnfram.columnconfigure(0, weight=1)
    editbtnfram.columnconfigure(1, weight=1)
    tmp4 = PIL.ImageTk.PhotoImage(image=tmp4)
    Button(editbtnfram,
           text="Adaugare",
           image=tmp4,
           compound=LEFT,
           command=lambda: add_to_purchase_table()).grid(row=0,
                                                         column=0,
                                                         sticky=N + E + S + W,
                                                         padx=10,
                                                         pady=5)
    SYMBOL_REMOVE = os.path.normpath('data/symbol_remove.png')
    tmp5 = PIL.Image.open(SYMBOL_REMOVE).resize((25, 25), PIL.Image.ANTIALIAS)
    tmp5 = PIL.ImageTk.PhotoImage(image=tmp5)
    Button(editbtnfram,
           text="Stergere",
           image=tmp5,
           compound=LEFT,
           command=lambda: delete_from_purchase_table()).grid(row=0,
                                                              column=1,
                                                              sticky=N + W +
                                                                     S + E,
                                                              padx=10,
                                                              pady=5)
    btn65 = Button(editbtnfram,
                   text=" Jurnal achizitii",
                   width=20,
                   command=lambda: ipurlog())
    btn65.grid(row=0, column=2, sticky=N + S + E + W, padx=10, pady=5)
    Label(lfp, text="Categorie ").grid(row=1,
                                       column=4,
                                       sticky=E,
                                       padx=10,
                                       pady=5)
    category_combo = Combobox(lfp, postcommand=lambda: ckeys())
    category_combo.grid(row=1, column=5, sticky=W + E, padx=10, pady=5)
    Label(lfp, text="Descriere").grid(row=3,
                                      column=4,
                                      sticky=E + N,
                                      padx=10,
                                      pady=5)
    description_text = tk.Text(lfp, width=0, height=2, wrap=WORD, relief=FLAT)
    description_text.grid(row=3,
                          column=5,
                          rowspan=3,
                          sticky=W + E + N + S,
                          padx=10,
                          pady=5)
    description_text.configure(highlightthickness=1,
                               highlightbackground="Grey",
                               relief=FLAT)
    Label(lfp, text="Pentru factura").grid(row=6,
                                           column=0,
                                           sticky=E,
                                           padx=5,
                                           pady=5)
    pentru_factura = Entry(lfp)
    pentru_factura.grid(row=6, column=1, sticky=W + E, padx=5, pady=5)
    Label(lfp, text="Furnizor").grid(row=5,
                                     column=2,
                                     sticky=E,
                                     padx=10,
                                     pady=5)
    supplier_combo_search_purchase = Combobox(
        lfp, values=supplier_keys(), postcommand=lambda: supplier_keys())
    supplier_combo_search_purchase.grid(row=5,
                                        column=3,
                                        sticky=N + E + W + S,
                                        padx=10,
                                        pady=10)
    Label(lfp, text="LOT   ").grid(row=6, column=4, sticky=E, padx=10, pady=5)
    lot_text = Entry(lfp)
    lot_text.grid(row=6, column=5, sticky=W + E, padx=10, pady=5)
    Label(lfp, text="Discount").grid(row=7, column=0, sticky=E, padx=10, pady=5)
    discount_text = Entry(lfp)
    discount_text.grid(row=7, column=1, sticky=W + E, padx=10, pady=5)
    Label(lfp, text="TVA").grid(row=6, column=2, sticky=W + E, padx=10, pady=5)
    tva_entry = Entry(lfp)
    tva_entry.grid(row=6, column=3, sticky=W + E, padx=10, pady=5)
    Label(lfp, text="Data expirare").grid(row=7, column=2, sticky=W + E, padx=10, pady=5)
    btn66 = CalendarButton(lfp)
    btn66.grid(row=7, column=3, sticky=W + E, padx=10, pady=5)
    product_purchase_listbox = tableTree.MultiListbox(
        app6, (('Nume produs', 35), ("UM", 10), ("Pret achizitie", 25),
               ("Pret comercializare", 25), ("Cantitate", 15), ("Data", 35),
               ("LOT", 25), ("Pentru factura", 35), ('Furnizor', 20), ("Discount", 8), ("Expira pe", 21),
               ('Varianta', 21)))
    product_purchase_listbox.grid(row=3, column=0, columnspan=1, rowspan=3, sticky=N + S + E + W)
    tmp3 = PIL.Image.open(NEXT_ICO).resize((70, 70), PIL.Image.ANTIALIAS)
    tmp3 = PIL.ImageTk.PhotoImage(image=tmp3)
    btn62 = Button(app6,
                   text="Terminare achizitie",
                   width=35,
                   image=tmp3,
                   compound=LEFT,
                   command=lambda: add_to_inventory())
    btn62.grid(row=8, column=0, sticky=N + E + S, pady=10)


purchase_product_frame()


def inventory_product_list():
    """ Inventory frame """
    global h, product_search, tmp6, tmp7, tmp_modify, tmp_extra, uom_opt_event, inventory_products_listbox
    # page 3
    # frame 3
    app2 = Frame(note)
    app2.grid(row=0, column=0)
    app2.columnconfigure(0, weight=1)
    app2.columnconfigure(1, weight=7)
    app2.rowconfigure(2, weight=1)
    note.add(app2, text='    Inventar    ')
    Label(app2,
          text='Produse inventar',
          foreground="#3496ff",
          font=('Berlin Sans FB Demi', 20)).grid(row=0,
                                                 column=0,
                                                 columnspan=2,
                                                 sticky=E + N + W + S,
                                                 padx=10,
                                                 pady=0)
    app2sub2 = Frame(app2)
    app2sub2.grid(row=1, column=0, sticky=N + S + W + E, padx=5, pady=0)
    app2sub2.columnconfigure(1, weight=1)
    app2sub2.columnconfigure(0, weight=5)
    app2sub2.rowconfigure(0, weight=1)
    lf3 = LabelFrame(app2sub2, text="Optiuni cautare produs")
    lf3.grid(row=0, column=0, sticky=N + S + W + E, padx=2, pady=10)
    for h in xrange(1, 3):
        lf3.columnconfigure(h, weight=1)
    for h in xrange(2):
        lf3.rowconfigure(h, weight=1)
    Label(lf3, text="Termen de cautare").grid(row=0,
                                              column=0,
                                              sticky=N + W + S + E,
                                              padx=5,
                                              pady=7)
    product_search = Combobox(lf3,
                              width=35,
                              postcommand=lambda: product__search())
    product_search.grid(row=0,
                        column=1,
                        columnspan=2,
                        sticky=N + W + S + E,
                        padx=5,
                        pady=7)
    tmp6 = PIL.ImageTk.PhotoImage(image=tmp6)
    Button(lf3,
           text="Cautare",
           width=15,
           image=tmp6,
           command=lambda: b_product__search()).grid(row=1,
                                                     column=1,
                                                     sticky=N + W + S + E,
                                                     padx=5,
                                                     pady=5)
    tmp7 = PIL.ImageTk.PhotoImage(image=tmp7)
    Button(lf3,
           text="Reincarcare",
           width=15,
           image=tmp7,
           command=lambda: b_product__search(refresh=True)).grid(row=1,
                                                                 column=2,
                                                                 sticky=N + W +
                                                                        S + E,
                                                                 padx=5,
                                                                 pady=5)
    lf31 = LabelFrame(app2sub2, text="Optiuni Editare Produs")
    lf31.grid(row=0, column=1, sticky=N + W + S + E, padx=2, pady=10)
    for h in range(2):
        lf31.columnconfigure(h, weight=1)
    for h in range(2):
        lf31.rowconfigure(h, weight=1)
    Button(lf31,
           text="Adaugare Produs",
           image=tmp4,
           compound=LEFT,
           command=lambda: a_d_d__product(),
           width=20).grid(row=0,
                          column=0,
                          sticky=N + W + E + S,
                          padx=5,
                          pady=5)
    Button(lf31,
           text="Stergere Produs",
           image=tmp5,
           compound=LEFT,
           command=lambda: remove__product(inventory_products_listbox),
           width=20).grid(row=0,
                          column=1,
                          sticky=N + W + S + E,
                          padx=5,
                          pady=5)

    tmp_modify = PIL.ImageTk.PhotoImage(image=tmp_modify)
    Button(lf31,
           text="Modificare Produs",
           image=tmp_modify,
           compound=LEFT,
           command=lambda: a_d_d__product(modify=True),
           width=20).grid(row=1,
                          column=0,
                          sticky=N + W + S + E,
                          padx=5,
                          pady=5)
    tmp_extra = PIL.ImageTk.PhotoImage(image=tmp_extra)
    Button(lf31,
           text="Optiuni Categorie",
           image=tmp_extra,
           compound=LEFT,
           command=lambda: category_opt_event(),
           width=20).grid(row=1,
                          column=1,
                          sticky=N + W + S + E,
                          padx=5,
                          pady=5)

    def uom_opt_event():
        rootd = tk.Toplevel(master=root)
        rootd.title("Optiuni UM")
        rootd.columnconfigure(0, weight=1)
        rootd.rowconfigure(0, weight=1)
        UnitsOfMeasure(rootd, DB)
        rootd.wait_window()
        return True

    Button(lf31,
           text="Unitati de masura",
           image=tmp_extra,
           compound=LEFT,
           command=lambda: uom_opt_event(),
           width=20).grid(row=2,
                          column=0,
                          sticky=N + W + S + E,
                          padx=5,
                          pady=5)
    inventory_products_listbox = tableTree.MultiListbox(
        app2, (('ID', 5), ('Nume', 45), ('Categorie', 25), ('Descriere', 65),
               ("Unitate de masura", 10), ("Cantitate", 10)))
    inventory_products_listbox.grid(row=2, column=0, columnspan=2, sticky=N + S + E + W)


inventory_product_list()


# page 4
# listing


def customer_database_list():
    """ Customer listing """
    global h, customer_search, customer_listbox
    app3 = Frame(note)
    app3.grid(row=0, column=0)
    app3.columnconfigure(0, weight=1)
    app3.columnconfigure(1, weight=5)
    app3.rowconfigure(2, weight=1)
    note.add(app3, text="    Clienti    ")
    Label(app3,
          text='Lista clienti',
          foreground="#3496ff",
          font=('Berlin Sans FB Demi', 20)).grid(row=0,
                                                 column=0,
                                                 columnspan=2,
                                                 sticky=E + N + W + S,
                                                 padx=10,
                                                 pady=0)
    df = Frame(app3)
    df.grid(row=1, column=0, sticky=N + S + W + E)
    df.columnconfigure(0, weight=5)
    df.columnconfigure(1, weight=1)
    lf41 = LabelFrame(df, text="Optiuni Cautare Clienti")
    lf41.grid(row=0, column=0, sticky=N + S + W + E, padx=2, pady=0)
    lf41.columnconfigure(1, weight=1)
    lf41.columnconfigure(2, weight=1)
    for h in xrange(2):
        lf41.rowconfigure(h, weight=1)
    Label(lf41, text="Termen de cautare").grid(row=0,
                                               column=0,
                                               sticky=N + S + E,
                                               padx=5,
                                               pady=5)
    customer_search = Combobox(lf41,
                               postcommand=lambda: customer__search(),
                               width=35)
    customer_search.grid(row=0,
                         column=1,
                         columnspan=2,
                         sticky=N + W + S + E,
                         padx=5,
                         pady=5)
    Button(lf41,
           text="Cauta",
           width=15,
           image=tmp6,
           command=lambda: b_customer__search()).grid(row=1,
                                                      column=1,
                                                      sticky=N + W + S + E,
                                                      padx=5,
                                                      pady=5)
    Button(lf41,
           text="Reincarcare",
           width=15,
           image=tmp7,
           command=lambda: b_customer__search(refresh=True)).grid(row=1,
                                                                  column=2,
                                                                  sticky=N +
                                                                         W + S + E,
                                                                  padx=5,
                                                                  pady=5)
    lf42 = LabelFrame(df, text="Optiuni Editare Clienti")
    lf42.grid(row=0, column=1, sticky=N + W + S + E, padx=2, pady=0)
    lf42.columnconfigure(0, weight=1)
    lf42.columnconfigure(1, weight=1)
    for h in xrange(2):
        lf42.rowconfigure(h, weight=1)
    Button(lf42,
           text="Adaugare Client",
           width=20,
           image=tmp4,
           compound=LEFT,
           command=lambda: a_d_d__customer()).grid(row=0,
                                                   column=0,
                                                   sticky=N + W + S + E,
                                                   padx=5,
                                                   pady=5)
    Button(lf42,
           text="Stergere Client",
           width=20,
           image=tmp5,
           compound=LEFT,
           command=lambda: remove__customer(customer_listbox)).grid(row=0,
                                                                    column=1,
                                                                    sticky=N + W + S + E,
                                                                    padx=5,
                                                                    pady=5)
    Button(lf42,
           text="Modificare Client",
           width=20,
           image=tmp_modify,
           compound=LEFT,
           command=lambda: a_d_d__customer(modify=True)).grid(row=1,
                                                              column=0,
                                                              sticky=N + W +
                                                                     E + S,
                                                              padx=5,
                                                              pady=5)
    Button(lf42,
           text="Optiuni Facturare",
           width=20,
           image=tmp_extra,
           compound=LEFT,
           command=lambda: invoice_opt_event()).grid(row=1,
                                                     column=1,
                                                     sticky=N + W + E + S,
                                                     padx=5,
                                                     pady=5)
    customer_listbox = tableTree.MultiListbox(app3, (('ID', 5), ('Nume Client', 40),
                                                     ('Telefon', 15), ('Adresa', 70),
                                                     ("Email", 30)))
    customer_listbox.grid(row=2, column=0, columnspan=2, sticky=N + S + E + W, pady=10)


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
    note.add(app4, text="    Importuri si Exporturi    ")
    Label(app4,
          text='Importare si Exportare CSV',
          foreground="#3496ff",
          font=('Berlin Sans FB Demi', 20)).grid(row=0,
                                                 column=0,
                                                 sticky=E + N + W + S,
                                                 padx=10,
                                                 pady=0)
    lf2 = LabelFrame(app4, text="Optiuni Importare")
    lf2.grid(row=2,
             column=0,
             rowspan=5,
             columnspan=6,
             sticky=N + W + S + E,
             padx=10,
             pady=10)
    for h in range(7):
        lf2.columnconfigure(h, weight=1)
    lbl54 = Label(lf2, text="Importare lista de produse din")
    lbl54.grid(row=2, column=1, sticky=N + E + S + W, padx=10, pady=10)
    entry51 = Entry(lf2, width=35)
    entry51.grid(row=2,
                 column=2,
                 columnspan=2,
                 sticky=N + E + S + W,
                 padx=10,
                 pady=10)
    btn51 = Button(lf2, text="Rasfoire", command=lambda: brow__file(entry51))
    btn51.grid(row=2, column=5, sticky=N + E + S + W, padx=10, pady=10)
    C51 = tk.Canvas(app4, width=350, height=350, bg="White")
    C51.grid(row=2,
             rowspan=15,
             column=8,
             columnspan=15,
             sticky=N + E + W + S,
             padx=10,
             pady=10)
    Fon3 = Font(family='Times', size=24)
    Fon4 = Font(family='Times', size=16)
    lbl58 = Label(lf2, text="Importa Lista de Clienti din   ")
    lbl58.grid(row=4, column=1, sticky=N + E + S + W, padx=10, pady=10)
    entry52 = Entry(lf2, width=35)
    entry52.grid(row=4,
                 column=2,
                 columnspan=2,
                 sticky=N + E + S + W,
                 padx=10,
                 pady=10)
    btn52 = Button(lf2, text="Rasfoire", command=lambda: brow__file(entry52))
    btn52.grid(row=4, column=5, sticky=N + E + S + W, padx=10, pady=10)
    btn55 = Button(lf2,
                   text="Imporare",
                   command=lambda: import_csv(entry51.get(), entry52.get()))
    btn55.grid(row=6,
               column=4,
               columnspan=2,
               sticky=N + E + S + W,
               padx=10,
               pady=10)
    # LabelFrame Export Option
    lf1 = LabelFrame(app4, text="Optiuni Export")
    lf1.grid(row=8,
             column=0,
             rowspan=9,
             columnspan=6,
             sticky=N + W + S + E,
             padx=10,
             pady=10)
    for h in range(7):
        lf1.columnconfigure(h, weight=1)
    lbl511 = Label(lf1, text="Exportare in Dosar")
    lbl511.grid(row=8, column=1, sticky=N + E + S + W, padx=10, pady=10)
    entry53 = Entry(lf1, width=35)
    entry53.grid(row=8,
                 column=2,
                 columnspan=2,
                 sticky=N + E + S + W,
                 padx=10,
                 pady=10)
    btn53 = Button(lf1,
                   text="Alegere Fisier",
                   command=lambda: save__as__file(entry53))
    btn53.grid(row=8, column=5, sticky=N + E + S + W, padx=10, pady=10)
    btn55 = Button(lf1, text="Export", command=lambda: export(entry53))
    btn55.grid(row=12,
               column=4,
               columnspan=2,
               sticky=N + E + S + W,
               padx=10,
               pady=10)


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
    note.add(app5, text="    Furnizori    ")
    Label(app5,
          text='Management Furnizori',
          foreground="#3496ff",
          font=('Berlin Sans FB Demi', 20)).grid(row=0,
                                                 column=0,
                                                 sticky=E + N + W + S,
                                                 padx=10,
                                                 pady=0)
    ef = Frame(app5)
    ef.grid(row=1, column=0, sticky=N + S + W + E)
    ef.columnconfigure(0, weight=5)
    ef.columnconfigure(1, weight=1)
    lf51 = LabelFrame(ef, text="Optiuni cautare furnizori")
    lf51.grid(row=0, column=0, sticky=N + S + W + E, padx=2, pady=0)
    lf51.columnconfigure(1, weight=1)
    lf51.columnconfigure(2, weight=1)
    for h in xrange(2):
        lf51.rowconfigure(h, weight=1)
    Label(lf51, text="Termen de cautare").grid(row=0,
                                               column=0,
                                               sticky=N + S + E,
                                               padx=5,
                                               pady=5)
    supplier_combo_search = Combobox(lf51,
                                     postcommand=lambda: supplier_search(),
                                     width=35)
    supplier_combo_search.grid(row=0,
                               column=1,
                               columnspan=2,
                               sticky=N + W + S + E,
                               padx=5,
                               pady=5)
    Button(lf51,
           text="Cauta",
           width=15,
           image=tmp6,
           command=lambda: b_supplier_search()).grid(row=1,
                                                     column=1,
                                                     sticky=N + W + S + E,
                                                     padx=5,
                                                     pady=5)
    Button(lf51,
           text="Reincarcare",
           width=15,
           image=tmp7,
           command=lambda: b_supplier_search(refresh=True)).grid(row=1,
                                                                 column=2,
                                                                 sticky=N + W +
                                                                        S + E,
                                                                 padx=5,
                                                                 pady=5)
    lf52 = Labelframe(ef, text="Optiuni editare Furnizori")
    lf52.grid(row=0, column=1, sticky=N + W + S + E, padx=2, pady=0)
    lf52.columnconfigure(0, weight=1)
    lf52.rowconfigure(0, weight=1)
    for h in xrange(2):
        lf52.rowconfigure(h, weight=1)
    Button(lf52,
           text="Adaugare Furnizor",
           width=20,
           image=tmp4,
           compound=LEFT,
           command=lambda: add_supplier()).grid(row=0,
                                                column=0,
                                                sticky=N + W + S + E,
                                                padx=5,
                                                pady=5)
    Button(lf52,
           text="Stergere furnizor",
           width=20,
           image=tmp5,
           compound=LEFT,
           command=lambda: remove_supplier(mlb51)).grid(row=0,
                                                        column=1,
                                                        sticky=N + W + S + E,
                                                        padx=5,
                                                        pady=5)
    Button(lf52,
           text="Modificare furnizor",
           width=20,
           image=tmp_modify,
           compound=LEFT,
           command=lambda: add_supplier(modify=True)).grid(row=1,
                                                           column=0,
                                                           sticky=N + W + E +
                                                                  S,
                                                           padx=5,
                                                           pady=5)
    mlb51 = tableTree.MultiListbox(app5, (("ID", 5), ("Nume", 40), ("RO", 12),
                                          ("Adresa", 70)))
    mlb51.grid(row=2, column=0, columnspan=2, sticky=N + S + E + W, pady=10)


suppliers_frame()


# from Graph import Graph

# app72 = Graph(note, 'RON', DB)
# app72.grid(row=0, column=0, sticky=N + S + E + W)
# note.add(app72, text='    Statistics   ')
# app72.columnconfigure(0, weight=6)
# app72.columnconfigure(1, weight=1)
# app72.rowconfigure(0, weight=1)


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
        tup = DB.sqldb.execute(
            """ select id, name, ro, address from suppliers""").fetchall()
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
    global variants_options_combo, variants_options, variants_combo
    """

    @param event:
    @return:
    """
    inp = str(product_name_search.get())
    l = DB.sqldb.get_products(inp.title())
    product_variants_options_for_product(inp)
    if l is None:
        l = DB.sqldb.get_products_if_first_is_none(inp.title())
        product_variants_options_for_product(inp)
        category = l[0]
        des = l[1]
        cost = l[2]
        price = l[3]
        tva = l[7]
        qty_text.delete(0, END)
        qty_text.insert(0, "1.0")
        category_combo.delete(0, END)
        description_text.delete(0.0, END)
        category_combo.insert(0, str(category))
        description_text.insert(0.0, str(des))
        cost_price_text.delete(0, END)
        cost_price_text.insert(0, str(cost))
        selling_price_text.delete(0, END)
        selling_price_text.insert(0, str(price))
        tva_entry.delete(0, END)
        tva_entry.insert(0, str(tva))
        return 1
    cost = l[0]
    price = l[1]
    category = l[2]
    des = l[3]
    tva = l[7]
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
    tva_entry.delete(0, END)
    tva_entry.insert(0, str(tva))
    tva_entry.configure(state='readonly')
    cost_price_text.configure(state="readonly")
    selling_price_text.configure(state="readonly")


def make_dict(event):
    """

    @param event
    """
    global var_string
    if var_string != '':
        var_string += ':' + event.widget.get()
    else:
        var_string = event.widget.get()


def product_variants_options_for_product(inp):
    """

    @param inp
    """
    global variants_combo, variant_var, var_string
    var_string = ''
    variants = DB.sqldb.execute(
        """ select * from product_variants where product_id = "%s" """ % DB.sqldb.get_product_id(
            inp.title())).fetchall()
    if variants:
        for j, i in enumerate(variants):
            options = DB.sqldb.execute(
                """ select * from variants_options where variant_id = "%s" """ % i[0]).fetchall()
            # variants_frame adaugare la variants_frame
            label = Label(variants_frame, text=str(i[1])).grid(row=j, column=1, sticky=N + E + S + W, padx=5, pady=10)
            variants_combo = Combobox(variants_frame, width=40)
            variants_combo.grid(row=j, column=1, sticky=N + E + S + E, padx=5, pady=10)
            variants_combo.bind('<<ComboboxSelected>>', make_dict)
            for v in options:
                variants_combo['values'] = (*variants_combo['values'], v[1])


def get_um_for_product(pid):
    """

    @param pid:
    @return:
    """
    return DB.sqldb.get_um_for_product(pid)


def add_to_purchase_table():
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
    discount = Filter(discount_text.get()).title()
    if discount == '':
        discount = 0.0
    supplier = Filter(supplier_combo_search_purchase.get()).title()
    for_invoice = Filter(pentru_factura.get()).title()
    expiry_date = Filter(btn66.get()).title()
    if len(qty.split()) == 0:
        return messagebox.showinfo("Eroare",
                                   "Cantitatea introdusa este invalida",
                                   parent=root)
    if len(date.split()) == 0:
        return messagebox.showinfo("Eroare",
                                   "Data introdusa nu este buna",
                                   parent=root)
    if len(cat.split()) == 0:
        return messagebox.showinfo("Eroare",
                                   "Categoria introdusa nu este valida",
                                   parent=root)
    if len(cost.split()) == 0:
        return messagebox.showinfo(
            title="Eroare",
            message='Pretul de achizitie trebuie specificat',
            parent=root)
    if len(price.split()) == 0:
        price = cost
    try:
        price = float(price)
        cost = float(cost)
        qty = float(qty)
    except ValueError:
        return messagebox.showinfo(
            title="Eroare",
            message=
            'Cantitatea, pretul de achizitie sau cel de vanzare trebuie sa fie formate numerice',
            parent=root)
    pid = DB.sqldb.get_product_id(name)
    if pid is None:
        aut = messagebox.askokcancel(
            "Autentificare",
            "Produsul nu se afla in lista de produse \nVrei sa-l adaug ?",
            parent=root)
        if not aut:
            return 0
        pid = DB.add_product(name, cat, des)
    costid = DB.sqldb.get_cost_id(pid, lot, cost, price)
    if costid is None:
        DB.add_cost(name, lot, cost, price)
    um = get_um_for_product(pid)[1]
    varianta = var_string
    cost = round(float(cost) - (float(cost) * (float(discount) / 100)), 2)
    price = round(float(price) - (float(price) * (float(discount) / 100)), 2)
    lopp = [name, um, cost, price, qty, date, lot, for_invoice, supplier, discount, expiry_date, var_string]
    product_purchase_listbox.insert(END, lopp)
    product_name_search.delete(0, END)
    qty_text.delete(0, END)
    cost_price_text.delete(0, END)
    selling_price_text.delete(0, END)
    category_combo.delete(0, END)
    description_text.delete(0.0, END)
    lot_text.delete(0, END)
    pentru_factura.configure(state="readonly")
    discount_text.configure(state="readonly")
    supplier_combo_search.configure(state="readonly")
    return 1


def delete_from_purchase_table():
    """

    @return:
    """
    index = product_purchase_listbox.Select_index
    if index is None or index > product_purchase_listbox.size():
        return messagebox.showinfo('Eroare',
                                   'Selecteaza randul care trebuie sters')
    product_purchase_listbox.delete(index)


def add_to_inventory():
    """

    @return:
    """
    tup_not_for = []
    if not product_purchase_listbox.tree.get_children():
        return messagebox.showinfo("Eroare", "Lista de achizitii este goala")
    item = product_purchase_listbox.tree.get_children()[-1]
    tup = product_purchase_listbox.tree.item(item)
    pid = DB.sqldb.get_product_id(tup['values'][0])
    date = tup['values'][5]
    qty = round(float(tup['values'][4]))
    cost = round(float(tup['values'][2]), 2)
    price = round(float(tup['values'][3]), 2)
    lot = tup['values'][6]
    costid = DB.sqldb.get_cost_id(pid, lot, cost, price)
    # introdu costul in baza de date
    if costid is None:
        costid = DB.sqldb.add_new_cost(pid, lot, cost, price)
        messagebox.showerror('Valoare inexistenta', 'Valoarea de achizitie ' + str(cost) + ' si valoarea de vanzare ' +
                             str(price) + ' nu exista in baza de date. El a fost adaugat.')
    s = costid + date + str(qty) + hex(int(t.time() * 10000))
    pur_id = "PUR-" + str(hash(s))
    supplier = tup['values'][8]
    for_factura = tup['values'][7]
    discount = tup['values'][9]
    expiry_date = tup['values'][10]
    supplier_id = DB.get_supplier(supplier)
    if DB.sqldb.get_purchase_doc_for_invoice(for_factura):
        messagebox.showerror('Eroare', 'Deja exista achizitie pe numarul de factura ' + str(for_factura))
        return 1
    DB.sqldb.insert_to_purchase(costid, date, discount, for_factura, pur_id, supplier_id)
    for item in product_purchase_listbox.tree.get_children():
        tup = product_purchase_listbox.tree.item(item)
        name = tup['values'][0]
        cost = round(float(tup['values'][2]), 2)
        price = round(float(tup['values'][3]), 2)
        qty = round(float(tup['values'][4]))
        date = tup['values'][5]
        pid = DB.sqldb.get_product_id(name)
        costid = DB.sqldb.get_cost_id(pid, lot, cost, price)
        for_factura = tup['values'][7]
        supplier = tup['values'][8]
        varianta = None
        if tup['values'][11]:
            varianta = var_string
        supplier_id = DB.get_supplier(supplier)
        um = get_um_for_product(pid)

        try:
            DB.add_products_to_purchase(pur_id, costid, date, qty, lot, pid, varianta, expiry_date)
            tup_not_for.append(tup["values"])
        except ValueError:
            ans = messagebox.askokcancel(
                "Achizitie existenta",
                "Achizitia pe acest produs in acest lot exista deja\n"
                "Doresti sa maresti cantitatea ?"
            )
            if ans:
                pur_i_d = DB.sqldb.get_purchase_id(costid, date, qty)
                qty += DB.sqldb.get_cell("purchase", "purchase_id", "QTY",
                                         "\"" + pur_i_d + "\"")

                DB.sqldb.edit_purchase(pur_i_d, 2, qty)
    nir_document(tup_not_for, pur_id, supplier_id)
    product_purchase_listbox.delete(0, END)
    return messagebox.showinfo("Info", "Toate produsele au fost achizitionate")


def reset():
    """

    @return:
    """
    s = messagebox.askokcancel("Avertisment",
                               "Esti sigur ca vrei sa resetezi totul?")
    if s:
        reset_coform()
    return 1


def reset_coform():
    """

    @return:
    """
    DB.sqldb.reset_database()
    return None


def remove__product(obj):
    """

    @param obj:
    @return:
    """
    del_row = obj.Select_index
    if del_row is None or del_row > obj.size():
        return messagebox.showinfo('Eroare',
                                   'Nu ai ales nimic pentru stergere')
    tup = obj.get(del_row)
    ans = messagebox.askokcancel(
        'Avertisment',
        "Esti sigur ca vrei sa stergi produsul " + tup[1] + " ?")
    if ans:
        ie = DB.delete_product(tup[0])
        if ie:
            messagebox.showinfo('Info', tup[1] + ' Sters cu succes')
        else:
            messagebox.showinfo(
                'Eroare',
                'Nu putem sterge produsul, deoarece se afla deja pe o intrare sau pe o iesire.'
            )
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
    ans = messagebox.askokcancel(
        'WARNING', "Do You Really Want To delete " + tup[1] + " ?")
    if ans:
        ie = DB.delete_customer(tup[0])
        if ie:
            messagebox.showinfo('Info', tup[1] + 'Has Been Deleted')
        else:
            messagebox.showinfo(
                'Error',
                'Sorry Cannot delete, Customer is attached to invoices')
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
    fst_l = set(DB.search_product(fst))
    return print__p_table(fst_l)


def print__p_table(lists):
    """

    @param lists:
    @return:
    """
    lists = list(lists)
    lists.sort()
    # print(lists)
    inventory_products_listbox.delete(0, END)
    for item in lists:
        tup = DB.sqldb.print_p_table_get_products(item)
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
            guiid = inventory_products_listbox.insert(END, p, colour, bg)
            tup1 = DB.sqldb.execute(
                """ select variant_id, name from product_variants where product_id = "%s" """ % p[0]).fetchall()
            inventory_products_listbox.insert(END, ('ID Varianta', 'Nume varianta'), parent=guiid, row_name='',
                                              bg="grey93", fg="Green", tag="lo")
            if tup1:
                for v in tup1:
                    inventory_products_listbox.see(
                        inventory_products_listbox.insert(END, v, parent=guiid, row_name="", bg='grey93', fg='Red',
                                                          tag="lo"))
                    tup2 = DB.sqldb.execute("""select option_id, value from variants_options where variant_id = "%s" 
                    """ % v[0]).fetchall()
                    opt_id = inventory_products_listbox.insert(END, ('ID Optiune', 'Nume optiune'), parent=guiid,
                                                               row_name='',
                                                               bg="grey93", fg="Blue", tag="lo")
                    if tup2:
                        for opt in tup2:
                            inventory_products_listbox.see(
                                inventory_products_listbox.insert(END, opt, parent=opt_id, bg="White", fg="Red",
                                                                  tag="lo"))

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
    fst_l = set(DB.search_customer(fst))
    return print__c_table(fst_l)


def print__c_table(lists):
    """

    @param lists:
    @return:
    """
    lists = list(lists)
    lists.sort()
    customer_listbox.delete(0, END)
    for item in lists:
        tup = DB.sqldb.execute(
            """SELECT customer_id,customer_name,phone_no,customer_address,customer_email
                       FROM customers JOIN contacts USING (customer_id)  WHERE customer_name = "%s" """
            % (item)).fetchall()
        for c in tup:
            guiid = customer_listbox.insert(END, c, bg=None, tag="ta")
            tup1 = DB.sqldb.execute(
                """SELECT invoice_id,invoice_no,invoice_date,paid
                           FROM invoices WHERE customer_id = "%s" ORDER BY invoice_no """
                % (c[0])).fetchall()
            customer_listbox.insert(
                END,
                ("Invoice ID", "Invoice No", "Invoice Time Stamp", "Paid"),
                parent=guiid,
                row_name="",
                bg='grey93',
                fg='Red',
                tag="lo")
            for p in tup1:
                customer_listbox.see(
                    customer_listbox.insert(END,
                                            p,
                                            parent=guiid,
                                            row_name="",
                                            bg='White',
                                            fg='Blue',
                                            tag="lol"))
            tup2 = DB.sqldb.execute(
                """ select id, name, cnp, car_no from delegates where customer_id = "%s" order by
            id """ % (c[0])).fetchall()
            customer_listbox.insert(
                END,
                ("Delegate ID", "Delegate Name", "Delegate CNP", "# Auto"),
                parent=guiid,
                row_name="",
                bg="grey93",
                fg="Green",
                tag="lo")
            for d in tup2:
                customer_listbox.see(
                    customer_listbox.insert(END,
                                            d,
                                            parent=guiid,
                                            row_name="",
                                            bg="White",
                                            fg="Brown",
                                            tag="lol"))
    customer_listbox.see("")
    customer_search.delete(0, END)
    return 1


def special__p_search(event):
    """

    @param event:
    """
    st = str(product_name.get())
    l = DB.sqldb.execute(
        """SELECT product_description,
        price FROM costs 
        JOIN products USING (product_id)
                 WHERE product_name LIKE  "%s"
                 """ % st).fetchone()
    des = l[0]
    price = l[1]
    qty = quantity.get()
    product_detail.delete(0.0, END)
    product_detail.insert(0.0, des)
    product_price.delete(0, END)
    product_price.insert(0, price)
    quantity.delete(0, END)
    quantity.insert(0, qty)
    product_id = DB.sqldb.get_product_id(st)
    # print(product_id)
    l_purchase = DB.sqldb.execute(""" select * from purchase where product_id = "%s" """ % product_id).fetchall()
    # print(l_purchase)
    if l_purchase is not None:
        print()
        # i don't know what to do with the purchase
    else:
        messagebox.showerror('Achizitie nerealizata', 'Nu a fost efectuata achizitie pe sku-ul ales')
    l_variants = DB.sqldb.execute(""" select * from product_variants where product_id = "%s" """ % st).fetchall()
    if l_variants is not None:
        print()
        # l.append(l_variants)
        # add to variants combo
    else:
        messagebox.showerror('Variante', 'Nu sunt variante pentru produsul ales')


def special__c_search(event):
    """

    @param event:
    """
    st = str(customer_name.get())
    l = DB.sqldb.execute(
        """SELECT customer_address,phone_no FROM customers JOIN contacts USING (customer_id)
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
    return DB.search_product(string.title())


def customer_name_search(string):
    """

    @param string:
    @return string
    """
    return DB.search_customer(string.title())


def supplier_name_search(string):
    """

    @param string:
    @return string
    """
    return DB.search_supplier(string.title())


def unit_name_search(string):
    """

    @param string:
    @return string
    """
    return DB.search_um(string.title())


def invoice_no_search(string):
    """
    @param string:
    @return string
    """
    return DB.search_invoice(string.title())


def category_name_search(string):
    """
    @param string:
    @return string
    """
    return DB.search_category(string.title())


def product_name__search():
    """

    @return self.add
    """
    inp = str(product_name.get())
    if inp == " ":
        inp = ""
    l = product_name_search_func(inp)
    return add(product_name, l)


def call__cn_search(event):
    """

    Event for calling customer search
    @param event:
    """
    customer_name__search()


def customer_name__search():
    """

    Searching customer names
    """
    inp = Filter(customer_name.get())
    if inp == " ":
        inp = ""
    l = customer_name_search(inp)
    return add(customer_name, l)


def call__cu_search(event):
    """

    Event for calling customer search
    @param event
    """
    customer__search()


# def call__i_search(event):
#     invoice__search()


def customer__search():
    """

    @return:
    """
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
    """

    @param event:
    """
    category__search()


def category__search():
    """

    @return:
    """
    inp = str(category_combo.get())
    if inp == " ":
        inp = ""
    l = category_name_search(inp)
    return add(category_combo, l)


def product__search():
    """

    @return:
    """
    inp = str(product_search.get())
    if inp == " ":
        inp = ""
    l = product_name_search_func(inp)
    return add(product_search, l)


def call__p_search(event):
    """

    @param event:
    """
    product__search()


def add(obj, l):
    """

    @param obj:
    @param l:
    """
    l = list(l)
    l.sort()
    obj["value"] = ""
    obj["value"] = list(l)


def ask_db_file():
    """

    @return:
    """
    fname = askopenfilename(filetypes=(('Fisier FitoGest', "*.ic"),
                                       ('All File', "*.*")))
    try:
        ds = open(fname, 'r')
    except IOError:
        messagebox.showinfo("Fisier inexistent",
                            "Nu am gasit niciun fisier cu acest nume!")
        return 0
    del ds
    boo = DB.load(fname)
    b_customer__search(refresh=True)
    b_product__search(refresh=True)
    if not boo:
        return messagebox.showinfo("Mesaj", "Eroare la incarcarea produselor")
    return messagebox.showinfo("Mesaj", "S-a finalizat incarcarea produselor")


def export(objentry1):
    """

    @param objentry1:
    @return:
    """
    from src.ImportExport import ExportCsv
    ans = messagebox.askokcancel(
        "Avertisment", "2 fisiere vor fi exportate in acest dosar ?")
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
    return messagebox.showinfo("Mesaj", "Fisierul tau a fost exportat")


def brow__file(obj):
    """Should always use entry widget as obj"""
    from tkinter.filedialog import askopenfilename
    try:
        fname = askopenfilename(filetypes=(('Csv File', "*.csv"), ('All File',
                                                                   "*.*")))
    except [IOError]:
        fname = ""
        messagebox.showinfo("Eroare fisier", "Alege din nou")
    if len(fname) == 0:
        messagebox.showinfo("Eroare fisier",
                            "Trebuie sa alegi un fisier CSV pentru inventar")
        return None
    obj.delete(0, END)
    obj.insert(0, fname)
    return 1


def save__as__file(obj):
    """
    Should always use entry widget as obj

    @param obj
    """
    try:
        fname = asksaveasfilename(defaultextension='.csv',
                                  filetypes=[('Csv File', "*.csv"),
                                             ('TEXT File', "*.txt")])
    except [IOError]:
        fname = ""
        messagebox.showinfo(
            "Eroare fisier",
            "Ar trebui sa exporti ca sa ai o copie de rezerva")
    if len(fname) == 0:
        messagebox.showinfo("Eroare fisier",
                            "Trebuie sa alegi un fisier CSV pentru inventar")
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
    """

    @param event:
    @return:
    """
    cur_item = inventory_products_listbox.tree.focus()
    index = int(inventory_products_listbox.tree.identify_column(event.x)[1])
    id = inventory_products_listbox.tree.item(cur_item)
    arg = id["values"][0]

    if index == 3:
        return category_opt_event()
    elif 1 < index < 6:
        return a_d_d__product(arg, modify=True)
    else:
        return 0


def d_click__on__c_list(event):
    """

    @param event:
    @return:
    """
    index = int(customer_listbox.tree.identify_column(event.x)[1])
    if index == 5:
        return invoice_opt_event()
    elif 7 > index > 1:
        return a_d_d__customer(modify=True)
    else:
        return 0


def get_pdf_date(timestamp):
    """

    @param timestamp:
    @return:
    """
    p = timestamp.split()
    del p[3]
    return " ".join(p)


# product_search.bind('<Any-KeyRelease>', call__p_search)
customer_search.bind('<Any-KeyRelease>', call__cu_search)
customer_name.bind('<Any-KeyRelease>', call__cn_search)
product_name.bind('<Any-KeyRelease>', call__pn_search)
customer_name.bind('<<ComboboxSelected>>', special__c_search)
product_name.bind('<<ComboboxSelected>>', special__p_search)
customer_listbox.tree.bind('<Double-Button-1>', d_click__on__c_list)
inventory_products_listbox.tree.bind('<Double-Button-1>', d_click__on__list)
product_name_search.bind('<Any-KeyRelease>', call_purchase_search)
product_name_search.bind('<<ComboboxSelected>>', special_purchase_search)


def process_cart(invid):
    """

    @param invid:
    @return:
    """
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
        product_lot = r['values'][5]
        product_variant = r['values'][6]
        expiry_date = DB.sqldb.get_expiration_date_for_lot(product_lot)
        listsw = [
            i, product_info, product_qty, product_price2,
            str(product_amount), product_variant, expiry_date
        ]
        lik.append(listsw)
        sold_price = product_price2 - discount_per_product
        DB.add_sells(costid, sold_price, invid, product_qty)
        DB.deplete_qty(product_lot, product_qty, product_name2, product_variant)
        i += 1
    mlb.delete(0, END)
    return lik


def generate__invoice(product__list_forpdf, custup, invoicetup, detail):
    """
    Generarea facturilor

    @param product__list_forpdf, custup, invoicetup, detail
    """
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

    PDfCompany_Adress = Company_Adress + "\n" + \
                        Detail_top + "\n" + email + "\n" + phone
    pdfcust_address = cust_address + "\n" + cust_phone
    try:
        delegate = DB.sqldb.get_delegate_for(custup[0])
    except ValueError as e:
        messagebox.showerror("Eroare delegat", e.__cause__)
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
                 sub_total=subtol_var.get())
    fileline = "Factura-" + invoi_num + ".pdf"

    try:
        if sys.platform == "win32":
            os.startfile(fileline)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            os.subprocess.call([opener, fileline])
    except FileExistsError:
        fileline = askopenfilename(filetypes=(('Microsoft Word Document File',
                                               "*.docx"),
                                              ("Portable Document File",
                                               "*.pdf")))
        if sys.platform == "win32":
            os.startfile(fileline)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            os.subprocess.call([opener, fileline])
    return None


def transfer():
    """

    @return:
    """
    invoi_num = invoice__maintain()
    detail = DB.sqldb.get_company_details
    if invoi_num is None:
        return 1
    alooas = DB.sqldb.get_invoice_id(invoi_num)
    if alooas is not None:
        return messagebox.showinfo(
            "Eroare",
            "Numarul de factura exista deja si este asignat unui alt client",
            parent=root)
    if mlb.size() == 0:
        messagebox.showinfo("Eroare Intrare",
                            "Ar trebui sa adaugi un produs",
                            parent=root)
        return 1
    custup = pre_inv()
    if custup is None:
        return messagebox.showinfo("Eroare Intrare",
                                   "Detaliile clientului sunt incomplete",
                                   parent=root)
    if len(detail['comp_name']) == 0 or len(detail['comp_add']) == 0 or len(
            detail['comp_phn']) == 0:
        messagebox.showinfo("Eroare Intrare",
                            "Detaliile firmei sunt incomplete",
                            parent=root)
        return 1
    ctmid, cust_name, cust_address, cust_phone = custup
    invoice__date2 = str(invoice_date.get())
    discount = str(Discount_var.get())
    amount = str(Amt_var.get())
    Grand_total = str(Gtol_var.get())
    invid = DB.add_invoice(ctmid, invoi_num, Grand_total, invoice__date2)
    Product_List_forpdf = process_cart(invid)
    invoicetup = (invoice__date2, invoi_num, Grand_total, amount, discount)
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
        messagebox.showinfo("Avertisment",
                            "Nu sunt permise litere in cadrul facturarii")
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
        return messagebox.showinfo(title='Error',
                                   message='Nothing is Selected To Remove')
    tup = mlb.get(index)
    a = float(tup[3]) * float(tup[4])
    amount = float(Amt_var.get()) - a
    Amt_var.set(amount)
    mlb.delete(index)


def add_discount(event):
    """

    @param event:
    @return:
    """
    paid = Filter(entry20.get())
    if len(paid) == 0:
        return 1
    if not paid.isdigit():
        try:
            paid = float(paid)
        except ValueError:
            messagebox.showinfo("Eroare Intrare",
                                "Discoutul trebuie sa fie numeric")
            return 1
    paid = float(paid)
    dis = float(subtol_var.get()) - paid
    Discount_var.set(str(dis))
    Gtol_var.set(str(paid))


entry20.bind('<Any-KeyRelease>', add_discount)


def add_2_cart():
    """

    @return:
    """
    product = Filter(str(product_name.get()))
    p_de = Filter(str(product_detail.get(0.0, END)))
    p_price = Filter(str(product_price.get()))
    qty = Filter(str(quantity.get()))
    lot_var = lot.get()
    variant_str = var_combo.get()
    if len(product) == 0:
        messagebox.showinfo("Eroare Intrare",
                            "Numele produsului trebuie sa fie completat")
        return 1
    if len(p_price) == 0:
        messagebox.showinfo("Eroare Intrare",
                            "Pretul produsului trebuie sa fie prezent")
        return 1
    try:
        p_price = float(p_price)
    except ValueError:
        messagebox.showinfo("Eroare Intrare",
                            "Pretul produsului trebuie sa fie numeric")
        return 1
    if len(qty) == 0:
        messagebox.showinfo("Eroare Intrare",
                            "Produsul nu poate fi adaugat fara cantitate")
        return 1

    try:
        qty = float(qty)
    except ValueError:
        messagebox.showinfo(
            "Eroare Intrare",
            "Cantitatea produsului trebuie sa fie o valoare numerica")
        return 1
    PID = DB.sqldb.get_product_id(product)
    if PID is None:
        return messagebox.showinfo("Eroare Intrare",
                                   "ID-ul produsului nu exista")
    costid = DB.get_any_cost_id(PID, lot_var, p_price)
    if costid is None:
        # @FIXME
        costid = DB.get_cost_id_with_lot(PID, '', lot_var)
        # print('costid')
        # print(costid)
        # for i in costid:
            # print('costid: ' + i)
        # Inseamna ca costul nu exista, a avut discount, discountul a fost trecut in lot si trebuie cautat cu join pe
        # lot
        return messagebox.showinfo("Eroare", "Produsul nu este in inventar")
    boo = False
    for ITEM in xrange(int(mlb.size())):
        r = mlb.get(ITEM)
        if costid == r[0]:
            newqty = float(r[3]) + float(qty)
            mlb.set_value(ITEM, "Cantitate", newqty)
            boo = True
    if not boo:
        tup = (costid, product, p_de, float(qty), p_price, lot_var, variant_str)
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
    """
    Se apeleaza pentru validare inainte de generarea unei facturi

    @return ctmid, name, address, phone
    """
    name = Filter(str(customer_name.get()))
    address = Filter(str(customer_address.get(0.0, END)))
    phone = Filter(str(customer_phone.get()))
    if len(name) == 0 or len(address) == 0 or len(phone) == 0:
        messagebox.showinfo("Goliciune",
                            "Ar trebui sa introduci toate detaliile")
        return None
    if not phone.isdigit():
        messagebox.showinfo(title="Eroare",
                            message='Acesta nu este un numar valid de telefon',
                            parent=root)
        return None
    ctmid = DB.sqldb.get_customer_id(phone)
    if ctmid is None:
        ctmid = DB.add_customer(name, address, phone, "")
    else:
        dbcmname = DB.sqldb.get_cell("customers", "customer_id",
                                     "customer_name", ctmid)
        if dbcmname != name:
            messagebox.showinfo(
                "Eroare",
                "Numarul de telefon exista deja si ii este asociat lui %s" %
                dbcmname)
            return None
    return ctmid, name, address, phone


def make_sure_path_exist(path):
    """

    @param path:
    @return:
    """
    import os
    filepath = os.getcwd()
    if not os.path.exists(filepath + os.path.sep + path):
        os.mkdir(filepath + os.path.sep + path)
    else:
        pass
    return 1


def a_d_d__product(id=False, modify=False):
    """

    @param id:
    @param modify:
    @return:
    """
    tup = []
    if not modify:
        titlel = "Create Produs"
    else:
        titlel = "Modificare Produs"
        index = inventory_products_listbox.Select_index
        if index is None or index > inventory_products_listbox.size():
            return messagebox.showinfo(title='Eroare',
                                       message='Nu ai ales nimic de modificat')
        cur_item = inventory_products_listbox.tree.focus()
        arg = inventory_products_listbox.tree.item(cur_item)
        tup = inventory_products_listbox.tree.item(cur_item)
        id = arg["values"][0]
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
    """

    @param modify:
    @return:
    """
    tup = []
    if not modify:
        titlel = "Creare client"
    else:
        titlel = "Modificare client"
        index = customer_listbox.Select_index
        if index is None or index > customer_listbox.size():
            return messagebox.showinfo('Eroare',
                                       'Nu ai ales nimic ca sa modifici.')
        cur_item = customer_listbox.tree.focus()
        arg = customer_listbox.tree.item(cur_item)
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
    ans = messagebox.askokcancel("Avertisment",
                                 "Doresti sa salvezi modificarile?")
    if ans:
        DB.save()
        root.destroy()
    else:
        root.destroy()


def cdmp_del():
    sapp = SampleApp(root, DB)
    sapp.load__de()


def add_supplier(id=False, modify=False):
    """
    method that is called upon button call
    @param id: the supplier id for modify
    @param modify: boolean flag
    @return autorefresh the MultiListbox object holding
    the suppliers
    """
    tup = []
    if not modify:
        title = "Furnizor nou"
    else:
        title = "Modificare furnizor"
        index = mlb51.Select_index
        piid = mlb51.true_parent(mlb51.Select_iid)
        index = mlb51.index(piid)
        tup = mlb51.get(index)
        cur_item = mlb51.tree.focus()
        arg = mlb51.tree.item(cur_item)
        id = arg["values"][0]
        if index is None or index > mlb51.size():
            return messagebox.showinfo(
                "Eroare", "Selecteaza ceva pentru a fi modificat")
    root13 = tk.Toplevel(master=root)
    root13.title(title)
    root13.focus()
    root13.grid()
    root13.rowconfigure(0, weight=1)
    root13.columnconfigure(0, weight=1)
    n_s = NewSupplier(root13, modify, tup, DB, id)
    n_s.grid(row=0, column=0, sticky=N + W + S + E)
    n_s.rowconfigure(0, weight=1)
    n_s.columnconfigure(0, weight=1)
    root13.wait_window()
    return b_supplier_search(refresh=True)


def remove_supplier(mlb51):
    """
    remove supplier

    @param mlb51: The MultiListbox object
    """
    piid = mlb51.true_parent(mlb51.Select_iid)
    index = mlb51.index(piid)

    pass


invoice__date()
invoice_num()
b_product__search(refresh=True)
b_customer__search(refresh=True)
b_supplier_search(refresh=True)
make_sure_path_exist("invoice")
make_sure_path_exist("data")
make_sure_path_exist("niruri")
root.protocol(name="WM_DELETE_WINDOW", func=call_save)

root.mainloop()
