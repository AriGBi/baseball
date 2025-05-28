import copy
import itertools
import random
import warnings


import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._allTeams=[]
        self._idMapTeams = {}
        self._bestPath=[]
        self._bestScore=0

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

    def getBestPathV2(self, start):
        self._bestPath = []
        self._bestScore = 0
        parziale=[start]
        vicini= self._graph.neighbors(start)
        #idea : siccome l'es chiede di prendere nodi con archi sempre più decrescenti, il primissimo nodo da cui parto sarà quello maggiore possibile
        #allora creo una lista di tuple in cui salvo (nodo,peso), la ordino per peso decrescente.
        #il primo elemento della lista sarà ls tupla con il nodo con peso massimo rispetto a start. Prendo SOLO quello e lo metto in parziale.
        #non ho più bisogno di ciclare su tutti i vicini di start, perchè ho già trovato quello con peso maggiore
        viciniTuples=[(v, self._graph[start][v]["weight"]) for v in vicini]
        viciniTuples.sort(key=lambda x: x[1], reverse=True)

        parziale.append(viciniTuples[0][0]) #prendo la prima tupla e dalla tupla prendo solo il nodo
        self._ricorsioneV2(parziale)
        return self.getWeightOfPaht(self._bestPath), self._bestScore

    def _ricorsioneV2(self, parziale):
        if self.score(parziale) > self._bestScore:
            self._bestScore=self.score(parziale)
            self._bestPath=copy.deepcopy(parziale)

        vicini = self._graph.neighbors(parziale[-1])
        viciniTuples = [(v, self._graph[parziale[-1]][v]["weight"]) for v in vicini] #ragiono sempre mettendo le coppie (nodo, peso) in una lista, la sorto e prendo sempre il più grande possibile
        viciniTuples.sort(key=lambda x: x[1], reverse=True)

        for t in viciniTuples:
            if t[0] not in parziale and self._graph[parziale[-2]][parziale[-1]]["weight"] > t[1]:
                parziale.append(t[0])
                self._ricorsioneV2(parziale)
                parziale.pop()
                return #non ha più senso esplorare altri nodi. Dopo che ho aggiunto l'arco che so che è migliore non devo esplorare altri archi

    def getWeightOfPaht(self, path):
        pathTuple=[(path[0],0) ]#il primo nodo ha peso 0
        for i in range(1,len(path)):
            pathTuple.append((path[i],self._graph[path[i-1]][path[i]]["weight"]))
        return pathTuple

    def getBestPath(self, start):
        self._bestPath = []
        self._bestScore = 0
        vicini= self._graph.neighbors(start)
        parziale=[start]
        for v in vicini:
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()
        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale):
        print(len(parziale))
        #1) verifico che parziale sia una soluzione e verifico se è migliore della best
        if self.score(parziale) > self._bestScore:
            self._bestScore=self.score(parziale)
            self._bestPath=copy.deepcopy(parziale)

        #2) verifico se posso aggiungere un nuovo nodo
        for v in self._graph.neighbors(parziale[-1]):
            if v not in parziale and self._graph[parziale[-2]][parziale[-1]]["weight"]>self._graph[parziale[-1]][v]["weight"]:
                # 3) aggiungo nodo e faccio ricorsione
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()



    def score(self, listOfNodes):
        if len(listOfNodes)<2:
            warnings.warn("Errore in score, attesa lista lunga 2.")
        totPeso=0
        for i in range(len(listOfNodes)-1):
            totPeso+=self._graph[listOfNodes[i]][listOfNodes[i+1]]["weight"]
        return totPeso

    def getNeighborsSorted(self, source):
        vicini = nx.neighbors(self._graph, source) #lista di tutti i nodi vicini
        #vogliamo recuperare i pesi
        viciniTuple=[] #lista di tuple con (nodoVicino,peso)
        for v in vicini:
            viciniTuple.append((v,self._graph[source][v]["weight"]))

        viciniTuple.sort(key=lambda x:x[1], reverse=True) #si fa il sort rispetto al peso
        return viciniTuple

    def printGraphDetails(self):
        print(f" Grafo creato con {len(self._graph.nodes())} nodi e {len(self._graph.edges())} archi")


    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getYears(self):
        return DAO.getAllYears()

    def getTeamsOfYear(self, year):
        self._allTeams=DAO.getTeamsOfYear(year)
        self._idMapTeams={}
        for t in self._allTeams:
            self._idMapTeams[t.ID]=t
        return  self._allTeams

    def getRandomNode(self):
        index=random.randint(0,self._graph.number_of_nodes()-1)
        return list(self._graph.nodes)[index]
