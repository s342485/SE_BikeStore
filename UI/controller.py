import networkx as nx

from UI.view import View
from model.model import Model
import flet as ft
import datetime

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

        self.G = nx.DiGraph() #creo un digraph diretto per in questo problema influiscono pure le direzioni
        self._nodes = None
        self._edges = None
        self._id_map = {}

        # valori selezionati nelle dropdown (oggetti Prodotto veri)
        self.dd_prod_start_value = None
        self.dd_prod_end_value = None


    def set_dates(self):
        first, last = self._model.get_date_range()

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)

    def aggiungi_categorie(self):
        categorie = self._model.get_category()
        return categorie

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """
        categoria = self._view.dd_category.value # mi prende la categoria selezionata dall'utente
        self._nodes = self._model.prodotti_categoria(categoria)

        data_inizio = self._view.dp1.value.date() #date prende proprio il giorno
        data_fine = self._view.dp2.value.date()

        if data_inizio is None or data_fine is None:
            self._view.show_alert("SELEZIONA ENTRAMBE LE DATE!")
            self._view.update()
            return None

        self.G = nx.DiGraph()

        for prodotto in self._nodes:
            self._id_map[prodotto.id] = prodotto
            self.G.add_node(prodotto)

        #print("NODI:", list(self.G.nodes))
        pari = 0
        for u in self.G:
            print(u.id)
            for v in self.G:
                print(v.id)
                if u.id  < v.id:
                    #funzione verifica
                    risultato = self._model.esiste_connessione(u, v, data_inizio, data_fine)

                    if len(risultato) != 2:
                        continue
                        #vuol dire che per tutti e due i nodi c'è una connessione e quindi è presente la loro riga con il loro id e il loro numero di vendite

                    vendite_v = 0
                    vendite_u = 0

                    for r in risultato:
                        if r[0] == u.id:
                            vendite_u = r[1]
                        if r[0] == v.id:
                            vendite_v = r[1]

                    peso = vendite_u + vendite_v

                    if vendite_u == vendite_v:
                        pari  += 1

                    if vendite_u > vendite_v:
                        self.G.add_edge(u, v, weight=peso)
                    elif vendite_u < vendite_v:
                        self.G.add_edge(v, u, weight=peso)
                    elif vendite_u == vendite_v:
                        self.G.add_edge(u, v, weight=peso)
                        self.G.add_edge(v, u, weight=peso)

                    print("COPPIE IN PARI:", pari)
                    print("ARCHI:", self.G.number_of_edges())

        self._view.txt_risultato.controls.clear()
        self._view.txt_risultato.controls.append(ft.Text("Date selezionate:"))
        self._view.txt_risultato.controls.append(ft.Text(f"Start date: {data_inizio}"))
        self._view.txt_risultato.controls.append(ft.Text(f"End date: {data_fine}"))
        if self.G.number_of_nodes() > 0 and self.G.number_of_edges() > 0:
            self._view.txt_risultato.controls.append(ft.Text("Grafo correttamente creato: "))
            self._view.txt_risultato.controls.append(ft.Text(f"Numero di nodi: {self.G.number_of_nodes()}"))
            self._view.txt_risultato.controls.append(ft.Text(f"Numero di archi: {self.G.number_of_edges()}"))
        else:
            self._view.show_alert("La creazione del grafo ha riscontrato dei problemi!")

        self._view.update()

    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        best_prodotti = []
        for n in self.G.nodes:
            score = 0
            #data = True mi da anche i pesi dell'arco e quindi posso andare a recuperare il weight ti restituisce: [(n, v1, {"weight": 2}),
            for e_out in self.G.out_edges(n, data=True):
                score += e_out[2]["weight"]
            for e_in in self.G.in_edges(n, data=True):
                score -= e_in[2]["weight"]

            best_prodotti.append((n.product_name, score))
        #ordina in base al secondo elemento della lista ovvero lo score | reverse = True vuol dire che ordini dal piu grande al piu piccolo
        best_prodotti.sort(reverse=True, key=lambda x: x[1])

        self._view.txt_risultato.controls.append(ft.Text("\nI cinque prodotti più venduti sono:"))
        for prodotto in best_prodotti[0:5]:
            self._view.txt_risultato.controls.append(ft.Text(f"{prodotto[0]} with score {prodotto[1]}"))

        self._view.update()

    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        id_prodotto_iniziale = int(self._view.dd_prodotto_iniziale.value)
        id_prodotto_finale = int(self._view.dd_prodotto_finale.value)


        start = self._id_map[id_prodotto_iniziale]
        print(f"Partenza {start}")
        end = self._id_map[id_prodotto_finale]
        print(f"Fine {end}")
        lungh = int(self._view.txt_lunghezza_cammino.value)
        print(f"Lunghezza {lungh}")


        miglior_percorso , miglior_score = self._model.get_best_path(start, end, lungh, self.G)

        self._view.txt_risultato.controls.clear()
        self._view.txt_risultato.controls.append(ft.Text("Cammino migliore: "))
        for prodotto in miglior_percorso:
            nome_prodotto = prodotto.product_name
            self._view.txt_risultato.controls.append(ft.Text(f"{nome_prodotto}"))

        self._view.txt_risultato.controls.append(ft.Text(f"Score: {miglior_score} "))

        self._view.update()


    def handle_category_change(self, e):
        categoria = self._view.dd_category.value
        lista_nomi_categoria = self._model.nomi_prodotti_categoria(categoria)

        options = [ft.dropdown.Option(key = id, text=nome) for id, nome in lista_nomi_categoria]

        self._view.dd_prodotto_iniziale.options = options
        self._view.dd_prodotto_finale.options = options.copy()

        #riabilito i bottoni
        self._view.dd_prodotto_iniziale.disabled = False
        self._view.dd_prodotto_finale.disabled = False


        self._view.update()




