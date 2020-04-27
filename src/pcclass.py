import src.sqldatabase as sqldb
from tkinter.messagebox import showinfo


class DatabaseTypeError(Exception):
    pass


class IncompleteDataError(Exception):
    pass


class InvalidDataError(Exception):
    pass


class InventoryDataBase(object):
    def __init__(self):
        """

        """
        self.sqldb = sqldb.MyDatabase()

    def add_variant(self, PID, variant_name, variant_value, variant_modifier):
        return self.sqldb.add_variant(PID, variant_name, variant_value, variant_modifier)

    def edit_variant(self, PID, variant_name, variant_value, variant_modifier):
        return self.sqldb.edit_variant(PID, variant_name, variant_value, variant_modifier)

    def get_customer_names(self):
        """

        @return:
        """
        l = self.execute("SELECT customer_name FROM customers")
        l.sort()
        return l

    def getproductnames(self):
        """

        @return:
        """
        l = self.execute("SELECT product_name FROM products ")
        l.sort()
        return l

    def getcategorynames(self):
        """

        @return:
        """
        l = self.execute("SELECT category_name FROM category")
        a = sorted(l)
        return a

    def get_supplier_names(self):
        """

        @return:
        """
        l = self.execute("SELECT name FROM suppliers")
        a = sorted(l)
        return a

    def getinvoiceno(self):
        """

        @return:
        """
        l = self.execute("SELECT invoice_no FROM invoices")
        l.sort()
        return l

    customer_list = property(get_customer_names)
    product_list = property(getproductnames)
    categorylist = property(getcategorynames)
    invoice_list = property(getinvoiceno)
    get_supplier_names = property(get_supplier_names)

    def search_customer(self, likename):
        """

        @param likename:
        @return:
        """
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

    def search_product(self, likename):
        """

        @param likename:
        @return:
        """
        tup = tuple([likename] * 4)
        row = self.execute(""" SELECT product_name FROM products
                            LEFT OUTER JOIN 
                            category 
                            USING (
                            category_id)  WHERE
                            product_name LIKE "%%%s%%"   OR
                            product_id  LIKE  "%%%s%%"  OR
                            product_description LIKE  "%%%s%%" OR
                            category_name LIKE "%%%s%%" """ % tup)
        return row

    def search_sales_invoice(self, like_name):
        """

        @param like_name:
        @return:
        """
        row = self.execute(""" select distinct for_invoice from purchase where for_invoice LIKE "%%%s%%" """ %
                           like_name)
        return row

    def search_category(self, likename):
        """

        @param likename:
        @return:
        """
        tup = tuple([likename] * 4)
        row = self.execute(""" SELECT category_name FROM category LEFT OUTER  JOIN products USING (category_id) WHERE
                                 product_name LIKE "%%%s%%"   OR 
                                 product_id  LIKE  "%%%s%%"  OR
                                 product_description LIKE  "%%%s%%"  OR
                                 category_name LIKE "%%%s%%" """ % tup)
        return row

    def search_invoice(self, likename):
        """

        @param likename:
        @return:
        """
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
        """

        @param query:
        @return:
        """
        row = self.sqldb.execute(query)
        lisr = set(row.fetchall())
        lisr = map(lambda x: x[0], lisr)
        return lisr

    def commit(self):
        """

        @return:
        """
        return self.sqldb.commit()

    def save(self):
        """

        @return:
        """
        self.commit()
        return showinfo("Info", "All Changes has Been Saved")

    def close(self):
        """

        @return:
        """
        return self.sqldb.close()

    def add_product_and_cost(self, name, category, description, cost, price, lot):
        """

        @param name:
        @param category:
        @param description:
        @param cost:
        @param price:
        @param lot:
        @return:
        """
        name = name.title()
        category = category.title()
        cost = round(float(cost), 2)
        price = round(float(price), 2)
        lot = lot.title()
        PID = self.sqldb.add_product(name, description, category, lot)
        costid = self.sqldb.add_new_cost(PID, cost, price)
        return costid

    def add_product(self, name, category, description, um, tva):
        """

        @param name:
        @param category:
        @param description:
        @param um:
        @return:
        """
        name = name.title()
        category = category.title()
        um = um.title()
        tva = tva.title()
        return self.sqldb.add_product(name, description, category, um, tva)

    def edit_product(self, PID, name, category, description, um):
        """

        @param PID:
        @param name:
        @param category:
        @param description:
        @param um:
        @return:
        """
        name = name.title()
        category = category.title()
        um = um.title()
        catid = self.sqldb.getcategory_id(category)
        umid = self.sqldb.get_um_id(um)
        if catid is None:
            catid = self.add_category(category)
        if umid is None:
            umid = self.add_um(um)
        self.sqldb.edit_product(PID, 1, name)
        self.sqldb.edit_product(PID, 2, description)
        self.sqldb.edit_product(PID, 3, catid)
        self.sqldb.edit_product(PID, 4, umid)
        return True

    def delete_product(self, PID):
        """

        @param PID:
        @return:
        """
        if PID != None:
            return self.sqldb.delete_product(PID)
        return False

    def add_cost(self, name, cost, price):
        """

        @param name:
        @param cost:
        @param price:
        @return:
        """
        name = name.title()
        cost = round(float(cost), 2)
        price = round(float(price), 2)
        PID = self.sqldb.get_product_id(name)
        return self.sqldb.add_new_cost(PID, cost, price)

    def edit_costs(self, costid, PID, cost, price):
        """

        @param costid:
        @param PID:
        @param cost:
        @param price:
        @return:
        """
        cost = round(float(cost), 2)
        price = round(float(price), 2)
        self.sqldb.edit_cost(costid, 1, PID)
        self.sqldb.edit_cost(costid, 2, cost)
        self.sqldb.edit_cost(costid, 3, price)
        return True

    def add_category(self, newcategory):
        """

        @param newcategory:
        @return:
        """
        newcategory = newcategory.title()
        return self.sqldb.add_category(newcategory)

    def add_um(self, um):
        """

        @param um:
        @return:
        """
        newum = um.title()
        return self.sqldb.add_um(newum)

    def edit_category_name(self, previousname, newcategory):
        """

        @param previousname:
        @param newcategory:
        @return:
        """
        newcategory = newcategory.title()
        catid = self.sqldb.getcategory_id(previousname)
        return self.sqldb.edit_category(catid, newcategory)

    def delete_category(self, category):
        """

        @param category:
        @return:
        """
        catid = self.sqldb.getcategory_id(category)
        return self.sqldb.delete_category(catid)

    def delete_um(self, um):
        """

        @param um:
        @return:
        """
        umid = self.sqldb.get_um_id(um)
        return self.sqldb.delete_um(umid)

    def add_phone(self, phone, ctmid):
        """

        @param phone:
        @param ctmid:
        @return:
        """
        # if not phone.isnumeric():
        #     raise Exception("Phone Number Not Valid")
        return self.sqldb.add_phone(phone, ctmid)

    def edit_phone(self, phnid, phone, ctmid):
        """

        @param phnid:
        @param phone:
        @param ctmid:
        @return:
        """
        ph = self.sqldb.get_phone_id(phone)
        if ph != None:
            raise Exception("Phone Number Already Listed")
        self.sqldb.edit_phone(phnid, 1, phone)
        self.sqldb.edit_phone(phnid, 2, ctmid)
        return None

    def delete_phone(self, phnid):
        """

        @param phnid:
        @return:
        """
        return self.sqldb.delete_phone(phnid)

    def add_customer(self, name, address, email, ro, cui, cnp):
        """

        @param name:
        @param address:
        @param email:
        @param ro:
        @param cui:
        @param cnp:
        @return:
        """
        name = name.title()
        return self.sqldb.add_new_customer(name, address, email, ro, cui, cnp)

    def edit_customer(self, ctmid, newname, address, email, ro):
        """

        @param ctmid:
        @param newname:
        @param address:
        @param email:
        @param ro:
        @return:
        """
        newname = newname.title()
        if ctmid == None:
            raise Exception("Not a Valid Customer")
        self.sqldb.edit_customer(ctmid, 1, newname)
        self.sqldb.edit_customer(ctmid, 2, address)
        self.sqldb.edit_customer(ctmid, 3, email)
        self.sqldb.edit_customer(ctmid, 4, ro)
        return True

    def delete_customer(self, ctmid, phone=False):
        """

        @param ctmid:
        @param phone:
        @return:
        """
        if phone:
            ctmid = self.sqldb.get_customer_id(ctmid)
        return self.sqldb.delete_customer(ctmid)

    def add_invoice(self, ctmid, no, paid, date):
        """

        @param ctmid:
        @param no:
        @param paid:
        @param date:
        @return:
        """
        paid = round(float(paid), 2)
        no = round(float(no), 1)
        return self.sqldb.add_new_invoice(ctmid, no, date, paid)

    def edit_invoice(self, inv_id, ctmid, no, date):
        """

        @param inv_id:
        @param ctmid:
        @param no:
        @param date:
        @return:
        """
        no = int(no)
        date = " ".join(date.split())
        self.sqldb.edit_invoice(inv_id, 1, ctmid)
        self.sqldb.edit_invoice(inv_id, 2, no)
        self.sqldb.edit_invoice(inv_id, 4, date)
        return True

    def delete_invoice(self, inv_id):
        """

        @param inv_id:
        @return:
        """
        return self.sqldb.delete_invoice(inv_id)

    def add_purchase(self, pid, costid, date, qty, lot, pentru_factura, supplier):
        """

        @param pid:
        @param costid:
        @param date:
        @param qty:
        @param lot:
        @param pentru_factura:
        @param supplier:
        @return:
        """
        return self.sqldb.add_new_purchase(pid, costid, date, qty, lot, pentru_factura, supplier)

    def edit_purchase(self, purid, costid, qty, date):
        """

        @param purid:
        @param costid:
        @param qty:
        @param date:
        @return:
        """
        qty = int(qty)
        date = " ".join(date.split())
        self.sqldb.edit_purchase(purid, 1, costid)
        self.sqldb.edit_purchase(purid, 2, qty)
        self.sqldb.edit_purchase(purid, 3, date)
        return True

    def delete_purchase(self, purid):
        """

        @param purid:
        @return:
        """
        return self.sqldb.delete_purchase(purid)

    def add_sells(self, costid, sold, invid, qty):
        """

        @param costid:
        @param sold:
        @param invid:
        @param qty:
        @return:
        """
        sold = round(float(sold), 2)
        qty = round(float(qty), 1)
        return self.sqldb.add_new_sell(invid, sold, qty, costid)

    def edit_sells(self, selid, sold, qty, costid):
        """

        @param selid:
        @param sold:
        @param qty:
        @param costid:
        @return:
        """
        sold = round(float(sold), 2)
        qty = round(float(qty), 1)
        self.sqldb.edit_sells(selid, 2, sold)
        self.sqldb.edit_sells(selid, 3, qty)
        self.sqldb.edit_sells(selid, 4, costid)
        return True

    def delete_sells(self, selid):
        """

        @param selid:
        @return:
        """
        return self.sqldb.delete_sells(selid)

    def get_all_sell_id(self, invid):
        """

        @param invid:
        @return:
        """
        row = self.execute("""SELECT selling_id FROM sells WHERE invoice_id = "%s"
                                    """ % invid)
        return row

    def get_any_cost_id(self, PID, price):
        """

        @param PID:
        @param price:
        @return:
        """
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

    def edit_invoice_with_paid(self, invid, ctmid, paid, no, date):
        """

        @param invid:
        @param ctmid:
        @param paid:
        @param no:
        @param date:
        @return:
        """
        no = int(no)
        paid = round(float(paid), 2)
        date = " ".join(date.split())
        self.sqldb.edit_invoice(invid, 1, ctmid)
        self.sqldb.edit_invoice(invid, 2, no)
        self.sqldb.edit_invoice(invid, 3, paid)
        self.sqldb.edit_invoice(invid, 4, date)
        return True

    def get_phones(self, ctmid):
        """

        @param ctmid:
        @return:
        """
        row = self.execute("""SELECT phone_no FROM contacts WHERE customer_id = "%s"
                                    """ % (ctmid))
        return row

    def Save(self):
        """

        """
        self.sqldb.commit()

    def load(self, fname):
        """

        @param fname:
        """
        pass

    def add_supplier(self, name, ro, cui, address, phone):
        """

        @param name:
        @param ro:
        @param cui:
        @param address:
        @param phone:
        @return:
        """
        name = name.title()
        ro = ro.title()
        cui = cui.title()
        address = address.title()
        phone = phone.title()
        return self.sqldb.add_supplier(name, ro, cui, address, phone)

    def search_supplier(self, fst):
        """

        @rtype: object
        @param fst:
        @return:
        """
        row = self.execute(""" SELECT name FROM suppliers WHERE
                                         name LIKE "%%%s%%" """ % fst)
        return row

    def search_um(self, param):
        """

        @param param:
        @return:
        """
        row = self.execute(""" SELECT name FROM units_of_measure WHERE name LIKE "%%%s%%" """ % param)
        return row

    def get_supplier(self, supplier):
        """

        @param supplier:
        @return:
        """
        row = self.sqldb.execute(""" select * from suppliers where name = "%s" """ % supplier).fetchone()
        return row

    def add_products_to_purchase(self, pur_id, costid, date, qty, lot, pid, variant, expiry_date):
        """

        @param pur_id:
        @param costid:
        @param date:
        @param qty:
        @param lot:
        @param pid:
        @param variant
        @return:
        """
        return self.sqldb.add_products_to_purchase(pur_id, costid, date, qty, lot, pid, variant, expiry_date)

    def deplete_qty(self, product_lot, product_qty, product_name, variant):
        """

        @param product_lot:
        @param product_qty:
        """
        return self.sqldb.deplete_qty(product_lot, product_qty, product_name, variant)

