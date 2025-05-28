import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        year= self._view._ddAnno.value
        if year is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Attenzione selezionare anno.", color="red"))
            self._view.update_page()
            return
        self._model.buildGraph(int(year)) #sono sicuro che questo int(year) NON DARà ERRORI PERCHè IL DD DELL'ANNO L'HO RIEMPITO IO
        nNodes,nEdges=self._model.getGraphDetails()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato"))
        self._view._txt_result.controls.append(ft.Text(f"Il grafo è costituito da {nNodes} nodi e {nEdges} archi"))
        self._view.update_page()


    def handleDettagli(self, e):
        source= self._selectedTeam #team scelto dal dd
        if self._selectedTeam is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Per favore selezionare un team", color="red"))
            self._view.update_page()
            return
        #viciniSorted --> lista di tuple in cui primo elemento è un nodo e il secondo è un peso
        viciniSorted= self._model.getNeighborsSorted(self._selectedTeam)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Il vicinato conta {len(viciniSorted)} squadre ", color="green"))
        for v in viciniSorted:
            self._view._txt_result.controls.append(ft.Text(f"{v[0]} -- peso: {v[1]}"))
        self._view.update_page()


    def handlePercorso(self, e):
        if self._selectedTeam is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Per favore selezionare un team", color="red"))
            self._view.update_page()
            return
        path, score= self._model.getBestPathV2(self._selectedTeam)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Trovato un cammino che parte da {self._selectedTeam} con somma dei pesi: {score}"))
        for v in path: #v è una tupla
            self._view._txt_result.controls.append(ft.Text(f"{v[0]} -- peso: {v[1]}"))
        self._view.update_page()

    def handleDDYearSelection(self,e):
        teams=self._model.getTeamsOfYear(self._view._ddAnno.value)
        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(ft.Text(f"Ho trovato {len(teams)} squadre che hanno giocato nel {self._view._ddAnno.value}"))
        for t in teams:
            self._view._txtOutSquadre.controls.append(ft.Text(f"{t.teamCode}"))
            self._view._ddSquadra.options.append(ft.dropdown.Option(data=t, text=t.teamCode, on_click=self._readDDTeams))

        self._view.update_page()


    def _readDDTeams(self, e):
        if e.control.data is None:
            self._selectedTeam=None
        else:
            self._selectedTeam=e.control.data
        print(f"readDDTeams called -- {self._selectedTeam}")

    def fillDDYear(self):
        years=self._model.getYears()
        yearsDD=map(lambda x: ft.dropdown.Option(x),years) #cicla su un iterabile (years) e fa la cosa che voglio che faccia, ovvero rendere ciascun elemento x un oggetto Option
        self._view._ddAnno.options=yearsDD
        self._view.update_page()


