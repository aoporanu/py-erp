from tkinter import *
from tkinter.messagebox import askokcancel, showerror
from tkinter.messagebox import showinfo
from tkinter.ttk import *

from src.Cython.buttoncalender import CalendarButton
from src.Cython.proWrd1 import Filter
from src.MultiListbox import MultiListbox

sty = N + W + S + E


def select_first(item):
    return item[0]


class NewProduct(Frame):
    def __init__(self, master, tup, modify, db, id, **kw):
        # print(tup)
        Frame.__init__(self, master)
        super().__init__(master, **kw)

        self.f = Frame(self, style='me.TFrame')
        self.f.grid(row=0, column=0, sticky=sty)
        self.f.rowconfigure(1, weight=3)
        self.f.columnconfigure(0, weight=1)
        note = Notebook(self.f)
        note.grid(row=1, column=0, sticky=sty)
        note.rowconfigure(0, weight=1)
        note.columnconfigure(0, weight=1)
        self.costs_app = Frame(note)
        self.purchase_app = Frame(note)
        self.purchase_lf = Frame(self.purchase_app)
        self.btn_delete_costs = Button(self.costs_app,
                                       text="delete costs",
                                       command=lambda: self.delete_cost())
        self.mlb_costs = MultiListbox(self.costs_app, (("Cost ID", 25), ("Cost Price", 30),
                                                       ("Selling Price", 30), ("Qty", 15)))
        self.sales_lf = LabelFrame(self.costs_app, text="ADD New Costs", labelanchor=N + W)
        self.costhead = self.sales_lf
        self.ncost = Entry(self.sales_lf)
        self.btn14 = Button(self.sales_lf,
                            text="Edit Cost",
                            command=lambda: self.addcost(True))
        self.nprice = Entry(self.sales_lf)
        self.btn13 = Button(self.sales_lf,
                            text="Add Cost",
                            command=lambda: self.addcost())
        self.id = id
        self.db = db
        self.tup = tup
        self.modify = modify
        bg = 'White'
        fg = "#3496ff"
        self.master = master

        if modify:
            value = id
        else:
            value = "Product Name"
        self.name = Label(self.f,
                          text=value,
                          font=('Berlin Sans FB Demi', 40),
                          foreground=fg)
        self.name.grid(row=0, column=0, sticky=sty)

        self.notepage_detail(note, modify, tup, id)
        self.variants_app = Frame(note)
        self.variation_lf = LabelFrame(self.variants_app, text="Adaugare variante", labelanchor=N + W)
        self.entry_new_variant_modifier = Entry(self.variation_lf, width=15)
        self.entry_new_variant_value = Entry(self.variation_lf, width=15)
        self.label_new_variant_value = Label(self.variation_lf, text="Valoare varianta")
        self.label_new_variant_name = Label(self.variation_lf, text="Nume varianta")
        self.entry_new_variant_name = Entry(self.variation_lf, width=35)
        self.label_new_variant_price_modifier = Label(self.variation_lf, text="Modificator pret")
        self.btn_variants_delete = Button(self.variants_app,
                                          text="stergere varianta",
                                          command=lambda: self.delete_variant())
        self.btn_variants_add = Button(self.variation_lf,
                                       text="adauga variatiune",
                                       command=lambda: self.add_variant())
        self.btn_variants_edit = Button(self.variation_lf,
                                        text="editare varianta",
                                        command=lambda: self.add_variant(True))
        self.mlb_variants = MultiListbox(self.variants_app, (('ID Produs', 20), ('Nume varianta', 10), ('Valoare', 20),
                                                             ('Modificator pret', 10)))
        if modify:
            self.notepage_costs(note)
            self.notepage_purchase(note)
            self.notepage_sales(note)
            self.notepage_variants(note)

    def update_name(self, event):
        name = Filter(self.entry5.get()).title()
        if len(name) == 0:
            name = "Product Name"
        self.name.configure(text=name)

    def load_percent(self, cost, price):
        if float(cost) == 0.0:
            return 0
        profit = float(price) - float(cost)
        percent = (100 * profit) / float(cost)
        return round(percent, 2)

    def notepage_detail(self, note, modify, tup, id):
        app = Frame(note)
        app.grid(row=0, column=0)
        self.f.rowconfigure(0, weight=1)
        self.f.columnconfigure(0, weight=1)
        note.add(app, text='Detail')
        for i in range(17):
            app.rowconfigure(i, weight=1)
        for i in range(8):
            app.columnconfigure(i, weight=1)
        Label(app,
              text='Product Detail',
              font=('Berlin Sans FB Demi', 23),
              foreground="#3496ff").grid(row=0,
                                         column=0,
                                         columnspan=2,
                                         sticky=sty)

        Label(app, text='Product Name').grid(row=1,
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

        Label(app, text="Product Category").grid(row=2,
                                                 column=0,
                                                 sticky=E,
                                                 padx=10,
                                                 pady=10)
        self.entry = Combobox(app, width=35)
        self.entry.grid(row=2,
                        column=1,
                        columnspan=2,
                        sticky=sty,
                        padx=10,
                        pady=10)

        Label(app, text="Product Description").grid(row=3,
                                                    column=0,
                                                    sticky=N + E,
                                                    padx=10,
                                                    pady=10)
        self.text = Text(app, width=26, height=5, wrap=WORD, relief=FLAT)
        self.text.grid(row=3,
                       column=1,
                       columnspan=2,
                       sticky=sty,
                       padx=10,
                       pady=10)
        self.text.configure(highlightthickness=1, highlightbackground="Grey")
        self.df = self.text.configure()

        Label(app, text="Product QTY").grid(row=4,
                                            column=0,
                                            sticky=E,
                                            padx=10,
                                            pady=10)
        self.qty = StringVar()
        self.entry3 = Entry(app, width=35, textvariable=self.qty)
        self.entry3.grid(row=4,
                         column=1,
                         columnspan=2,
                         sticky=E + W,
                         padx=10,
                         pady=10)

        Label(app, text=" Product ID ").grid(row=5, column=0, sticky=E)
        self.entry6 = Entry(app, width=35)
        self.entry6.grid(row=5,
                         column=1,
                         columnspan=2,
                         sticky=sty,
                         padx=10,
                         pady=10)

        Label(app, text=" Unit of Measure").grid(row=6, column=0, sticky=E)
        self.entry7 = Combobox(app, width=35)
        self.entry7.grid(row=6,
                         column=1,
                         columnspan=2,
                         sticky=sty,
                         padx=10,
                         pady=10)
        Label(app, text="TVA").grid(row=7, column=0, sticky=E)
        self.entry8 = Entry(app, width=35)
        self.entry8.grid(row=7, column=1, columnspan=2, sticky=sty, padx=10,
                         pady=10)
        btn = Button(app,
                     text='save',
                     width=12,
                     command=lambda: self.save(modify, self.tup),
                     style='new.TButton')
        btn.grid(row=8, column=1, sticky=sty, padx=10, pady=10)
        copy = Button(app,
                      text='save As Copy',
                      command=lambda: self.save(False, self.tup),
                      style='new.TButton')
        copy.grid(row=8, column=2, sticky=sty, padx=10, pady=10)
        keys = self.db.sqldb.execute(
            "SELECT category_name FROM category").fetchall()
        _keys_um = self.db.sqldb.execute(
            "select name from units_of_measure").fetchall()
        keys_um = sorted(map(select_first, _keys_um))
        keys_um.sort()
        keys = sorted(map(select_first, keys))
        keys.sort()
        self.entry['value'] = keys
        self.entry7["value"] = keys_um
        del keys
        del keys_um
        if not modify:
            copy['state'] = DISABLED
        if modify:
            d = self.db.sqldb.execute(
                """ SELECT product_name,category_name,product_description FROM
            products
                        JOIN category USING (category_id) join units_of_measure on products.um_id=units_of_measure.id 
                        WHERE product_id = "%s" """ % tup['values'][0]).fetchone()
            # print(d)
            name = d[0]
            category = d[1]
            Des = d[2]
            no = tup['values'][0]
            qty = self.db.sqldb.get_quantity(no)
            um = self.db.sqldb.get_um(no)
            self.entry5.delete(0, END)
            self.entry5.insert(0, name)
            self.entry.delete(0, END)
            self.entry.insert(0, category)
            self.text.delete(0.0, END)
            self.text.insert(0.0, Des)
            self.entry3.delete(0, END)
            self.qty.set(qty)
            self.entry6.delete(0, END)
            self.entry6.insert(0, no)
            self.entry7.delete(0, END)
            self.entry7.insert(0, um)
        self.entry6['state'] = "readonly"
        self.entry3['state'] = "readwrite"

    def Percent(self, event):
        cost = Filter(self.entry4.get())
        if len(cost) == 0:
            return showinfo(
                title="Error",
                message='Product Cost Must Be Specified Before Product % ',
                parent=self.master)
        else:
            try:
                cost = float(cost)
            except (AttributeError, ValueError):
                return showinfo(
                    title="Error",
                    message='Numbers Must be Written in Cost Entry',
                    parent=self.master)
        percent = Filter(self.entry7.get())
        if len(percent) == 0:
            percent = 0
        else:
            try:
                percent = float(percent)
            except (AttributeError, ValueError):
                return showinfo(
                    title="Error",
                    message='Numbers Must be Written in Profit % Entry',
                    parent=self.master)
        s = cost / 100.0
        s = s * percent
        price = float(cost) + s
        price = round(price, 2)
        self.entry2.delete(0, END)
        self.entry2.insert(0, price)
        return 1

    def save(self, modify, tup):
        """Objects of Tup
           tup[0] ->  ID No
           tup[1] ->  Product name
           tup[2] ->  category
           tup[3] ->  description
           tup[4] ->  quantity
        """

        name = Filter(self.entry5.get()).title()
        category = Filter(self.entry.get()).title()
        description = Filter(self.text.get(0.0, END)).title()
        um = Filter(self.entry7.get()).title()
        tva = Filter(self.entry8.get()).title()
        if len(name.split()) == 0:
            return showinfo(title="Error",
                            message='Product Name Must Be Specified',
                            parent=self.master)
        if len(category.split()) == 0:
            return showinfo(title="Error",
                            message='Product Category Must Be Specified',
                            parent=self.master)
        if len(um.split()) == 0:
            return showinfo(title="Error",
                            message='Product Category Must Be Specified',
                            parent=self.master)
        vre = self.db.sqldb.get_product_id(name)
        if not modify:
            if vre is not None:
                return showinfo(
                    title="Error",
                    message=
                    'Product Name is Already Listed Change Name To save As Copy',
                    parent=self.master)
            PID = self.db.add_product(name, category, description, um, tva)
        elif modify:
            print(tup)
            PID = tup['values'][0]
            # previousname = tup['values'][1]
            # previouscategory = tup['values'][2]
            # pdescription = tup['values'][3]
            # if previousname != name:
            #     if vre is not None:
            #         return showinfo(title="Error",
            #                         message='Product Name is Already Listed',
            #                         parent=self.master)
            #     s = askokcancel(
            #         "Name Mismatch",
            #         "Are You Sure You Want to Change\n\n%s to %s\n\n%s to %s\n\n%s to %s"
            #         % (previousname, name, previouscategory, category,
            #            pdescription, description),
            #         parent=self.master)
            #     if not s:
            #         return False
            self.db.edit_product(PID, name, category, description, um)
        self.master.destroy()
        return showinfo("Adaugat", 'Produsul a fost salvat')

    def add_to_cost_list_box(self):
        self.mlb_costs.delete(0, END)
        ins = self.mlb_costs.insert
        if self.modify:
            row = self.db.sqldb.execute(
                """ SELECT cost_id,cost,price FROM costs
                                          JOIN products USING (product_id)  WHERE product_id = "%s"  """
                % (self.tup['values'][0])).fetchall()
            for i in row:
                i = list(i)
                price = i[2]
                cost = i[1]
                costid = i[0]
                qty = self.db.sqldb.get_cost_quantity(costid)
                i.append(qty)
                ins(END, i)

    def dummy(self):
        pass

    def addcost(self, edit=False):
        try:
            PID = self.tup['values'][0]
        except IndexError:
            return showinfo(title="ERROR",
                            message='Product Not Yet Saved',
                            parent=self.master)
        try:
            newcost = float(Filter(self.ncost.get()))
            newprice = float(Filter(self.nprice.get()))
        except:
            return showinfo(title="ERROR",
                            message='costs and price must be numbers',
                            parent=self.master)
        costid = self.db.sqldb.get_cost_id(PID, newcost, newprice)
        if costid is not None:
            return showinfo("Message",
                            "Cost and Price Already Listed",
                            parent=self.master)
        if not edit:
            self.db.sqldb.add_new_cost(PID, newcost, newprice)
        else:
            i = self.mlb_costs.Select_index
            if i is None:
                return showinfo("Message",
                                "Select a Cost Or Price To Edit",
                                parent=self.master)
            r = self.mlb_costs.get(i)
            pcostid = r[0]
            self.db.edit_costs(pcostid, PID, newcost, newprice)
        self.add_to_cost_list_box()
        self.ncost.delete(0, END)
        self.nprice.delete(0, END)

    def delete_cost(self):
        PID = self.tup['values'][0]
        costid = self.pcostid
        if costid is None:
            return showinfo("Message",
                            "Select a Cost Or Price To delete",
                            parent=self.master)
        ans = self.db.sqldb.delete_cost(costid)
        if ans:
            return showinfo("Message",
                            "%s Has Been Successfully Deleted" % (costid),
                            parent=self.master), self.add_to_cost_list_box()
        else:
            return showinfo(
                "Message",
                "Cannot delete %s It Is Associated With Purchase And Sells" %
                costid,
                parent=self.master)

    def setcostid(self, event):
        i = self.mlb_costs.Select_index
        r = self.mlb_costs.get(i)
        pcostid = r[0]
        self.costhead['text'] = pcostid
        self.pcostid = pcostid

    def notepage_costs(self, note):
        self.pcostid = None
        self.costs_app.grid(row=0, column=0)
        for i in range(3):
            self.costs_app.rowconfigure(i, weight=1)
        for i in range(3):
            self.costs_app.columnconfigure(i, weight=1)
        self.costs_app.rowconfigure(0, weight=1)
        note.add(self.costs_app, text=' Costs ')
        Label(self.costs_app,
              text="Product Costs",
              foreground="#3496ff",
              font=('Berlin Sans FB Demi', 25)).grid(row=0,
                                                     column=0,
                                                     columnspan=1,
                                                     sticky=sty,
                                                     pady=9)
        self.btn_delete_costs.grid(row=0, column=2, sticky=sty, pady=20, padx=10)
        self.mlb_costs.grid(row=1, column=0, columnspan=3, sticky=sty)
        self.mlb_costs.tree.bind('<Double-Button-1>', self.setcostid)
        self.sales_lf.grid(row=2, column=0, sticky=sty, pady=5, padx=5)
        for i in range(3):
            self.sales_lf.rowconfigure(i, weight=1)
        for i in range(2):
            self.sales_lf.columnconfigure(i, weight=1)
        Label(self.sales_lf, text="New Cost").grid(row=0,
                                                   column=0,
                                                   sticky=sty,
                                                   pady=5,
                                                   padx=5)
        self.ncost.grid(row=0, column=1, sticky=sty, pady=5, padx=5)
        Label(self.sales_lf, text="New Price").grid(row=1,
                                                    column=0,
                                                    sticky=sty,
                                                    pady=5,
                                                    padx=5)
        self.nprice.grid(row=1, column=1, sticky=sty, pady=5, padx=5)
        self.btn13.grid(row=2, column=1, sticky=sty, pady=5, padx=5)
        self.btn14.grid(row=2, column=0, sticky=sty, pady=5, padx=5)
        self.add_to_cost_list_box()

    def mlb_variants_load(self):
        self.mlb_variants.delete(0, END)
        ins = self.mlb_variants.insert
        row = self.db.sqldb.execute(""" select * from product_variants join variants_options using(variant_id) where 
        product_id = "%s" """ % self.tup['values'][0]).fetchall()
        for i in row:
            i = list(i)
            to_insert = [self.tup['values'][0], i[1], i[5], i[7]]
            ins(END, to_insert)

    def Add2Mlb21(self):
        self.mlb21.delete(0, END)
        estmpro = 0
        cap = 0
        brou = 0
        ins = self.mlb21.insert
        if self.modify:
            row = self.db.sqldb.execute("""select 
            pur.purchase_id, pur.for_invoice, pur.supplier_id, pp.purchased_qty, c.cost, c.price, 
            pp.product_id, pur.purchase_date
            from purchased_products pp 
            left join costs as c on c.cost_id = pp.cost_id 
            left join purchase as pur on pur.purchase_id  = pp.purchase_id where pp.product_id ="%s" """ %
                                        self.tup['values'][0]).fetchall()
            # print(row)
            for i in row:
                i = list(i)
                purid = i[0]
                price = i[5]
                cost = i[4]
                date = i[7]
                qty = i[3]
                profit = round(price - cost, 2)
                estmpro += (profit * qty)
                cap += cost * qty
                brou += qty
                i.append(profit)
                app = [purid, date, cost, price, qty, cap]
                ins(END, app)
        self.te.configure(text=str(estmpro))
        self.ci.configure(text=str(cap))
        self.ib.configure(text=str(brou))

    def purchaseedit(self, event):
        i = self.mlb21.tree.focus()
        if i is None:
            return showinfo("Message", "No Item Selected", parent=self.master)
        r = self.mlb21.tree.item(i)['values']
        self.purid = r[0]
        root13 = Toplevel()
        root13.title("Modificare achiztie")
        root13.grid()
        for i in range(5):
            root13.rowconfigure(i, weight=1)
        for i in range(2):
            root13.columnconfigure(i, weight=1)
        lf = root13
        self.purgui = root13
        color = 'gray98'
        root13['background'] = color
        Label(lf,
              text="ID Achizitie : %s" % self.purid,
              foreground="#3496ff",
              font=('Berlin Sans FB Demi', 18)).grid(row=0,
                                                     column=0,
                                                     columnspan=2,
                                                     sticky=sty,
                                                     pady=8,
                                                     padx=7)
        r = self.db.sqldb.execute(
            """ SELECT purchase_date, purchased_qty, cost, price FROM purchase
             join purchased_products using(purchase_id)
            JOIN costs USING (cost_id)
             WHERE purchase_id = "%s"
            """ % self.purid).fetchone()
        Label(lf, text="Data Achizitie").grid(row=1,
                                             column=0,
                                             sticky=sty,
                                             pady=8,
                                             padx=2)
        Label(lf, text="Cantitate").grid(row=2,
                                        column=0,
                                        sticky=sty,
                                        pady=8,
                                        padx=7)
        Label(lf, text="Cost").grid(row=3,
                                    column=0,
                                    sticky=sty,
                                    pady=8,
                                    padx=7)
        Label(lf, text="Pret").grid(row=4,
                                     column=0,
                                     sticky=sty,
                                     pady=8,
                                     padx=7)
        self.purdate = CalendarButton(lf)
        self.purdate.grid(row=1, column=1, sticky=sty, pady=8, padx=7)
        try:
            self.purdate.insert(r[0])
        except:
            self.purdate.insert(self.purdate.getTimeStamp())
        self.purqty = Entry(lf)
        self.purqty.grid(row=2, column=1, sticky=sty, pady=8, padx=7)
        self.purqty.delete(0, END)
        self.purqty.insert(0, r[1])
        self.purcost = Entry(lf)
        self.purcost.grid(row=3, column=1, sticky=sty, pady=8, padx=7)
        self.purcost.delete(0, END)
        self.purcost.insert(0, r[2])
        self.purprice = Entry(lf)
        self.purprice.grid(row=4, column=1, sticky=sty, pady=8, padx=7)
        self.purprice.delete(0, END)
        self.purprice.insert(0, r[3])
        Button(lf, text="save",
               command=lambda: self.purchasesave()).grid(row=5,
                                                         column=1,
                                                         sticky=sty,
                                                         pady=8,
                                                         padx=7)
        root13.wait_window()
        return 1

    def purchasesave(self):
        PID = self.tup['values'][0]
        try:
            cost = float(Filter(self.purcost.get()))
            price = float(Filter(self.purprice.get()))
            qty = float(Filter(self.purqty.get()))
            date = Filter(self.purdate.get())
            date = " ".join(date.split())
        except:
            return showinfo(title="ERROR",
                            message='costs and price must be numbers',
                            parent=self.master)
        costid = self.db.sqldb.get_cost_id(PID, cost, price)
        if costid is None:
            costid = self.db.sqldb.add_new_cost(PID, cost, price)
        self.db.edit_purchase(self.purid, costid, qty, date)
        self.purgui.destroy()
        self.Add2Mlb21()
        return showinfo(title="Successful",
                        message='Changes Saved',
                        parent=self.master)

    def deletepurchase(self):
        i = self.mlb21.Select_index
        if i == None:
            return showinfo("Message", "No Item Selected", parent=self.master)
        r = self.mlb21.get(i)
        self.purid = r[0]
        ans = askokcancel("Message",
                          "Sure You Want To delete %s ?" % (self.purid),
                          parent=self.master)
        if ans == True:
            self.db.delete_purchase(self.purid)
            return showinfo("Message",
                            "%s Has Been Successfully Deleted" % (self.purid),
                            parent=self.master), self.Add2Mlb21()
        return False

    def notepage_purchase(self, note):
        self.purid = None
        self.purchase_app.grid(row=0, column=0)
        for i in range(3):
            self.purchase_app.rowconfigure(i, weight=1)
        for i in range(3):
            self.purchase_app.columnconfigure(i, weight=1)
        self.purchase_app.rowconfigure(0, weight=1)
        note.add(self.purchase_app, text=' Purchase ')
        Label(self.purchase_app,
              text="Purchase Records",
              foreground="#3496ff",
              font=('Berlin Sans FB Demi', 25)).grid(row=0,
                                                     column=0,
                                                     columnspan=1,
                                                     sticky=sty,
                                                     pady=9)
        self.btn21 = Button(self.purchase_app,
                            text="Edit Purchase Records",
                            command=lambda: self.purchaseedit(None))
        self.btn21.grid(row=0, column=1, sticky=sty, pady=20)
        self.btn22 = Button(self.purchase_app,
                            text="delete Purchase Records",
                            command=lambda: self.deletepurchase())
        self.btn22.grid(row=0, column=2, sticky=sty, pady=20, padx=10)
        self.mlb21 = MultiListbox(self.purchase_app,
                                  (("Purchase ID", 25), ("Purchase Date", 35),
                                   ("Cost Price", 25), ("Selling Price", 25),
                                   ("Qty", 10), ("Expected profit", 25)))
        self.mlb21.grid(row=1, column=0, columnspan=3, sticky=sty)
        self.mlb21.tree.bind('<Double-Button-1>', self.purchaseedit)
        self.purchase_lf.grid(row=2, column=0, sticky=sty)
        Label(self.purchase_lf, text="Total Profit Estimated  - ").grid(row=1,
                                                                        column=0,
                                                                        sticky=sty,
                                                                        pady=8,
                                                                        padx=7)
        Label(self.purchase_lf, text="Total Capital Invested  - ").grid(row=0,
                                                                        column=0,
                                                                        sticky=sty,
                                                                        pady=8,
                                                                        padx=7)
        Label(self.purchase_lf, text="Total Item Brought  - ").grid(row=2,
                                                                    column=0,
                                                                    sticky=sty,
                                                                    pady=8,
                                                                    padx=7)
        self.ib = Label(self.purchase_lf, text="0")
        self.ib.grid(row=2, column=1, sticky=sty, padx=2)
        self.ci = Label(self.purchase_lf, text="0")
        self.ci.grid(row=0, column=1, sticky=sty, padx=2)
        self.te = Label(self.purchase_lf, text="0")
        self.te.grid(row=1, column=1, sticky=sty, padx=2)
        self.Add2Mlb21()

    def Add2Mlb22(self):
        self.mlb22.delete(0, END)
        gp = 0
        pg = 0
        tis = 0
        ins = self.mlb22.insert
        if self.modify:
            row = self.db.sqldb.execute(
                """ SELECT selling_id,invoice_date,cost,sold_price,QTY FROM (SELECT * FROM
            sells JOIN invoices USING (invoice_id) )
                                            JOIN costs USING (cost_id) JOIN products USING (product_id) WHERE
                                            product_id = "%s" """ %
                (self.tup['values'][0])).fetchall()
            for i in row:
                i = list(i)
                date = i[1]
                cost = i[2]
                price = i[3]
                qty = i[4]
                profit = round(price - cost, 2)
                pg += (profit * qty)
                gp += price * qty
                tis += qty
                i.append(profit)
                ins(END, i)
        self.gp.configure(text=str(round(gp, 2)))
        self.pg.configure(text=str(round(pg, 2)))
        self.tis.configure(text=str(tis))

    def sells_edit(self, event):
        i = self.mlb22.tree.focus()
        if i is None:
            return showinfo("Message", "No Item Selected", parent=self.master)
        r = self.mlb22.tree.item(i)
        self.selid = r['values'][0]
        root13 = Toplevel()
        root13.title("Modificare vanzari")
        root13.grid()
        for i in range(8):
            root13.rowconfigure(i, weight=1)
        for i in range(2):
            root13.columnconfigure(i, weight=1)
        lf = root13
        self.salegui = root13
        color = 'gray98'
        root13['background'] = color
        Label(lf,
              text="Selling ID : %s" % (self.selid),
              foreground="#3496ff",
              font=('Berlin Sans FB Demi', 18)).grid(row=0,
                                                     column=0,
                                                     columnspan=2,
                                                     sticky=sty,
                                                     pady=8,
                                                     padx=7)

        r = self.db.sqldb.execute(
            """ SELECT invoice_date,invoice_no,QTY,cost,price,sold_price FROM (SELECT * FROM
        sells JOIN invoices USING (invoice_id) )
                                            JOIN costs USING (cost_id) JOIN products USING (product_id) WHERE
                                            selling_id = "%s" """ %
            self.selid).fetchone()
        # print(r)
        Label(lf, text="Selling Date", width=15).grid(row=1,
                                                      column=0,
                                                      sticky=sty,
                                                      pady=8,
                                                      padx=2)
        Label(lf, text="Invoice No").grid(row=2,
                                          column=0,
                                          sticky=sty,
                                          pady=8,
                                          padx=7)
        Label(lf, text="Quantity").grid(row=3,
                                        column=0,
                                        sticky=sty,
                                        pady=8,
                                        padx=7)
        Label(lf, text="Cost").grid(row=4,
                                    column=0,
                                    sticky=sty,
                                    pady=8,
                                    padx=7)
        Label(lf, text="Selling Price").grid(row=5,
                                             column=0,
                                             sticky=sty,
                                             pady=8,
                                             padx=7)
        Label(lf, text="Sold Price").grid(row=6,
                                          column=0,
                                          sticky=sty,
                                          pady=8,
                                          padx=7)
        self.seldate = CalendarButton(lf)
        self.seldate.grid(row=1, column=1, sticky=sty, pady=8, padx=7)
        try:
            self.seldate.insert(r['values'][0])
        except:
            self.seldate.insert(self.seldate.getTimeStamp())
        self.selinvno = Entry(lf, width=40)
        self.selinvno.grid(row=2, column=1, sticky=sty, pady=8, padx=7)
        self.selinvno.delete(0, END)
        self.selinvno.insert(0, int(r[1]))
        self.selinvno['state'] = "readonly"

        self.selqty = Entry(lf)
        self.selqty.grid(row=3, column=1, sticky=sty, pady=8, padx=7)
        self.selqty.delete(0, END)
        self.selqty.insert(0, int(r[2]))

        self.selcost = Entry(lf)
        self.selcost.grid(row=4, column=1, sticky=sty, pady=8, padx=7)
        self.selcost.delete(0, END)
        self.selcost.insert(0, r[3])

        self.selprice = Entry(lf)
        self.selprice.grid(row=5, column=1, sticky=sty, pady=8, padx=7)
        self.selprice.delete(0, END)
        self.selprice.insert(0, r[4])

        self.selsold = Entry(lf)
        self.selsold.grid(row=6, column=1, sticky=sty, pady=8, padx=7)
        self.selsold.delete(0, END)
        self.selsold.insert(0, r[5])

        Button(lf, text="save",
               command=lambda: self.sale_save()).grid(row=7,
                                                      column=1,
                                                      sticky=sty,
                                                      pady=8,
                                                      padx=7)
        root13.wait_window()
        return 1

    def sale_save(self):
        print(self.tup)
        PID = self.tup['values'][0]
        try:
            cost = float(Filter(self.selcost.get()))
            price = float(Filter(self.selprice.get()))
            sold = float(Filter(self.selsold.get()))
            qty = float(Filter(self.selqty.get()))
            invno = float(Filter(self.selinvno.get()))
            date = Filter(self.seldate.get())
        except:
            return showinfo(
                title="ERROR",
                message=
                'Costs,Price,Selling,Price,Invoice No And Qty must be numbers',
                parent=self.master)
        costid = self.db.sqldb.get_cost_id(PID, cost, price)
        if costid is None:
            costid = self.db.sqldb.add_new_cost(PID, cost, price)
        invid = self.db.sqldb.get_invoice_id(invno)
        if invid is None:
            return showinfo(title="ERROR",
                            message='Invoice In That Number Dsn\'t Exsist',
                            parent=self.master)
        # print(self.selid, sold, qty, costid)
        self.db.edit_sells(self.selid, sold, qty, costid)
        self.salegui.destroy()
        self.Add2Mlb22()
        return showinfo(title="Successful",
                        message='Changes Saved',
                        parent=self.master)

    def deletesells(self):
        i = self.mlb22.Select_index
        if i is None:
            return showinfo("Message", "No Item Selected", parent=self.master)
        r = self.mlb22.get(i)
        self.selid = r[0]
        ans = askokcancel("Message",
                          "Sure You Want To delete %s ?" % (self.selid),
                          parent=self.master)
        if ans:
            self.db.delete_sells(self.selid)
            return showinfo("Message",
                            "%s Has Been Successfully Deleted" % (self.selid),
                            parent=self.master), self.Add2Mlb22()
        return False

    def notepage_variants(self, note):
        self.variants_app.grid(row=0, column=0)
        for i in range(3):
            self.variants_app.rowconfigure(i, weight=1)
        for i in range(3):
            self.variants_app.columnconfigure(i, weight=1)
        note.add(self.variants_app, text=' Variatiuni ')
        Label(self.variants_app,
              text='Variatiuni ale Produsului',
              foreground="#3496ff",
              font=('Berlin Sans FB Demi', 25)).grid(row=0,
                                                     column=0,
                                                     columnspan=1,
                                                     sticky=sty,
                                                     pady=9
                                                     )
        self.btn_variants_delete.grid(row=0, column=2, sticky=sty, pady=20, padx=10)
        self.mlb_variants.grid(row=1, column=0, columnspan=3, sticky=sty)
        self.variation_lf.grid(row=2, column=0, columnspan=3, sticky=sty)
        self.label_new_variant_name.grid(row=1, column=0, columnspan=1, sticky=sty, pady=6)
        self.label_new_variant_value.grid(row=2, column=0, columnspan=1, sticky=sty, pady=6)
        self.label_new_variant_price_modifier.grid(row=3, column=0, columnspan=1, sticky=sty, pady=6)
        self.entry_new_variant_name.grid(row=1, column=1, columnspan=1, sticky=sty, pady=6)
        self.entry_new_variant_value.grid(row=2, column=1, columnspan=1, sticky=sty, pady=6)
        self.entry_new_variant_modifier.grid(row=3, column=1, columnspan=1, sticky=sty, pady=6)
        self.btn_variants_add.grid(row=4, column=0, columnspan=1, sticky=sty)
        self.btn_variants_edit.grid(row=4, column=1, columnspan=1, sticky=sty)
        self.mlb_variants_load()

    def notepage_sales(self, note):
        app2 = Frame(note)
        app2.grid(row=0, column=0)
        for i in range(3):
            app2.rowconfigure(i, weight=1)
        for i in range(3):
            app2.columnconfigure(i, weight=1)
        note.add(app2, text=' Vanzari ')
        Label(app2,
              text="Inregistrari vanzari",
              foreground="#3496ff",
              font=('Berlin Sans FB Demi', 25)).grid(row=0,
                                                     column=0,
                                                     columnspan=1,
                                                     sticky=sty,
                                                     pady=9)
        self.btn31 = Button(app2,
                            text="Edit Selling Records",
                            command=lambda: self.sells_edit(None))
        self.btn31.grid(row=0, column=1, sticky=sty, pady=20)
        self.btn32 = Button(app2,
                            text="Sterge vanzarea",
                            command=lambda: self.deletesells())
        self.btn32.grid(row=0, column=2, sticky=sty, pady=20, padx=10)

        self.mlb22 = MultiListbox(app2,
                                  (("Selling ID", 25), ("Sold Date", 35),
                                   ("Cost Price", 25), ("Sold Price", 25),
                                   ("Quantity", 15), ("Profit", 25)))
        self.mlb22.grid(row=1, column=0, columnspan=3, sticky=sty)
        self.mlb22.tree.bind('<Double-Button-1>', self.sells_edit)
        lf = Frame(app2)
        lf.grid(row=2, column=0, sticky=sty)
        Label(lf, text="Incasari totale pe produs  - ").grid(row=0,
                                                           column=0,
                                                           sticky=sty,
                                                           pady=8,
                                                           padx=7)
        self.gp = Label(lf, text="0")
        self.gp.grid(row=0, column=1, sticky=sty, padx=2)
        Label(lf, text="Total Profit  - ").grid(row=1,
                                                column=0,
                                                sticky=sty,
                                                pady=8,
                                                padx=7)
        self.pg = Label(lf, text="0")
        self.pg.grid(row=1, column=1, sticky=sty, padx=2)
        Label(lf, text="Total vanzare pe SKU  - ").grid(row=2,
                                                   column=0,
                                                   sticky=sty,
                                                   pady=8,
                                                   padx=7)
        self.tis = Label(lf, text="0")
        self.tis.grid(row=2, column=1, sticky=sty, padx=2)
        self.Add2Mlb22()

    def delete_variant(self):
        pass

    def add_variant(self, modify=False):
        variant_name = self.entry_new_variant_name.get()
        variant_value = self.entry_new_variant_value.get()
        variant_modifier = self.entry_new_variant_modifier.get()
        current_index = self.mlb_variants.Select_index
        r = self.mlb_variants.get(current_index)
        PID = self.tup['values'][0]
        if modify:
            if current_index is None:
                return showinfo("Message",
                                "Select a Cost Or Price To Edit",
                                parent=self.master)
            self.db.sqldb.edit_variant(PID, variant_name, variant_value, variant_modifier)
        else:
            try:
                self.db.sqldb.add_variant(PID, variant_name, variant_value, variant_modifier)
                showinfo('Succes', 'Variatia produsului a fost adaugata', parent=self.master)
                self.mlb_variants_load()
            except Exception as e:
                return showerror('Error', e, parent=self.master)


class ProductVariant():
    pass
