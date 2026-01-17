from database.dao import DAO
from model.product import Product

from UI.controller import Controller

dao = DAO()

ris = dao.get_product_name_by_category(2)
for r in ris:
    print(r)