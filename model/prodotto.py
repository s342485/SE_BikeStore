from dataclasses import dataclass


@dataclass
class Prodotto:
    id : int
    product_name : str
    brand_id : int
    category_id : int
    model_year : int
    list_price : float

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f"nome prodotto: {self.product_name} brand_id: {self.brand_id} id_cateogria: {self.category_id} anno_modello: {self.model_year}"

    #importante sennò non riesco a creare il grafo
    def __hash__(self):
        return hash(self.id)
