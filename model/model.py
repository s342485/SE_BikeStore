import copy

import networkx as nx

from database.dao import DAO

class Model:
    def __init__(self):
        self._nodes = None
        self._edges = None
        self.G = nx.DiGraph()
        self.id_map = {}

        #per la ricorsione
        self.best_path = []
        self.best_score = None


    def get_date_range(self):
        return DAO.get_date_range()

    def get_categorie(self):
        return DAO.get_all_categorie()

    def get_all_nomi_prodotti(self):
        return DAO.get_all_nomi_prodotti()

    def get_all_prodotti(self):
        return DAO.get_all_prodotti()

    def get_id_categoria(self, titolo_categoria):
        categorie = self.get_categorie()
        for categoria in categorie:
            if categoria[1] == titolo_categoria:
                return categoria[0]

    def costruisci_grafo(self, titolo_categoria, data_inizio, data_fine):
        self.G.clear()
        categoria = self.get_id_categoria(titolo_categoria)
        self._nodes = DAO.get_all_prodotti_categoria(categoria)
        for hub in self._nodes:
            self.G.add_node(hub)

        self.id_map = {p.id: p for p in self._nodes}

        for u in self.G:
            for v in self.G:
                if u.id < v.id:
                    risultato = DAO.exist_connessione_tra(u,v, data_inizio, data_fine)

                    if risultato is None or len(risultato) <= 1:
                        continue

                    (id1, vend1), (id2, vend2) = risultato
                    n1 = self.id_map[id1]
                    n2 = self.id_map[id2]


                    peso = vend1 + vend2

                    if vend1 > vend2:
                        self.G.add_edge(n1, n2, weight=peso)
                    elif vend2 > vend1:
                        self.G.add_edge(n2, n1, weight=peso)
                    else:
                        self.G.add_edge(n1, n2, weight=peso)
                        self.G.add_edge(n2, n1, weight=peso)


        return self.G.number_of_nodes(), self.G.number_of_edges()


    def i_piu_venduti(self):
        scores = []
        for n in self.G.nodes:
            out_w = sum(d["weight"] for _, _, d in self.G.out_edges(n, data=True))
            in_w = sum(d["weight"] for _, _, d in self.G.in_edges(n, data=True))
            scores.append((n, out_w - in_w)) #n = oggetto prodotto

        top5 = sorted(scores, key=lambda x: x[1], reverse=True)[:5]

        return top5

    def get_best_path(self, lungh, start_id, end_id):
        start = self.id_map.get(start_id)
        end = self.id_map.get(end_id)

        print(f"--- Inizio Ricerca Cammino ---")
        print(f"Start: {start.product_name if start else 'None'} (id: {start_id})")
        print(f"End: {end.product_name if end else 'None'} (id: {end_id})")
        print(f"Target Length: {lungh}")

        if start is None or end is None:
            print("ERRORE: Nodo start o end non trovato nella id_map!")
            return [], 0

        self.best_path = []
        self.best_score = -1
        parziale = [start]

        # Contatore per vedere quante combinazioni sta provando
        self._tentativi = 0

        self._ricorsione(parziale, lungh, start, end)

        print(f"--- Ricerca terminata ---")
        print(f"Tentativi totali esplorati: {self._tentativi}")
        print(f"Miglior score trovato: {self.best_score}")

        return self.best_path, self.best_score

    def _ricorsione(self, parziale, lungh, start, end):
        self._tentativi += 1

        # Print ogni 1000 tentativi per non rallentare troppo ma dare segni di vita
        if self._tentativi % 1000 == 0:
            nomi_parziali = [p.product_name[:10] for p in parziale]
            print(f"Esplorando... (Tentativo {self._tentativi}) - Path attuale: {nomi_parziali}")

        # Caso terminale: abbiamo raggiunto la lunghezza desiderata
        if len(parziale) == lungh:
            if parziale[-1] == end:
                corrente_score = self._get_score(parziale)
                print(f"  >>> TROVATO cammino valido! Score: {corrente_score}")
                if corrente_score > self.best_score:
                    print(f"  *** NUOVO RECORD! ***")
                    self.best_score = corrente_score
                    self.best_path = copy.deepcopy(parziale)
            return

        # Esplorazione dei vicini
        successori = list(self.G.successors(parziale[-1]))

        # Se un nodo non ha successori, la ricorsione si ferma qui per questo ramo
        if not successori and len(parziale) < lungh:
            # print(f"Ramo morto: {parziale[-1].product_name} non ha successori")
            pass

        for n in successori:
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, lungh, start, end)
                parziale.pop()

    def _get_score(self, parziale):
        score = 0
        for i in range(len(parziale) - 1):
            # Accedo al peso dell'arco tra il nodo i e il nodo i+1
            score += self.G[parziale[i]][parziale[i + 1]]["weight"]
        return score
