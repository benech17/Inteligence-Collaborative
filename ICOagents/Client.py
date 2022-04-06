from ICOagents import Geo
import random
import mesa

class Agent(Geo.Agent):
    '''Client Agent'''
    def __init__(self, model, series):
        super().__init__(model, series['CUSTOMER_CODE'], series['CUSTOMER_LATITUDE'], series['CUSTOMER_LONGITUDE'])
        self.number_of_articles = series['NUMBER_OF_ARTICLES']
        self.total_weight_kg = series['TOTAL_WEIGHT_KG']
        self.total_volume_m3 = series['TOTAL_VOLUME_M3']
    def step():
        pass

class Liste_Clients(mesa.Agent):
    '''Special list object that contains clients'''
    def __init__(self, model):
        super().__init__(model.next_id(), model)
        self.liste = []
    
    def add_liste_to_list(self, liste):
        self.liste = liste
    
    def shuffle_list(self):
        self.liste = random.shuffle(self.liste)

    def permutation_list(self):
        result = self.liste.copy()
        n=len(result)
        i=random.randint(0,n-1)
        j=random.randint(0,n-1)
        while(i==j):
            j=random.randint(1,n-2)
        x=result[i]
        result[i]=result[j]
        result[j]=x
        return(result)
    
    #Le croisement ne marche que si les deux listes sont de même longueur
    def croisement_list(self, liste_clients):
        s = len(self.liste)
        resultat1 = self.liste.copy()
        resultat2 = liste_clients.liste.copy()
        point = random.randint(0, s-1)
        for i in range(point, s) :
            resultat1[i], resultat2[i] = resultat2[i], resultat1[i]
        resultat1 = self.verifSolu(resultat1, self)
        resultat2 = self.verifSolu(resultat2, self)
        return(resultat1, resultat2)

    def add_client_to_list(self, client):
        self.liste.append(client)
    
    def verifSolu(resultat, self) :
        Absents = []
        Doublons = []
        resultatf = resultat.copy()
        for i in self.liste :
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