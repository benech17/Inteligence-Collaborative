from ssl import PROTOCOL_TLS_SERVER
import mesa
import numpy as np
import random as rd
import math
from mesa.datacollection import DataCollector


class GeneticAgent(mesa.Agent):
    def __init__(self, model, vhl, pcross, pmut, taille, popu_init, cout_init):
        super().__init__(model.next_id(), model)
        self.vehicule = vhl
        self.Pcross = pcross
        self.Pmut = pmut
        self.popu_size = taille
        self.popu = popu_init
        self.cout = cout_init
        self.s = 0
        self.mins = [min(self.cout)]
        self.prev_solus = []
        #self.dc = DataCollector({"solution": lambda m: self.f_main() })

    def permutation_list(self, liste):
        result = liste.copy()
        n=len(result)
        i=rd.randint(0,n-1)
        j=rd.randint(0,n-1)
        # while(i==j):
        #     j=rd.randint(0,n-1)
        x=result[i]
        result[i]=result[j]
        result[j]=x
        return(result)
    
    def verifSolu(self, resultat, liste) :
        Absents = []
        Doublons = []
        resultatf = resultat.copy()
        for i in liste :
            instances = 0
            for j in range(len(resultat)):
                if resultat[j].code == i.code and instances == 0 :
                    instances += 1
                elif resultat[j].code == i.code and instances == 1 :
                    Doublons.append([i,j])
            if instances == 0 :
                Absents.append(i)
        for k in range(len(Doublons)) :
            resultatf[Doublons[k][1]] = Absents[k]
        if len(Absents) > len(Doublons) :
            for l in range(len(Doublons), len(Absents)) :
                resultatf.append(Absents[l])
        return(resultatf)
    
    #Le croisement ne marche que si les deux listes sont de même longueur
    def croisement_list(self, liste1, liste2):
        s = len(liste1)
        resultat1 = liste1.copy()
        resultat2 = liste2.copy()
        point = rd.randint(0, s-1)
        for i in range(point, s) :
            resultat1[i], resultat2[i] = resultat2[i], resultat1[i]
        resultat1 = self.verifSolu(resultat1, liste1)
        resultat2 = self.verifSolu(resultat2, liste2)
        return(resultat1, resultat2)

    def triInsertion(self, liste_couts,liste_pop):
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
    
    def proba(self, liste_couts_tr,liste_pop_tr):
        k = len(liste_couts_tr)
        L = []    
        for i in range(0,k):
            a = int((math.exp(liste_couts_tr[k-1]/liste_couts_tr[i])-1)*10)
            for j in range(0,a):
                L.append(liste_pop_tr[i])
        return(L)

    def constructS(self, listeProba, taille):
        k = len(listeProba)
        S = []
        for i in range(0, taille):
            S.append(listeProba[rd.randint(0, k-1)]) 
        return(S)

    def step(self):
        forceTriee, prePopTriee = self.triInsertion(self.cout,self.popu)
        liste_clients_f = prePopTriee[0]
        cout_f = forceTriee[0]
        #construction de S(t), liste de solutions de classe Liste_Clients
        listeProba = self.proba(forceTriee, prePopTriee)
        S1 = self.constructS(listeProba, self.popu_size)

        #construction de S(t+1), liste de solutions de classe Liste_Clients
        S2 = []
        for i in range(0,len(S1),2) :
            if rd.random() < self.Pcross :
                a,b = self.croisement_list(S1[i],S1[i+1])
                S2.append(a)
                S2.append(b)
            else :
                S2.append(S1[i])
                S2.append(S1[i+1])

        #construction de P(t+1)
        self.popu = []
        self.cout = []
        for i in S2 :
            if rd.random() < self.Pmut :
                a = self.permutation_list(i)
                
                self.popu.append(a)
                self.cout.append(self.vehicule.f_cout(a))
            else :
                self.popu.append(i)
                self.cout.append(self.vehicule.f_cout(i))
        
        if self.cout[0] > self.vehicule.f_cout(liste_clients_f):
            self.popu[0] = liste_clients_f
            self.cout[0] = self.vehicule.f_cout(liste_clients_f)
        self.mins.append(cout_f)
        self.prev_solus.append(liste_clients_f)
        return(liste_clients_f)
