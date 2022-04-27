import random as rd
from ICOheuristics.Genetic import GeneticAgent
from ICOheuristics.Taboo import TabouAgent
from ICOheuristics.RS import RSAgent
import mesa
    
class Agent(mesa.Agent):
    '''Vehicle Agent'''
    def __init__(self, model, series, w):
        super().__init__(model.next_id(), model)
        self.id = model.current_id
        self.code = series['VEHICLE_CODE']
        self.vehicle_total_weight = series['VEHICLE_TOTAL_WEIGHT_KG']
        self.vehicle_total_volume = series['VEHICLE_TOTAL_VOLUME_M3']
        self.vehicle_fixed_cost_km = series['VEHICLE_FIXED_COST_KM']
        self.vehicle_variable_cost_km = series['VEHICLE_VARIABLE_COST_KM']
        self.vehicle_weight = 0
        self.vehicle_volume = 0
        self.omega = w
        # A list of clients. Attention: Deposits should not be added
        self.clients = []
        self.algorithm = []
        self.verifier = 0
    
    def add_client_order(self, client):
        if client == 0:
            return(False)
        elif (self.vehicle_weight + client.total_weight_kg > self.vehicle_total_weight) or (self.vehicle_volume + client.total_volume_m3 > self.vehicle_total_volume) or (client in self.clients):
            return(False)
        self.vehicle_weight += client.total_weight_kg
        self.vehicle_volume += client.total_volume_m3
        return(True)
    
    def f_cout(self, liste):
        d=0
        n=len(liste)
        for i in range(n-1):
            d += liste[i].distance(liste[i+1])
        d+=1 #liste[0].depot_to_customer
        d+=0 #liste[n-1].customer_to_depot
        return self.omega + d*self.vehicle_variable_cost_km
    
    def generateur(self, popu_size):
        newpop = []
        newcout = []
        for i in range(popu_size) :
            newpop.append(self.clients.copy())
            rd.shuffle(newpop[i])
            newcout.append(self.f_cout(newpop[i]))
        return newpop,newcout

    def attribute_client_to_vehicle(self, client):
        if self.add_client_order(client) == True:
            self.clients.append(client)
            return(True)
        return(False)

    def attribute_algorithm_to_vehicle(self, model, pcross, pmut, taille_pop, iter_cycle, refroidissement, typea):
        if len(self.clients) == 0 and len(self.clients) == 1 :
            print("Unique client, ou pas de clients assignés")
        elif typea == "genetic" :
            popu_init,cout_init = self.generateur(taille_pop)
            a = GeneticAgent(model, self, pcross, pmut, taille_pop, popu_init, cout_init)
            self.algorithm.append(a)
        elif typea == "rs" :
            a = RSAgent(model, self, iter_cycle, refroidissement)
            self.algorithm.append(a)
        elif typea == "taboo" :
            a = TabouAgent(model, self, taille_pop)
            self.algorithm.append(a)

    def intra_route_swap(self):
        if len(self.clients) != 0 and len(self.clients) != 1:
            a = rd.randint(0,len(self.clients)-1)
            b = rd.randint(0,len(self.clients)-1)
            c = self.clients[a]
            d = self.clients[b]
            self.clients[a] = d
            self.clients[b] = c
        else :
            print("Non réalisé")
        
    def inter_route_swap(self,vhl):
        if len(self.clients) != 0 and len(self.clients) != 1:
            a = rd.randint(0,len(self.clients)-1)
            b = rd.randint(0,len(vhl.clients)-1)
            c = self.clients[a]
            d = vhl.clients[b]
            # voir si c'est compatible
            if (vhl.vehicle_weight + c.total_weight_kg - d.total_weight_kg > vhl.vehicle_total_weight) or (self.vehicle_weight + d.total_weight_kg - c.total_weight_kg > self.vehicle_total_weight) or (vhl.vehicle_volume + c.total_volume_m3 - d.total_volume_m3 > vhl.vehicle_total_volume) or (self.vehicle_volume - c.total_volume_m3 + d.total_volume_m3 > self.vehicle_total_volume) or (d in self.clients) or (c in vhl.clients):
                print("Non réalisé")
            else:
                self.clients[a] = d
                vhl.clients[b] = c
        else :
            print("Non réalisé")
        
    def intra_route_shift(self):
        if len(self.clients) != 0 and len(self.clients) != 1:
            a = rd.randint(0,len(self.clients)-1)
            b = rd.randint(0,len(self.clients)-1)
            if a == b:
                while (a==b):
                    b = rd.randint(0,len(self.clients)-1)
            
            self.clients.insert(b,self.clients.pop(a))
        else :
            print("Non réalisé")
            
    def inter_route_shift(self,vhl):
        if len(self.clients) != 0 and len(self.clients) != 1:
            b = self.clients[-1]
            
            if (vhl.vehicle_weight + b.total_weight_kg > vhl.vehicle_total_weight) or (vhl.vehicle_volume + b.total_volume_m3 > vhl.vehicle_total_volume) or (b in vhl.clients):
                print("Non réalisé")
            else:
                vhl.clients.insert(0,b)
                self.clients.pop(-1)
        else :
            print("Non réalisé")
        
    def two_intra_route_swap(self):
        if len(self.clients) != 0 and len(self.clients) != 1 and len(self.clients) != 2:
            a = rd.randint(0,len(self.clients)-2)
            b = rd.randint(0,len(self.clients)-2)
            
            c1,c2 = self.clients[a],self.clients[a+1]
            d1,d2 = self.clients[b],self.clients[b+1]
            
            self.clients[a],self.clients[a+1] = d1,d2
            self.clients[b],self.clients[b+1] = c1,c2
        else :
            print("Non réalisé")
        
    def two_intra_route_shift(self):
        if len(self.clients) != 0 and len(self.clients) != 1 and len(self.clients) != 2:
            a = rd.randint(0,len(self.clients)-2)
            b = rd.randint(0,len(self.clients)-2)
            if a == b:
                while (a==b):
                    b = rd.randint(0,len(self.clients)-2)
            
            if a + 1 == b :
                self.clients.insert(a,self.clients.pop(b+1))
            if b + 1 == a :
                self.clients.insert(b,self.clients.pop(a+1))
            else :
                self.clients.insert(b,self.clients.pop(a))
                self.clients.insert(b+1,self.clients.pop(a+1))
        
        else :
            print("Non réalisé")

    def step(self):
        for i in self.algorithm :
            i.step()


