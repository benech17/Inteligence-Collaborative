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
        self.popu_size = taille
        self.cout = []
        self.popu = self.generateur(model)
        self.s = 0
        #self.dc = DataCollector({"solution": lambda m: self.f_main() })
    
    def generateur(self):
        newpop = []
        for i in range(self.popu_size) :
            newpop.append(rd.shuffle(self.vehicule.liste))
            self.cout.append(self.vehicule.f_cout(newpop[i]))
        return newpop

    def permutation_list(self, liste):
        result = liste.copy()
        n=len(result)
        i=rd.randint(0,n-1)
        j=rd.randint(0,n-1)
        while(i==j):
            j=rd.randint(1,n-2)
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
                if resultat[j].customer_code == i.customer_code and instances == 0 :
                    instances += 1
                elif resultat[j].customer_code == i.customer_code and instances == 1 :
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
        resultat2 = liste2.liste.copy()
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
            a = int((liste_couts_tr[k-1]/liste_couts_tr[i])*10)
            for j in range(0,a):
                L.append(liste_pop_tr[i])
        return(L)

    def constructS(self, listeProba, taille):
        k = len(listeProba)
        S = []
        for i in range(0, taille):
            S.append(listeProba[np.random.randint(0, k-1)]) 
        return(S)

    def step(self):
        forceTriee, prePopTriee = self.triInsertion(self.cout,self.popu)
        print(forceTriee, prePopTriee)
        liste_clients_f = prePopTriee[0]

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
        for i in S2 :
            if rd.random() < self.Pmut :
                self.popu.append(self.permutation_list(i))
            else :
                self.popu.append(i)
        print("je suis dans le step")
        return(liste_clients_f)
