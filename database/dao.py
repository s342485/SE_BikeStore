from database.DB_connect import DBConnect
from model.product import Product


class DAO:
    @staticmethod
    def get_date_range():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT order_date
                    FROM `order` 
                    ORDER BY order_date """
        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def get_category():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM category"""
        cursor.execute(query)

        for row in cursor:
            #appendo delle tuple di categorie
            results.append((row["id"], row["category_name"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_product_by_category(category):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM product WHERE category_id = %s"""
        cursor.execute(query, (category,))

        for row in cursor:
            p = Product(row["id"], row["product_name"], row["brand_id"], row["category_id"], row["model_year"], row["list_price"])
            results.append(p)
            #results è una lista di oggetti Prodotto

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def esiste_connessione(u, v, data_inizio, data_fine):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)

        #STAMPA UNA TABELLA: CON ID E CONTO ORDINATE PER VENDITE MAGGIORI in un determinato arco temporale
        query = """select p.id , count(p.id) as conto
                   from order_item oi , `order` o , product p 
                   where p.id = oi.product_id 
                   and oi.order_id = o.id 
                   and o.order_date >= %s
                   and o.order_date <= %s
                   and p.id in (%s,%s)
                   group by p.id
                   order by conto DESC"""

        cursor.execute(query, (data_inizio, data_fine, u.id, v.id))

        for row in cursor:
            #tuple id conto
            results.append((row["id"], row["conto"]))


        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_product_name_by_category(category):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT p.id, p.product_name FROM product p WHERE category_id = %s"""
        cursor.execute(query, (category,))

        for row in cursor:
            #tuple id-nome
            results.append((row["id"],row["product_name"]))

        cursor.close()
        conn.close()
        return results





