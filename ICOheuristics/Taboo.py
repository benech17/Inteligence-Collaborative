from ssl import PROTOCOL_TLS_SERVER
import mesa
import numpy as np
import random as rd
from mesa.datacollection import DataCollector

class TabouAgent(mesa.Agent):
    def __init__(self,model,vhl,taille):
        super().__init__(model.next_id(), model)
        self.vehicule = vhl
        self.popu_size = taille
        self.init_popu_size = taille
        self.count = 0
        self.mins = [self.vehicule.f_cout(self.vehicule.clients)]
        self.prev_solus = [self.vehicule.clients.copy()]
        self.taboo = []
         
    def permutation_list(self, liste):
        result = liste.copy()
        n=len(result)
        i=rd.randint(0,n-1)
        j=rd.randint(0,n-1)
        while(i==j):
            j=rd.randint(0,n-1)
        x=result[i]
        result[i]=result[j]
        result[j]=x
        return(result)
        
    def step(self):
        #on exploite les informations des autres algos
        if self.vehicule.mode == "collab":
            liste_clients_f = self.vehicule.clients.copy()
        else:
            liste_clients_f = self.prev_solus[-1].copy()
        
        #on génère un ensemble de solutions voisines
        popu = [liste_clients_f]
        if self.count > 10 : #on peut augmenter la taille de la population quand l'algo stagne
            self.popu_size = 4*self.init_popu_size
        for k in range(1, self.popu_size):
            elt = popu[-1]
            popu.append(self.permutation_list(elt.copy()))
            
        #on détermine le minimum en vérifiant qu'il n'est pas dans la liste taboue
        cle = popu[0]
        for j in range(self.popu_size):
            if self.vehicule.f_cout(cle) > self.vehicule.f_cout(popu[j]) and popu[j] not in self.taboo :
                cle = popu[j] 
        if self.vehicule.f_cout(cle) < self.vehicule.f_cout(liste_clients_f):
            self.taboo.append(liste_clients_f)
            liste_clients_f = cle
            self.count = 0
            self.popu_size = self.init_popu_size
        else:
            self.count += 1
            
        #on enregistre le minimum dans la liste taboue et on récupère sa valeur
        self.taboo.append(cle)
        self.mins.append(self.vehicule.f_cout(liste_clients_f))
        self.prev_solus.append(liste_clients_f)
        return(liste_clients_f)