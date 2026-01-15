from UI.view import View
from model.model import Model
import flet as ft
import datetime

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

        self.numero_nodi = -1
        self.numero_archi = -1

        self._lista_categorie = []
        self._lista_nomi_prodotti = []

    def set_dates(self):
        first, last = self._model.get_date_range()

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """
        self._view.txt_risultato.controls.clear()

        categoria = self._view.dd_category.value
        print(categoria)
        data_inizio = self._view.dp1.current_date
        data_fine = self._view.dp2.current_date
        self._view.txt_risultato.controls.append(ft.Text(f"Date selezionate: "))
        self._view.txt_risultato.controls.append(ft.Text(f"Start date: {data_inizio.strftime('%d/%m/%Y')}"))
        self._view.txt_risultato.controls.append(ft.Text(f"End date: {data_fine.strftime('%d/%m/%Y')}"))

        numero_nodi, numero_archi = self._model.costruisci_grafo(categoria, data_inizio, data_fine)
        if numero_archi != -1 and numero_nodi != -1:
            self._view.txt_risultato.controls.append(ft.Text("Grafo correttamente creato:"))
            self._view.txt_risultato.controls.append(ft.Text(f"Numero di nodi: {numero_nodi}"))
            self._view.txt_risultato.controls.append(ft.Text(f"Numero di archi: {numero_archi}"))
        else:
            self._view.alert("Il grafo non è stato creato correttamente")


        self._view.update()

    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        piu_venduti = self._model.i_piu_venduti()
        if len(piu_venduti)> 0 :

            self._view.txt_risultato.controls.append(ft.Text("\nI cinque prodotti più venduti sono: "))
            for venduto in piu_venduti:
                self._view.txt_risultato.controls.append(ft.Text(f"{venduto[0].product_name} with score {venduto[1]}"))
        else:
            self._view.alert("Errore di caricamento del grafo")

        self._view.update()



    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        self._view.txt_risultato.controls.clear() #pulisco la listview prima di metterci dei dati
        self._view.update()

        val = self._view.txt_lunghezza_cammino.value
        if val is None or val.strip() == "" or not val.isdigit():
            self._view.alert("Inserisci un numero valido per la lunghezza del cammino")
            return
        lunghezza_cammino = int(val)
        prodotto_iniziale = self._view.dd_prodotto_iniziale.value
        prodotto_finale = self._view.dd_prodotto_finale.value

        if prodotto_iniziale is None or prodotto_finale is None:
            self._view.alert("Seleziona prodotto iniziale e prodotto finale")
            return

        start, end = self.restituisci_id(prodotto_iniziale, prodotto_finale)

        print("Lunghezza cammino: ", lunghezza_cammino)
        print("Prodotto iniziale: ", prodotto_iniziale)
        print("Prodotto finale: ", prodotto_finale)

        miglior_percorso , miglior_score = self._model.get_best_path(lunghezza_cammino, start,end)

        self._view.txt_risultato.controls.append(ft.Text("Cammino migliore"))

        if not miglior_percorso:
            self._view.txt_risultato.controls.append(ft.Text("Nessun cammino trovato con i vincoli richiesti"))
            self._view.update()
            return

        for p in miglior_percorso:
            self._view.txt_risultato.controls.append(ft.Text(p.product_name))

        self._view.txt_risultato.controls.append(ft.Text(f"Score: {miglior_score}"))
        self._view.update()

    def dropdown_categorie(self):
        lista_categorie = self._model.get_categorie()
        for categoria in lista_categorie:
            self._lista_categorie.append(ft.dropdown.Option(categoria[1]))

        return self._lista_categorie

    def dropdown_prodotto(self):
        lista = []
        lista_nomi_prodotto = self._model.get_all_nomi_prodotti()
        for prodotto in lista_nomi_prodotto:
            lista.append(ft.dropdown.Option(prodotto))

        return lista

    def restituisci_id(self, prodotto_iniziale, prodotto_finale):
        lista_prodotti = self._model.get_all_prodotti()

        id_iniziale = 0
        id_finale = 0
        for prodotto in lista_prodotti:
            if prodotto.product_name == prodotto_iniziale:
                id_iniziale = prodotto.id
            if prodotto.product_name == prodotto_finale:
                id_finale = prodotto.id

        return id_iniziale, id_finale


