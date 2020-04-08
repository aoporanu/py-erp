import Src.sqldatabase as sqldb
from tkinter.messagebox import showinfo


class DatabaseTypeError(Exception):
    pass


class IncompleteDataError(Exception):
    pass


class InvalidDataError(Exception):
    pass


class InventoryDataBase(object):
    def __init__(self):
        self.sqldb = sqldb.MyDatabase()

    def getcustomernames(self):
        l = self.execute("SELECT customer_name FROM customers")
        l.sort()
        return l

    def getproductnames(self):
        l = self.execute("SELECT product_name FROM products ")
        l.sort()
        return l

    def getcategorynames(self):
        l = self.execute("SELECT category_name FROM category")
        a = sorted(l)
        return a

    def get_supplier_names(self):
        l = self.execute("SELECT name FROM suppliers")
        a = sorted(l)
        return a

    def getinvoiceno(self):
        l = self.execute("SELECT invoice_no FROM invoices")
        l.sort()
        return l

    customerlist = property(getcustomernames)
    productlist = property(getproductnames)
    categorylist = property(getcategorynames)
    invoicelist = property(getinvoiceno)
    get_supplier_names = property(get_supplier_names)

    def searchcustomer(self, likename):
        tup = tuple([likename] * 8)
        row = self.execute(""" SELECT customer_name FROM customers LEFT OUTER JOIN invoices USING (customer_id)
                             LEFT OUTER JOIN contacts USING (customer_id) WHERE
                                 customer_name LIKE "%%%s%%"
                                 OR customer_address LIKE  "%%%s%%"
                                 OR  customers.customer_id LIKE  "%%%s%%"
                                 OR customer_email LIKE "%%%s%%"
                                 OR invoice_no LIKE "%%%s%%"
                                 OR customer_cui LIKE "%%%s%%"
                                 OR customer_cnp LIKE "%%%s%%"
                                 OR phone_no LIKE "%%%s%%" """ % tup)
        return row

    def searchproduct(self, likename):
        tup = tuple([likename] * 4)
        row = self.execute(""" SELECT product_name FROM products  LEFT OUTER JOIN category USING (category_id)  WHERE
                                 product_name LIKE "%%%s%%"   OR
                                 product_id  LIKE  "%%%s%%"  OR
                                 product_description LIKE  "%%%s%%" OR
                                 category_name LIKE "%%%s%%" """ % tup)
        return row

    def search_sales_invoice(self, like_name):
        row = self.execute(""" select distinct for_invoice from purchase where for_invoice LIKE "%%%s%%" """ %
                           like_name)
        return row

    def searchcategory(self, likename):
        tup = tuple([likename] * 4)
        row = self.execute(""" SELECT category_name FROM category LEFT OUTER  JOIN products USING (category_id) WHERE
                                 product_name LIKE "%%%s%%"   OR 
                                 product_id  LIKE  "%%%s%%"  OR
                                 product_description LIKE  "%%%s%%"  OR
                                 category_name LIKE "%%%s%%" """ % tup)
        return row

    def searchinvoice(self, likename):
        tup = tuple([likename] * 5)
        row = self.execute(""" SELECT invoice_no FROM customers  LEFT OUTER JOIN invoices USING (customer_id) WHERE
                                 customer_name LIKE "%%%s%%"   OR 
                                 customer_id  LIKE  "%%%s%%"  OR
                                 customer_address LIKE  "%%%s%%"  OR 
                                 customer_email LIKE "%%%s%%" OR
                                 customer_ro LIKE  "%%%s%%" OR
                                 invoice_no LIKE "%%%s%%" """ % tup)
        return row

    def execute(self, query):  # use this only for fetchall and one element in every row
        row = self.sqldb.execute(query)
        lisr = set(row.fetchall())
        lisr = map(lambda x: x[0], lisr)
        return lisr

    def commit(self):
        return self.sqldb.commit()

    def save(self):
        self.commit()
        return showinfo("Info", "All Changes has Been Saved")

    def close(self):
        return self.sqldb.close()

    def addproduct_and_cost(self, name, category, description, cost, price, lot):
        name = name.title()
        category = category.title()
        cost = round(float(cost), 2)
        price = round(float(price), 2)
        lot = lot.title()
        PID = self.sqldb.addproduct(name, description, category, lot)
        costid = self.sqldb.addnewcost(PID, cost, price)
        return costid

    def addproduct(self, name, category, description, um):
        name = name.title()
        category = category.title()
        um = um.title()
        return self.sqldb.addproduct(name, description, category, um)

    def editproduct(self, PID, name, category, description, um):
        name = name.title()
        category = category.title()
        um = um.title()
        catid = self.sqldb.getcategory_id(category)
        umid = self.sqldb.get_um_id(um)
        if catid is None:
            catid = self.addcategory(category)
        if umid is None:
            umid = self.add_um(um)
        self.sqldb.editproduct(PID, 1, name)
        self.sqldb.editproduct(PID, 2, description)
        self.sqldb.editproduct(PID, 3, catid)
        self.sqldb.editproduct(PID, 4, umid)
        return True

    def deleteproduct(self, PID):
        if PID != None:
            return self.sqldb.deleteproduct(PID)
        return False

    def addcost(self, name, cost, price):
        name = name.title()
        cost = round(float(cost), 2)
        price = round(float(price), 2)
        PID = self.sqldb.getproductID(name)
        return self.sqldb.addnewcost(PID, cost, price)

    def editcosts(self, costid, PID, cost, price):
        cost = round(float(cost), 2)
        price = round(float(price), 2)
        self.sqldb.editcost(costid, 1, PID)
        self.sqldb.editcost(costid, 2, cost)
        self.sqldb.editcost(costid, 3, price)
        return True

    def addcategory(self, newcategory):
        newcategory = newcategory.title()
        return self.sqldb.addcategory(newcategory)

    def add_um(self, um):
        newum = um.title()
        return self.sqldb.add_um(newum)

    def editcategoryname(self, previousname, newcategory):
        newcategory = newcategory.title()
        catid = self.sqldb.getcategory_id(previousname)
        return self.sqldb.editcategory(catid, newcategory)

    def deletecategory(self, category):
        catid = self.sqldb.getcategory_id(category)
        return self.sqldb.deletecategory(catid)

    def delete_um(self, um):
        umid = self.sqldb.get_um_id(um)
        return self.sqldb.delete_um(umid)

    def addphone(self, phone, ctmid):
        # if not phone.isnumeric():
        #     raise Exception("Phone Number Not Valid")
        return self.sqldb.add_phone(phone, ctmid)

    def editphone(self, phnid, phone, ctmid):
        ph = self.sqldb.get_phone_ID(phone)
        if ph != None:
            raise Exception("Phone Number Already Listed")
        self.sqldb.edit_phone(phnid, 1, phone)
        self.sqldb.edit_phone(phnid, 2, ctmid)
        return None

    def deletephone(self, phnid):
        return self.sqldb.delete_phone(phnid)

    def addcustomer(self, name, address, email, ro, cui, cnp):
        name = name.title()
        return self.sqldb.add_new_customer(name, address, email, ro, cui, cnp)

    def editcustomer(self, ctmid, newname, address, email, ro):
        newname = newname.title()
        if ctmid == None:
            raise Exception("Not a Valid Customer")
        self.sqldb.edit_customer(ctmid, 1, newname)
        self.sqldb.edit_customer(ctmid, 2, address)
        self.sqldb.edit_customer(ctmid, 3, email)
        self.sqldb.edit_customer(ctmid, 4, ro)
        return True

    def deletecustomer(self, ctmid, phone=False):
        if phone == True:
            ctmid = self.sqldb.get_customer_ID(ctmid)
        return self.sqldb.delete_customer(ctmid)

    def addinvoice(self, ctmid, no, paid, date):
        paid = round(float(paid), 2)
        no = round(float(no), 1)
        return self.sqldb.add_new_invoice(ctmid, no, date, paid)

    def editinvoice(self, invid, ctmid, no, date):
        no = int(no)
        date = " ".join(date.split())
        self.sqldb.edit_invoice(invid, 1, ctmid)
        self.sqldb.edit_invoice(invid, 2, no)
        self.sqldb.edit_invoice(invid, 4, date)
        return True

    def deleteinvoice(self, invid):
        return self.sqldb.delete_invoice(invid)

    def addpurchase(self, PID, costid, date, qty, lot, pentru_factura, supplier):
        return self.sqldb.add_new_purchase(PID, costid, date, qty, lot, pentru_factura, supplier)

    def editpurchase(self, purid, costid, qty, date):
        qty = int(qty)
        date = " ".join(date.split())
        self.sqldb.edit_purchase(purid, 1, costid)
        self.sqldb.edit_purchase(purid, 2, qty)
        self.sqldb.edit_purchase(purid, 3, date)
        return True

    def deletepurchase(self, purid):
        return self.sqldb.delete_purchase(purid)

    def addsells(self, costid, sold, invid, qty):
        sold = round(float(sold), 2)
        qty = round(float(qty), 1)
        return self.sqldb.add_new_sell(invid, sold, qty, costid)

    def editsells(self, selid, sold, qty, costid):
        sold = round(float(sold), 2)
        qty = round(float(qty), 1)
        self.sqldb.edit_sells(selid, 2, sold)
        self.sqldb.edit_sells(selid, 3, qty)
        self.sqldb.edit_sells(selid, 4, costid)
        return True

    def deletesells(self, selid):
        return self.sqldb.delete_sells(selid)

    def getallsellID(self, invid):
        row = self.execute("""SELECT selling_id FROM sells WHERE invoice_id = "%s"
                                    """ % invid)
        return row

    def getanycostid(self, PID, price):
        costid = self.execute("""SELECT cost_id FROM costs WHERE product_id = "%s"
                                    AND price = %.2f """ % (PID, price))
        for i in costid:
            qty = self.sqldb.get_cost_quantity(i)
            if qty > 0:
                return i
        costid = self.execute("""SELECT cost_id FROM costs WHERE product_id = "%s" """ % (PID))
        for i in costid:
            qty = self.sqldb.get_cost_quantity(i)
            if qty > 0:
                return i
        return None

    def editinvoice_withpaid(self, invid, ctmid, paid, no, date):
        no = int(no)
        paid = round(float(paid), 2)
        date = " ".join(date.split())
        self.sqldb.edit_invoice(invid, 1, ctmid)
        self.sqldb.edit_invoice(invid, 2, no)
        self.sqldb.edit_invoice(invid, 3, paid)
        self.sqldb.edit_invoice(invid, 4, date)
        return True

    def getphoneS(self, ctmid):
        row = self.execute("""SELECT phone_no FROM contacts WHERE customer_id = "%s"
                                    """ % (ctmid))
        return row

    def Save(self):
        self.sqldb.commit()

    def load(self, fname):
        pass

    def add_supplier(self, name, ro, cui, address, phone):
        name = name.title()
        ro = ro.title()
        cui = cui.title()
        address = address.title()
        phone = phone.title()
        return self.sqldb.add_supplier(name, ro, cui, address, phone)

    def search_supplier(self, fst):
        row = self.execute(""" SELECT name FROM suppliers WHERE
                                         name LIKE "%%%s%%" """ % fst)
        return row

    def search_um(self, param):
        row = self.execute(""" SELECT name FROM units_of_measure WHERE name LIKE "%%%s%%" """ % param)
        return row
