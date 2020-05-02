import sqlite3 as sqldb
import time as t


def new_database_create(conn):
    conn.execute("PRAGMA foreign_keys")
    conn.execute("""CREATE TABLE IF NOT EXISTS category(
                 category_id TEXT UNIQUE PRIMARY KEY NOT NULL,
                 category_name TEXT NOT NULL UNIQUE); """)

    conn.execute("""CREATE TABLE IF NOT EXISTS products(
                 product_id TEXT UNIQUE PRIMARY KEY NOT NULL,
                 product_name TEXT NOT NULL UNIQUE,
                 product_description TEXT,
                 product_tva TEXT,
                 um_id TEXT NOT NULL REFERENCES units_of_measure(id),
                 category_id TEXT NOT NULL REFERENCES category(category_id)); """)

    conn.execute("""CREATE TABLE IF NOT EXISTS units_of_measure(
                id TEXT UNIQUE PRIMARY KEY NOT NULL,
                name TEXT NOT NULL UNIQUE,
                created_on TEXT NOT NULL DEFAULT CURRENT_DATE); """)

    conn.execute("""CREATE TABLE IF NOT EXISTS costs(
                 cost_id TEXT UNIQUE PRIMARY KEY NOT NULL,
                 product_id TEXT NOT NULL REFERENCES products(product_id) ,
                 cost FLOAT NOT NULL DEFAULT 0.0,
                 price FLOAT NOT NULL DEFAULT 0.0); """)

    conn.execute("""CREATE TABLE IF NOT EXISTS purchase(
                 purchase_id TEXT UNIQUE PRIMARY KEY NOT NULL,
                 cost_id TEXT NOT NULL REFERENCES costs(cost_id) ,
                 QTY INT NOT NULL DEFAULT 1,
                 lot TEXT,
                 supplier_id TEXT REFERENCES suppliers(id),
                 for_invoice TEXT NOT NULL,
                 purchase_date TEXT NOT NULL DEFAULT CURRENT_DATE); """)

    conn.execute("""create table if not exists purchased_products(
                id integer primary key autoincrement not null,
                cost_id text not null references costs(cost_id),
                purchase_id text not null references purchase(purchase_id),
                product_id text not null references products(product_id),
                qty_purchased int not null default 1,
                lot text,
                variant text,
                purchased_date text not null default current_date);""")

    conn.execute("""CREATE TABLE IF NOT EXISTS suppliers(
                id TEXT UNIQUE PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                phone TEXT NOT NULL,
                cui TEXT NOT NULL,
                ro TEXT NOT NULL,
                created_on TEXT NOT NULL DEFAULT CURRENT_DATE); """)

    conn.execute("""create table if not exists product_variants(
                variant_id text unique primary key not null,
                name text not null,
                product_id text not null references products(product_id),
                created_on text not null default current_date);""")

    conn.execute("""create table if not exists variants_options(
                option_id TEXT UNIQUE PRIMARY KEY NOT NULL,
                value TEXT NOT NULL,
                variant_id text not null references product_variants(variant_id),
                modifier TEXT default '0',
                created_on text not null default current_date);""")

    conn.execute(""" create table if not exists product_variant_option(
                id TEXT UNIQUE PRIMARY KEY NOT NULL,
                product_id TEXT NOT NULL REFERENCES products(product_id),
                variant_id TEXT NOT NULL REFERENCES products_variants(variant_id),
                option_id TEXT NOT NULL REFERENCES variants_options(option_id),
                created_on TEXT NOT NULL DEFAULT CURRENT_DATE
                );""")

    conn.execute("""CREATE TABLE IF NOT EXISTS customers(
                 customer_id TEXT UNIQUE PRIMARY KEY NOT NULL,
                 customer_name TEXT NOT NULL ,
                 customer_address TEXT ,
                 customer_email TEXT ,
                 customer_cui TEXT,
                 delegate_id TEXT NOT NULL REFERENCES delegates(id),
                 customer_cnp TEXT); """)

    conn.execute("""CREATE TABLE IF NOT EXISTS contacts(
                 phone_id TEXT UNIQUE PRIMARY KEY NOT NULL,
                 phone_no TEXT UNIQUE NOT NULL,
                 customer_id TEXT NOT NULL REFERENCES customers(customer_id)); """)

    conn.execute("""CREATE TABLE IF NOT EXISTS invoices(
                 invoice_id TEXT UNIQUE PRIMARY KEY NOT NULL,
                 customer_id TEXT NOT NULL REFERENCES customers(customer_id),
                 invoice_no INT NOT NULL UNIQUE,
                 paid FLOAT NOT NULL ,
                 invoice_date TEXT NOT NULL DEFAULT CURRENT_DATE ); """)

    conn.execute("""CREATE TABLE IF NOT EXISTS sells(
                 selling_id TEXT UNIQUE PRIMARY KEY NOT NULL,
                 invoice_id TEXT NOT NULL REFERENCES invoices(invoice_id),
                 sold_price FLOAT NOT NULL ,
                 QTY INT NOT NULL ,
                 cost_id TEXT NOT NULL REFERENCES costs(cost_id)); """)

    conn.execute("""CREATE TABLE IF NOT EXISTS details( company_name TEXT,
                 company_email TEXT,
                 company_address TEXT,
                 company_phone TEXT,
                 company_website TEXT,
                 company_header TEXT,
                 company_footer TEXT,
                 currency TEXT,
                 pic_address TEXT,
                 invoice_start_no INT,
                 sgst_rate INT,
                 cgst_rate INT);""")
    conn.execute("""
                create table if not exists delegates(
                id TEXT UNIQUE PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                customer_id TEXT NOT NULL REFERENCES customers(customer_id),
                cnp TEXT NOT NULL,
                car_no TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_DATE); """)
    conn.execute(""" create table if not exists `batches`(
                id text unique primary key not null,
                name text not null,
                batch_qty text not null,
                purchase_id text not null references purchase(purchase_id),
                product_id text not null references purchased_products(product_id),
                expiry_date text not null default CURRENT_DATE,
                created_at text not null default CURRENT_DATE
    ); """)

    # conn.execute(""" alter table products add tva text default '9'""")

    if conn.execute("SELECT count(*) FROM details").fetchone()[0] == 0:
        conn.execute("INSERT INTO details VALUES('','','','','','','','Rs','logo.png',0,0,0)")
    conn.commit()
    return 1


