import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._allTeams=[]
        self._idMapTeams = {}

    def buildGraph(self, year):
        self._graph.clear()
        if len(self._allTeams)==0:
            print("Lista squadre vuota")
            return
        self._graph.add_nodes_from(self._allTeams)
        #modo1:
        # for n1 in self._graph.nodes:
        #     for n2 in self._graph.nodes:
        #         if n1 != n2:
        #             self._graph.add_edge(n1, n2)

        #modo2 --> funzione combinations che DATA una lista, forma tutte le possibili tuple
        myedges=list(itertools.combinations(self._allTeams, 2))
        self._graph.add_edges_from(myedges)

        salaryOfTeams=DAO.getSalaryOfTeams(year, self._idMapTeams) #è un dizionario!!
        for e in self._graph.edges:
            self._graph[e[0]][e[1]]["weight"]=salaryOfTeams[e[0]]+salaryOfTeams[e[1]] #sommo i due salari di ciascun nodo



    def printGraphDetails(self):
        print(f" Grafo creato con {len(self._graph.nodes())} nodi e {len(self._graph.edges())} archi")



    def getYears(self):
        return DAO.getAllYears()

    def getTeamsOfYear(self, year):
        self._allTeams=DAO.getTeamsOfYear(year)
        self._idMapTeams={}
        for t in self._allTeams:
            self._idMapTeams[t.ID]=t
        return  self._allTeams
