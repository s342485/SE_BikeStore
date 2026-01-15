from database.DB_connect import DBConnect
from model.prodotto import Prodotto


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
    def get_all_categorie():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM category"""
        cursor.execute(query)

        for row in cursor:
            results.append((row["id"],row["category_name"]))


        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_all_prodotti_categoria(id_categoria):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * 
                    FROM product
                    WHERE category_id = %s """
        cursor.execute(query, (id_categoria,))

        for row in cursor:
            prodotto = Prodotto(row["id"],row["product_name"],row["brand_id"], row["category_id"], row["model_year"], row["list_price"])
            results.append(prodotto)

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def exist_connessione_tra(u: Prodotto, v:Prodotto, data_inizio, data_fine):
        """
        Due prodotti sono collegati se sono stati venduti nello stesso periodo
        Arco uscente nel caso di vendite maggiori
        Arco entrante nel caso di vendite minori
        Uguali inserisco entrambi gli archi
        """
        conn = DBConnect.get_connection()

        results = []


        cursor = conn.cursor(dictionary=True)
        query = """SELECT p.id as id , count(distinct oi.order_id) as vendita
                   FROM order_item oi , `order`  o,  product p 
                   WHERE p.id = oi.product_id 
                   AND o.id = oi.order_id 
                   AND o.order_date >= %s AND o.order_date <= %s
                   AND p.id in (%s, %s)
                   GROUP BY p.id 
                   ORDER BY vendita DESC
                """
        cursor.execute(query, (data_inizio,data_fine, u.id, v.id))

        for row in cursor:
            results.append((row["id"], row["vendita"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_all_nomi_prodotti():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT p.product_name as name FROM product p"""
        cursor.execute(query)

        for row in cursor:
            results.append(row["name"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_all_prodotti():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM product"""
        cursor.execute(query)

        for row in cursor:
            prodotto = Prodotto(row["id"], row["product_name"], row["brand_id"], row["category_id"], row["model_year"],
                                row["list_price"])
            results.append(prodotto)

        cursor.close()
        conn.close()
        return results

