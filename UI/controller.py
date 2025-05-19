import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        pass

    def handleDettagli(self, e):
        pass

    def handlePercorso(self, e):
        pass

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


