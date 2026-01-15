import flet as ft
from UI.alert import AlertManager

class View:
    def __init__(self, page: ft.Page):
        # Page
        self.page = page
        self.page.title = "SE_BikeStore"
        self.page.horizontal_alignment = "center"
        self.page.theme_mode = ft.ThemeMode.DARK

        # Alert
        self.alert = AlertManager(page)

        # Controller
        self.controller = None



    def show_alert(self, messaggio):
        self.alert.show_alert(messaggio)

    def set_controller(self, controller):
        self.controller = controller

    def update(self):
        self.page.update()

    def load_interface(self):
        """ Crea e aggiunge gli elementi di UI alla pagina e la aggiorna. """
        # Intestazione
        self.txt_titolo = ft.Text(value="Gestione Vendita Biciclette", size=30, weight=ft.FontWeight.BOLD)

        # Riga 1
        self.dd_category = ft.Dropdown(label="Categoria", width=200, options=self.controller.dropdown_categorie()) # TODO: Gestire il dropdown

        self.dp1 = ft.DatePicker(
            on_change=lambda e: print(f"Giorno selezionato: {self.dp1.value}"),
            on_dismiss=lambda e: print("Data non selezionata")
        )

        self.page.overlay.append(self.dp1)
        self.pulsante_start_date = ft.ElevatedButton("Data Inizio",
                                          icon=ft.Icons.CALENDAR_MONTH,
                                          on_click=lambda _: self.page.open(self.dp1))

        self.dp2 = ft.DatePicker(
            on_change=lambda e: print(f"Giorno selezionato: {self.dp2.value}"),
            on_dismiss=lambda e: print("Data non selezionata")
        )
        self.page.overlay.append(self.dp2)
        self.pulsante_end_date = ft.ElevatedButton("Data Fine",
                                          icon=ft.Icons.CALENDAR_MONTH,
                                          on_click=lambda _: self.page.open(self.dp2))

        self.controller.set_dates()

        self.pulsante_crea_grafo = ft.ElevatedButton(text="Crea Grafo", on_click=self.controller.handle_crea_grafo)

        self.pulsante_best_prodotti = ft.ElevatedButton(text="Prodotti più venduti",
                                                  on_click=self.controller.handle_best_prodotti)

        row1 = ft.Row([self.dd_category, self.pulsante_start_date, self.pulsante_end_date, self.pulsante_crea_grafo, self.pulsante_best_prodotti],
                      alignment=ft.MainAxisAlignment.CENTER)

        # Riga 2
        self.txt_lunghezza_cammino = ft.TextField(label="Lunghezza Cammino", width=120)
        self.dd_prodotto_iniziale = ft.Dropdown(label="Prodotto Iniziale", width=350, options=self.controller.dropdown_prodotto())
        self.dd_prodotto_finale = ft.Dropdown(label="Prodotto Finale", width=350, options=self.controller.dropdown_prodotto())

        self.pulsante_cerca_cammino = ft.ElevatedButton(text="Cerca", on_click=self.controller.handle_cerca_cammino, width=120)

        row2 = ft.Row([self.txt_lunghezza_cammino, self.dd_prodotto_iniziale, self.dd_prodotto_finale, self.pulsante_cerca_cammino],
                      alignment=ft.MainAxisAlignment.CENTER)

        self.txt_risultato = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

        # --- Toggle Tema ---
        self.toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=self.cambia_tema)

        self.lst_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)



        # --- Layout della pagina ---
        self.page.add(
            self.toggle_cambia_tema,
            self.txt_titolo,
            ft.Divider(),

            row1,
            row2,
            ft.Divider(),

            self.txt_risultato
        )

        self.page.scroll = "adaptive"
        self.page.update()

    def cambia_tema(self, e):
        """ Cambia tema scuro/chiaro """
        self.page.theme_mode = ft.ThemeMode.DARK if self.toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        self.toggle_cambia_tema.label = "Tema scuro" if self.toggle_cambia_tema.value else "Tema chiaro"
        self.page.update()
