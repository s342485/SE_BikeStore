from dataclasses import dataclass


@dataclass
class Product:
    id: int
    product_name: str
    brand_id : int
    category_id : int
    model_year : int
    list_price : float

    def __str__(self):
        return f"Prodotto {self.id}: {self.product_name}, brand {self.brand_id}, categoria {self.category_id}, anno modello {self.model_year}, prezzo listino {self.list_price}"

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


