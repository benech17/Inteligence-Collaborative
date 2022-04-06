from ssl import PROTOCOL_TLS_SERVER
import mesa
import numpy as np
import random as rd
from mesa.datacollection import DataCollector
from ICOagents.Client import Liste_Clients


class GeneticAgent(mesa.Agent):
    def __init__(self, model, vhl, pcross, pmut, taille):
        super().__init__(model.next_id(), model)
        self.vehicule = vhl
        self.Pcross = pcross
        self.Pmut = pmut
        self.pop_size = taille
        self.pop = []
        self.cout = []
        self.s = 0
        #self.dc = DataCollector({"solution": lambda m: self.f_main() })
    
    def generateur(self, model):
        for i in range(self.pop_size) :
            a = Liste_Clients(model)
            self.pop.append(a.add_liste_to_list(self.vehicule.clients.shuffle_list()))
            self.cout.append(self.vehicule.f_cout(self.pop[i].liste))
            
    def triInsertion(liste_couts,liste_pop):
        k = len(liste_couts)
        for i in range(1, k) :
            cle = liste_couts[i]
            cle2 = liste_pop[i]
            j = i-1
            while j >= 0 and liste_couts[j] > cle:
                liste_couts[j+1] = liste_couts[j]# decalage
                liste_pop[j+1] = liste_pop[j]
                j = j-1
            liste_couts[j+1] = cle
            liste_pop[j+1] = cle2
        return(liste_couts, liste_pop)
    
    def proba(liste_couts_tr,liste_pop_tr):
        k = len(liste_couts_tr)
        L = []    
        for i in range(0,k):
            a = int((liste_couts_tr[k-1]/liste_couts_tr[i])*10)
            for j in range(0,a):
                L.append(liste_pop_tr[i])
        return(L)

    def constructS(listeProba, taille):
        k = len(listeProba)
        S = []
        for i in range(0, taille):
            S.append(listeProba[np.random.randint(0, k-1)]) 
        return(S)

    def step(self):
        forceTriee, prePopTriee = self.triInsertion(self.cout,self.pop)
        liste_clients_f = prePopTriee[0]

        #construction de S(t), liste de solutions de classe Liste_Clients
        listeProba = self.proba(forceTriee, prePopTriee)
        S1 = self.constructS(listeProba, self.pop_size)
          
        #construction de S(t+1), liste de solutions de classe Liste_Clients
        S2 = []
        for i in range(0,len(S1),2) :
            if rd.random() < self.Pcross :
                a,b = S1[i].croisement_list(S1[i+1].liste)
                S2.append(a)
                S2.append(b)
            else :
                S2.append(S1[i])
                S2.append(S1[i+1])
          
        #construction de P(t+1)
        self.pop = []
        for i in S2 :
            if rd.random() < self.Pmut :
                self.pop.append(i.permutation_list())
            else :
                self.pop.append(i)
        self.s+=1
        print("je suis dans le step")
        return(liste_clients_f)
