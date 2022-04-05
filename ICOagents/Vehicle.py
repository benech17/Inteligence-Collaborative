import random
import mesa
    
class Agent(mesa.Agent):
    '''Vehicle Agent'''
    def __init__(self, model, series, w):
        super().__init__(model.next_id(), model)
        self.code = series['VEHICLE_CODE']
        self.vehicle_total_weight = series['VEHICLE_TOTAL_WEIGHT_KG']
        self.vehicle_total_volume = series['VEHICLE_TOTAL_VOLUME_M3']
        self.vehicle_weight = 0
        self.vehicle_volume = 0
        self.vehicle_fixed_cost_km = series['VEHICLE_FIXED_COST_KM']
        self.vehicle_variable_cost_km = series['VEHICLE_VARIABLE_COST_KM']
        self.omega = w
        # A list of clients. Attention: Deposits should not be added
        self.clients = []
    
    def add_client_order(self, client):
        if (self.vehicle_weight + client.total_weight_kg > self.vehicle_total_weight) or (self.vehicle_volume + client.total_volume_m3 > self.vehicle_total_volume):
            return(False)
        self.vehicle_weight += client.total_weight_kg
        self.vehicle_volume += client.total_volume_m3
        return(True)
    
    def f_cout(self, liste_client):
        d=0
        n=len(liste_client)
        for i in range(n-1):
            d += liste_client[i].calc_dist(liste_client[i+1])
        d+=liste_client[0].depot_to_customer
        d+=liste_client[n-1].customer_to_depot
        return self.omega + d*self.vehicle_fixed_cost_km

    def assign_clients(self,liste_vehicules,liste_client):
        # adapt
        j = 0
        for i in range(len(liste_vehicules)):
            while liste_vehicules[i].add_client_order(liste_client.liste[j]) != False:
                liste_vehicules[i].attribute_client_to_vehicle(liste_client.liste[j])
                j += 1

    def attribute_client_to_vehicle(self, client):
        if self.add_client_order(client) == True:
            self.liste_clients.append(client)
    
    def step():
        pass
  
class Liste_Clients:
    '''Special list object that contains clients'''
    def __init__(self, unique_id):
        self.id = unique_id
        self.liste = []
    
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