class IDPresentError(Exception):
    pass


class MyDatabase(object):
    def __init__(self):

        self.connection = sqldb.connect("Database.db")
        # self.connection.set_trace_callback(print)
        new_database_create(self.connection)
        self.cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def execute(self, query):
        return self.cursor.execute(query)

    def get_cell(self, table_name, row_name, column_name, rowid):
        sqldb.enable_callback_tracebacks(True)
        row = self.cursor.execute(
            """SELECT %s FROM %s WHERE %s = "%s" """ % (column_name, table_name, row_name, rowid)).fetchone()
        if row is None:
            return None
        return row[0]

    def get_expiration_date_for_lot(self, lot_name):
        row = self.cursor.execute(""" SELECT expiry_date FROM `batches` WHERE name LIKE "%s" """ % lot_name).fetchone()
        if row is None:
            return None
        return row

    def get_purchase_doc_for_invoice(self, for_factura):
        """

        @param for_factura:
        @return:
        """
        row = self.cursor.execute(
            """ select purchase_id from purchase where for_invoice="%s" """ % for_factura
        ).fetchone()
        if row:
            return True
        return None

    def set_cell(self, table_name, row_name, column_name, rowid, value):
        self.cursor.execute(
            """UPDATE %s SET %s = %s  WHERE %s = "%s" """ % (table_name, column_name, value, row_name, rowid))

    def get_um_for_product(self, pid):
        l = self.execute(""" select * from units_of_measure where id = (select um_id from products
        where product_id= "%s")""" % pid).fetchone()
        return l

    def get_delegate_for(self, customer_id):
        l = self.execute(""" select * from delegates where customer_id= "%s" """ % customer_id)
        row = l.fetchone()
        return row

    def print_p_table_get_products(self, item):
        stmt = ""
        l = self.execute(""" SELECT products.product_id,product_name,category_name,product_description,
        units_of_measure.name FROM
        products
                        JOIN category USING (category_id) 
                        join units_of_measure on products.um_id=units_of_measure.id
                        JOIN `batches` ON batches.product_id=products.product_id
                        WHERE
                        product_name LIKE
                        "%s" """ % item).fetchall()
        # print(l)
        return l

    def get_products(self, inp):
        l = self.execute("""SELECT
        cost,price,category_name,product_description,products.product_id as
        prod_id, product_variants.name as 
        variant_name,
        purchased_products.lot,
        tva
        FROM
        costs JOIN products USING (product_id) JOIN purchase on products.product_id = prod_id
        JOIN batches USING (purchase_id) 
                JOIN purchased_products using(purchase_id)
                JOIN category USING (category_id) 
                join product_variants using(product_id) 
                join variants_options using(variant_id) WHERE 
                product_name LIKE "%s" """
                         % inp).fetchone()
        return l

    def get_products_if_first_is_none(self, inp):
        l = self.execute("""SELECT 
            category_name,
            product_description,
            cost,
            price,
            tva
            from products
            join product_variants using (product_id)
            JOIN variants_options using (variant_id)
            JOIN costs USING (product_id)
                JOIN category USING (category_id) WHERE product_name LIKE  "%s"
                         """ % inp).fetchone()
        return l

    def add_category(self, category):
        catid = "CAT" + str(hash(category + hex(int(t.time() * 10000))))
        self.cursor.execute(
            """INSERT INTO category (category_id,category_name) VALUES ("%s","%s") """ % (catid, category))
        return catid

    def edit_category(self, catid, new_name):
        self.cursor.execute(
            """UPDATE category SET category_name = "%s" WHERE category_id = "%s" """ % (new_name, catid))
        return True

    def getcategory_id(self, category):
        row = self.cursor.execute("""SELECT category_id FROM category WHERE category_name = "%s" """ % category)
        catid = row.fetchone()
        if catid is None:
            return catid
        return catid[0]

    def get_um_id(self, um):
        row = self.cursor.execute("""select id from units_of_measure WHERE name = "%s" """ % um)
        umid = row.fetchone()
        if umid is None:
            return umid
        return umid[0]

    def delete_category(self, catid):
        row = self.cursor.execute("""SELECT product_id FROM products WHERE category_id = "%s" """ % catid)
        i = row.fetchone()
        if i is None:
            self.cursor.execute("""DELETE FROM category WHERE category_id = "%s" """ % catid)
            return True
        return False

    def get_product_id(self, name):
        row = self.cursor.execute("""SELECT product_id FROM products WHERE product_name = "%s" """ % name)
        pid = row.fetchone()
        if pid is None:
            return pid
        return pid[0]

    def add_product(self, name, description, category, um, tva):
        prod_id = "PDT" + str(hash(name + hex(int(t.time() * 10000))))
        catid = self.getcategory_id(category)
        umid = self.get_um_id(um)
        if catid is None:
            catid = self.add_category(category)
        if umid is None:
            umid = self.add_um(um)
        if self.get_product_id(name) is not None:
            raise Exception("Product already listed")
        self.cursor.execute(
            """INSERT INTO products (product_id,product_name,product_description,category_id, um_id, tva) VALUES ("%s",
            "%s","%s",
            "%s", "%s", "%s")""" % (
                prod_id, name, description, catid, umid, tva))
        return prod_id

    def edit_product(self, pid, attribute, value):
        """attribute -> name or 1 , description or 2, category_id or 3 """
        dic = {1: "product_name", 2: "product_description", 3: "category_id", 4: "um_id"}
        if type(attribute) == int:
            attribute = dic[attribute]
        row = self.cursor.execute("""SELECT %s FROM products WHERE product_id = "%s" """ % (attribute, pid))
        row = row.fetchone()
        if row[0] == value:
            return False
        self.cursor.execute("""UPDATE products SET %s = "%s" WHERE product_id = "%s" """ % (attribute, value, pid))
        return True

    def delete_product(self, pid):
        row = self.cursor.execute("""SELECT cost_id FROM costs WHERE product_id = "%s" """ % pid)
        i = row.fetchone()
        if i is None:
            self.cursor.execute("""DELETE FROM products WHERE product_id = "%s" """ % pid)
            return True
        return False

    def get_cost_id(self, pid, lot, cost, price):
        row = self.cursor.execute(
            """SELECT cost_id FROM costs WHERE product_id = "%s" AND `batch_id`="%s" AND cost = %f AND price = %f """ % (pid, lot, cost, price))
        iid = row.fetchone()
        if iid is None:
            return iid
        return iid[0]

    def add_new_cost(self, pid, lot, cost, price):
        s = str(pid) + str(cost) + str(price) + hex(int(t.time() * 10000))
        costid = "CST" + str(hash(s))
        if self.get_cost_id(pid, lot, cost, price) is not None:
            raise Exception("""cost already listed""")
        self.cursor.execute("""INSERT INTO costs (cost_id,product_id,batch_id,cost,price) VALUES ("%s","%s","%s",%.2f,%.2f)""" % (
            costid, pid, lot, cost, price))
        return costid

    def edit_cost(self, costid, attribute, value):
        """attribute -> product_id or 1 , cost or 2 , price or 3 """
        dic = {1: "product_id", 2: "cost", 3: "price"}
        if type(attribute) == int:
            attribute = dic[attribute]
        row = self.cursor.execute("""SELECT %s FROM costs WHERE cost_id = "%s" """ % (attribute, costid))
        row = row.fetchone()
        if row[0] == value:
            return False
        if attribute == "product_id":
            value = "\"" + str(value) + "\""
        self.cursor.execute("""UPDATE costs SET %s = %s WHERE cost_id = "%s" """ % (attribute, str(value), costid))
        return True

    def delete_cost(self, costid):
        row = self.cursor.execute("""SELECT purchase_id FROM purchase WHERE cost_id = "%s" """ % costid)
        i = row.fetchone()
        row = self.cursor.execute("""SELECT selling_id FROM sells WHERE cost_id = "%s" """ % costid)
        k = row.fetchone()
        if i is None and k is None:
            self.cursor.execute("""DELETE FROM costs WHERE cost_id = "%s" """ % costid)
            return True
        return False

    def get_purchase_id(self, costid, date, qty):
        row = self.cursor.execute(
            """SELECT purchase_id FROM purchase WHERE cost_id = "%s" AND QTY = %.2f AND purchase_date = "%s" """ % (
                costid, qty, date))
        iid = row.fetchone()
        if iid is None:
            return iid
        return iid[0]

    def get_purchased_product_id(self, costid, date, qty):
        row = self.cursor.execute("""select id from purchased_products where cost_id="%s" and qty = %.2f and
        purchase_date = "%s" """ % (costid, qty, date))
        id = row.fetchone()
        if id is None:
            return id
        return id[0]

    def add_new_purchase(self, pid, costid, date, qty, lot, pentru_factura, supplier):
        s = costid + date + str(qty) + hex(int(t.time() * 10000))
        pur_id = "PUR" + str(hash(s))
        if self.get_purchase_id(costid, date, qty) is not None:
            raise ValueError("purchase already listed")
        self.cursor.execute(
            """ INSERT INTO purchase (purchase_id,cost_id,QTY,purchase_date,lot,for_invoice,supplier_id,
            product_id) VALUES ("%s",
            "%s",%.2f,
            "%s","%s","%s","%s","%s")""" % (
                pur_id, costid, qty, date, lot, pentru_factura, supplier, pid))
        return pur_id

    def edit_purchase(self, pur_id, attribute, value):
        """""""""attribute -> cost_id or 1 , QTY or 2 , purchase_date or 3 """""""""
        dic = {1: """cost_id""", 2: """QTY""", 3: """purchase_date"""}
        if type(attribute) == int:
            attribute = dic[attribute]
        row = self.cursor.execute("""SELECT %s FROM purchase WHERE purchase_id = "%s" """ % (attribute, pur_id))
        row = row.fetchone()
        if row[0] == value:
            return False
        if attribute == """cost_id""" or attribute == """purchase_date""":
            value = """\"""" + str(value) + """\""""
        self.cursor.execute(
            """UPDATE purchase SET %s = %s WHERE purchase_id = "%s" """ % (attribute, str(value), pur_id))
        return True

    def delete_purchase(self, pur_id):
        return self.cursor.execute(""" DELETE FROM purchase WHERE purchase_id = "%s" """ % pur_id)

    def get_phone_id(self, phone):
        row = self.cursor.execute("""SELECT phone_id FROM contacts WHERE phone_no = "%s" """ % phone)
        iid = row.fetchone()
        if iid is None:
            return iid
        return iid[0]

    def add_phone(self, phone, ctmid):
        phnid = """PHN""" + str(hash(str(phone) + ctmid + hex(int(t.time() * 10000))))
        if self.get_phone_id(phone) is not None:
            raise Exception("""Phone Number already listed""")
        self.cursor.execute(
            """INSERT INTO contacts (phone_id,phone_no,customer_id) VALUES ("%s","%s","%s")""" % (phnid, phone, ctmid))
        return phnid

    def edit_phone(self, phnid, attribute, value):
        """""""""attribute -> phone_no or 1 , customer_id or 2  """""""""
        dic = {1: """phone_no""", 2: """customer_id"""}
        if type(attribute) == int:
            attribute = dic[attribute]
        row = self.cursor.execute("""SELECT %s FROM contacts WHERE phone_id = "%s" """ % (attribute, phnid))
        row = row.fetchone()
        if row[0] == value:
            return False
        self.cursor.execute("""UPDATE contacts SET %s = "%s" WHERE phone_id = "%s" """ % (attribute, value, phnid))
        return True

    def delete_phone(self, phnid):
        ctmid = self.get_customer_id_frm_phn_id(phnid)
        row = self.cursor.execute("""SELECT phone_id FROM contacts WHERE customer_id = "%s" """ % ctmid)
        i = map(lambda x: x[0], row.fetchall())
        if len(i) > 1:
            self.cursor.execute("""DELETE FROM contacts WHERE phone_id = "%s" """ % phnid)
            return True
        return False

    def get_customer_id(self, phone):
        row = self.cursor.execute("""SELECT customer_id FROM contacts WHERE phone_no = "%s" """ % phone)
        iid = row.fetchone()
        if iid is None:
            return iid
        return iid[0]

    def add_new_customer(self, name, address, email, ro, cui, cnp):
        ctmid = """CTM""" + str(hash(hex(int(t.time() * 10000))))
        self.cursor.execute(
            """INSERT INTO customers (customer_id,customer_name,customer_address,customer_email, delegate_id,
            customer_cui, customer_cnp
            ) VALUES ("%s","%s",
            "%s","%s","%s","%s","%s")""" % (
                ctmid, name, address, email, ro, cui, cnp))
        return ctmid

    def edit_customer(self, ctmid, attribute, value):
        """""""""attribute -> customer_name or 1 , customer_address or 2,customer_email or 3  """""""""
        dic = {1: """customer_name""", 2: """customer_address""", 3: """customer_email"""}
        if type(attribute) == int:
            attribute = dic[attribute]
        row = self.cursor.execute("""SELECT %s FROM customers WHERE customer_id = "%s" """ % (attribute, ctmid))
        row = row.fetchone()
        if row[0] == value:
            return False
        self.cursor.execute("""UPDATE customers SET %s = "%s" WHERE customer_id = "%s" """ % (attribute, value, ctmid))
        return True

    def delete_customer(self, ctmid):
        row = self.cursor.execute("""SELECT invoice_id FROM invoices WHERE customer_id = "%s" """ % ctmid)
        i = row.fetchone()
        if i is None:
            self.cursor.execute("""DELETE FROM customers WHERE customer_id = "%s" """ % ctmid)
            self.cursor.execute("""DELETE FROM contacts WHERE customer_id = "%s" """ % ctmid)
            return True
        return False

    def get_invoice_id(self, no):
        no = int(no)
        row = self.cursor.execute("""SELECT invoice_id FROM invoices WHERE invoice_no = %d """ % no)
        iid = row.fetchone()
        if iid is None:
            return iid
        return iid[0]

    def add_new_invoice(self, ctmid, no, date, paid):
        inv_id = """INV""" + str(hash(ctmid + date + str(paid) + str(no) + hex(int(t.time() * 10000))))
        if self.get_invoice_id(no) is not None:
            raise Exception("""invoice already listed""")
        self.cursor.execute(
            """INSERT INTO invoices (invoice_id,customer_id,invoice_no,paid,invoice_date) VALUES ("%s","%s",%d,%.2f,
            "%s")""" % (
                inv_id, ctmid, no, paid, date))
        return inv_id

    def edit_invoice(self, inv_id, attribute, value):
        """""""""attribute -> customer_id or 1 ,invoice_no or 2, paid or 3,invoice_date or 4  """""""""
        dic = {1: """customer_id""", 2: "invoice_no", 3: """paid""", 4: """invoice_date"""}
        if type(attribute) == int:
            attribute = dic[attribute]
        row = self.cursor.execute("""SELECT %s FROM invoices WHERE invoice_id = "%s" """ % (attribute, inv_id))
        row = row.fetchone()
        if row[0] == value:
            return False
        if attribute == """customer_id""" or attribute == """invoice_date""":
            value = "\"" + str(value) + "\""
        self.cursor.execute("""UPDATE invoices SET %s = %s WHERE invoice_id = "%s" """ % (attribute, value, inv_id))
        return True

    def delete_invoice(self, inv_id):
        row = self.cursor.execute("""SELECT selling_id FROM sells WHERE invoice_id = "%s" """ % inv_id)
        i = row.fetchone()
        if i is None:
            self.cursor.execute("""DELETE FROM invoices WHERE invoice_id = "%s" """ % inv_id)
            return True
        return False

    def get_sell_id(self, inv_id, costid):
        row = self.cursor.execute("""SELECT selling_id FROM sells WHERE
                    invoice_id = "%s" AND cost_id = "%s" """ % (inv_id, costid))
        iid = row.fetchone()
        if iid is None:
            return iid
        return iid[0]

    def add_new_sell(self, inv_id, sold, qty, costid):
        sell_id = """SEL""" + str(hash(inv_id + str(sold) + str(qty) + costid + hex(int(t.time() * 10000))))
        if self.get_sell_id(inv_id, costid) is not None:
            raise ValueError("""sell already listed""")
        self.cursor.execute(
            """INSERT INTO sells (selling_id,invoice_id,sold_price,QTY,cost_id) VALUES ("%s","%s",%.2f,%.2f,"%s")""" % (
                sell_id, inv_id, sold, qty, costid))
        return sell_id

    def get_lots_for_product(self, product_name):
        """

        @param product_name:
        @return:
        """
        product = self.get_product_id(product_name)
        lots = self.cursor.execute("""select * from `batches` where product_id= "%s" """ % product).fetchall()
        return lots

    def edit_sells(self, sell_id, attribute, value):
        """""""""attribute -> invoice_id or 1 , sold_price or 2,QTY or 3 ,cost_id or 4 """""""""
        dic = {1: """invoice_id""", 2: """sold_price""", 3: """QTY""", 4: """cost_id"""}
        if type(attribute) == int:
            attribute = dic[attribute]
        row = self.cursor.execute("""SELECT %s FROM sells WHERE selling_id = "%s" """ % (attribute, sell_id))
        row = row.fetchone()
        if row[0] == value:
            return False
        if attribute == "cost_id" or attribute == "invoice_id":
            value = "\"" + str(value) + "\""
        self.cursor.execute("""UPDATE sells SET %s = %s WHERE selling_id = "%s" """ % (attribute, value, sell_id))
        return True

    def delete_sells(self, sell_id):
        return self.cursor.execute(""" DELETE FROM sells WHERE selling_id = "%s" """ % sell_id)

    def get_quantity(self, pid):
        row = self.cursor.execute("""SELECT cost_id FROM costs WHERE product_id = "%s" """ % pid)
        l = row.fetchall()
        # print(l)
        qty = 0.0
        for i in l:
            i = i[0]
            qty += self.get_cost_quantity(i)
        return qty

    def get_cost_quantity(self, cost_id):
        qtytup = list(self.cursor.execute("""SELECT q,qty FROM (SELECT SUM(QTY) AS qty FROM sells WHERE cost_id = 
        "%s") JOIN (SELECT SUM(purchased_qty) AS q FROM purchased_products WHERE cost_id = "%s") """ % (
            cost_id, cost_id)).fetchone())
        qty = 0.0
        if qtytup[0] is None:
            qtytup[0] = 0.0
        if qtytup[1] is None:
            qtytup[1] = 0.0
        # print('qtytup: ')
        qty += (qtytup[0] - qtytup[1])
        return float(qty)

    def get_um(self, um_id):
        um = list(self.cursor.execute(""" select name from units_of_measure where id = "%s" """ % um_id))
        return um

    def reset_database(self):
        self.cursor.execute(""" BEGIN ;
                            DROP TABLE category;
                            DROP TABLE products;
                            DROP TABLE costs;
                            DROP TABLE purchase;
                            DROP TABLE customers;
                            DROP TABLE invoices ;
                            DROP TABLE sells ;
                            DROP TABLE contacts ;
                            COMMIT; """)
        new_database_create(self.connection)
        return True

    def get_customer_id_frm_phn_id(self, phnid):
        row = self.cursor.execute("""SELECT customer_id FROM contacts WHERE phone_id = "%s" """ % phnid)
        iid = row.fetchone()
        if iid is None:
            return iid
        return iid[0]

    def save_company_details(self, details):
        qry = """UPDATE details SET company_name = '%s',company_address='%s',
              company_phone='%s',company_email='%s',company_website='%s',company_header='%s',
              company_footer='%s',currency='%s',pic_address='%s',invoice_start_no=%d,sgst_rate=%d,
              cgst_rate=%d, openapi_key='%s';""" % (details['comp_name'],
                                                    details['comp_add'],
                                                    details['comp_phn'],
                                                    details['comp_email'],
                                                    details['comp_site'],
                                                    details['detail_top'],
                                                    details['extra'],
                                                    details['curry'],
                                                    details['pic_add'],
                                                    int(details['inv_start']),
                                                    int(details['sgst']),
                                                    int(details['cgst']),
                                                    details['openapi_key'])
        cursor = self.connection.cursor()
        cursor.execute(qry)
        self.connection.commit()
        return True

    @property
    def get_company_details(self):
        row = self.cursor.execute("SELECT * FROM details").fetchone()
        details = {'comp_name': row[0], 'comp_add': row[2], 'comp_phn': row[3], 'comp_email': row[1],
                   'comp_site': row[4], 'detail_top': row[5], 'extra': row[6], 'curry': row[7], 'pic_add': row[8],
                   'inv_start': row[9], 'sgst': row[10], 'cgst': row[11], 'openapi_key': row[12]}
        return details

    def get_supplier_id(self, search):
        row = self.cursor.execute("""SELECT id FROM suppliers WHERE cui = "%s" or ro = "%s" """ % (search, search))
        pid = row.fetchone()
        if pid is None:
            return pid
        return pid[0]

    def add_supplier(self, name, ro, cui, address, phone):
        supplier_id = "SID" + str(hash(name + hex(int(t.time() * 10000))))
        if self.get_supplier_id(ro) or self.get_supplier_id(cui) is not None:
            raise Exception("Supplier already listed")
        self.cursor.execute("""INSERT INTO suppliers(id, name, ro, cui, address, phone) VALUES("%s", "%s", "%s", "%s",
        "%s", "%s")""" % (supplier_id, name, ro, cui, address, phone))
        return supplier_id

    def add_um(self, newum):
        umid = "UM" + str(hash(newum + hex(int(t.time() * 10000))))
        self.cursor.execute(
            """INSERT INTO units_of_measure (id,name) VALUES ("%s","%s") """ % (umid, newum))
        return umid

    def delete_um(self, umid):
        row = self.cursor.execute("""SELECT product_id FROM products WHERE category_id = "%s" """ % umid)
        i = row.fetchone()
        if i is None:
            self.cursor.execute("""DELETE FROM category WHERE category_id = "%s" """ % umid)
            return True
        return False

    def get_supplier(self, supplier):
        """

        @param supplier:
        @return:
        """
        row = self.cursor.execute("""select * from suppliers where id = "%s" """ % supplier).fetchone()
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
        @param expiry_date
        @return:
        """
        self.cursor.execute(
            """ INSERT INTO purchased_products(purchase_id,cost_id,purchased_qty,purchased_date,lot,product_id, variant
            ) VALUES (
            "%s",
            "%s",%.2f,
            "%s","%s","%s","%s")""" % (
                pur_id, costid, qty, date, lot, pid, variant))
        lot_id = "LOT-" + str(hex(int(t.time()))) + str(lot)
        self.cursor.execute("""insert into `batches`(id, name, batch_qty, purchase_id, product_id, expiry_date, variant) 
        values ("%s", "%s", "%s", "%s", "%s", "%s", "%s")""" % (lot_id, lot, qty, pur_id, pid, expiry_date, variant))
        return pur_id

    def add_variant(self, PID, variant_name, variant_value, variant_modifier):
        """

        @param PID:
        @param variant_name:
        @param variant_value:
        @param variant_modifier:
        """
        variant_id = self.get_variant_id_for_product(PID, variant_name)
        if variant_id is None:
            variant_id = "VAR-" + str(hash(variant_name + hex(int(t.time() * 10000))))
            self.cursor.execute(""" insert into product_variants(variant_id, name, product_id) values("%s", "%s", "%s")
        """ % (variant_id, variant_name, PID))
        if self.get_variant_for_product(PID, variant_name, variant_value, variant_modifier) is not None:
            raise Exception(
                "Produsul are deja varianta " + variant_name + " cu valoarea " + variant_value + " pentru produsul ales")
        option_id = "VAR_OPT-" + str(hash(variant_name + variant_value + hex(int(t.time() * 10000))))
        self.cursor.execute(""" insert into variants_options(option_id, value, variant_id, modifier) values("%s", "%s",
        "%s", "%s")""" % (option_id, variant_value, variant_id, variant_modifier))

        return [variant_id, option_id]

    def get_option_for_variant(self, variant_id, variant_value):
        row = self.cursor.execute("""SELECT option_id FROM variants_options WHERE variant_id = "%s" and value="%s" """
                                  % (variant_id, variant_value))
        pid = row.fetchone()
        if pid is None:
            return pid
        return pid[0]

    def get_variant_name_for_product(self, PID, variant_name):
        row = self.cursor.execute(""" select variant_id from product_variants where product_id="%s" and
        name="%s" """ % (PID, variant_name))
        pid = row.fetchone()
        if pid is None:
            return pid
        return pid[0]

    def get_variant_for_product(self, pid, variant_name, variant_value, variant_modifier):
        row = self.cursor.execute(""" select * from product_variants join variants_options using(variant_id) where
        product_id="%s" and name="%s" and value="%s" and modifier = "%s" """ % (pid, variant_name,
                                                                                variant_value, variant_modifier))
        pid = row.fetchone()
        if pid is None:
            return pid
        return pid[0]

    def get_variant_id_for_product(self, PID, variant_name):
        row = self.cursor.execute(""" select variant_id from product_variants where product_id="%s" and name="%s" """
                                  % (PID, variant_name))
        pid = row.fetchone()
        if pid is None:
            return pid
        return pid[0]

    def edit_variant(self, PID, variant_name, variant_value, variant_modifier):
        variant_id = self.get_variant_id_for_product(PID, variant_name)
        self.cursor.execute(""" update product_variants set variant_name="%s" where variant_id="%s" """ % variant_name)
        option_id = self.cursor.execute(""" select option_id from variants_options where variant_id="%s" """
                                        % variant_id).fetchone()
        self.cursor.execute(""" update variants_options set value="%s", modifier="%s" where variant_id="%s" and
        option_id="%s" """
                            % (variant_value, variant_modifier, variant_id, option_id))

    def deplete_qty(self, product_lot, product_qty, product_name, variant):
        """

        @param product_lot:
        @param product_qty:
        @param product_name
        """
        # """SELECT %s FROM %s WHERE %s = "%s" """ % (column_name, table_name, row_name, rowid)).fetchone()

        qty = self.cursor.execute(""" select batch_qty from `batches` where name = "%s" and variant = "%s" """ % (
            product_lot, variant)).fetchone()
        if int(qty[0]) < 1:
            return 'Quantity not available'

        self.cursor.execute(
            """ update `batches` set batch_qty = batch_qty - "%s" where name= "%s" and variant= "%s" """ % (
                int(product_qty), product_lot, variant))

    def insert_to_purchase(self, costid, date, discount, for_factura, pur_id, supplier_id):
        self.cursor.execute("""insert into purchase(purchase_id,purchase_date,supplier_id,for_invoice, cost_id,
        discount) values("%s",
        "%s",
        "%s", "%s", "%s", "%s")""" % (
            pur_id, date, supplier_id[0], for_factura, costid, discount))
