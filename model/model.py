import copy

from database.dao import DAO
from model.product import Product


class Model:
    def __init__(self):
        self._best_soluzione = None
        self._best_score = None

    def get_date_range(self):
        return DAO.get_date_range()

    def get_category(self):
        return DAO.get_category()

    def prodotti_categoria(self, categoria):
        return DAO.get_product_by_category(categoria)

    def nomi_prodotti_categoria(self, categoria):
        return DAO.get_product_name_by_category(categoria)

    def esiste_connessione(self, u: Product, v: Product, data_inizio, data_fine):
        return DAO.esiste_connessione(u, v, data_inizio, data_fine)


    def get_best_path(self, start, end, lungh, grafo):
        self._best_score = -1
        self._best_soluzione = []

        parziale = [start] #lista vuota che viene riempita dei tentativi
        score = 0

        self.ricorsione(end, lungh, parziale, score, grafo)
        return self._best_soluzione, self._best_score

    #contorolli parziale[-1] == end | un nodo non può essere contenuto piu volte nella soluzione
    def ricorsione(self, end, lungh, parziale, count_score, grafo):
        # Cond. terminale
        if len(parziale) == lungh: #condizione di vincita, lunghezza uguale a quella prestabilita e score massimo
            if parziale[-1] == end and count_score > self._best_score:
                self._best_score = count_score
                self._best_soluzione = parziale.copy()
            return
        else:
            nodo_corrente = parziale[-1]
            for vicino in grafo.successors(nodo_corrente):
                if vicino in parziale:
                    continue

                peso = grafo[nodo_corrente][vicino]["weight"]
                parziale.append(vicino)
                self.ricorsione(end, lungh, parziale, count_score + peso, grafo)

                #backtracking!!
                parziale.pop()






