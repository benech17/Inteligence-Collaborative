from sklearn.cluster import AgglomerativeClustering
from mesa.time import RandomActivation
import pandas
import mesa
import random

import matplotlib.pyplot as plt

from ICOagents import Client, Deposit, Vehicle

class Model(mesa.Model):
    '''Model is the name for the global model controller'''
    def __init__(self, verbose = False):
        super().__init__()
        self.verbose = verbose
        self.agents = {"deposits": {},"vehicles": {}, "clients": {}, "routes": {}}

    def read_deposits(self, path):
        '''Reads deposits from file and returns pandas dataframe'''
        df = pandas.read_csv(path).reset_index()
        for index, row in df.iterrows():
            id = row['DEPOT_CODE']
            if not id in self.agents['deposits']:
                self.agents['deposits'][id] = Deposit.Agent(self,row)
        if self.verbose:
            print(df.shape,len(self.agents['deposits']),"Deposits")
        return df

    def read_vehicles(self, path, w = 0):
        '''Reads vehicles from file and returns pandas dataframe'''
        df = pandas.read_csv(path).reset_index()
        for index, row in df.iterrows():
            id = row['VEHICLE_CODE']
            if not id in self.agents['vehicles']:
                self.agents['vehicles'][id] = Vehicle.Agent(self,row,w);
        if self.verbose:
            print(df.shape,len(self.agents['vehicles']),"Vehicles")
        return df

    def read_clients(self, path):
        '''Reads clients from file and returns pandas dataframe''' 
        df = pandas.read_csv(path).reset_index()
        for index, row in df.iterrows():
            id = row['CUSTOMER_CODE']
            route_id = row['ROUTE_ID']
            if not id in self.agents['clients']:
                self.agents['clients'][id] = Client.Agent(self,row)
            if not route_id in self.agents['routes']:
                self.agents['routes'][route_id] = []
            self.agents['routes'][route_id].append(self.agents['clients'][id])
        # Transforms routes in list
        self.agents['routes'] = list(self.agents['routes'].values())
        if self.verbose:
            print(df.shape,len(self.agents['clients']),"Clients.",len(self.agents['routes']),"Routes")
        return df

    def make_clusters(self):
        model = AgglomerativeClustering(n_clusters=10, compute_distances=True)
        X = clients[['CUSTOMER_LATITUDE','CUSTOMER_LONGITUDE']]
        model = model.fit(X)

    def assign_clusters_to_vehicles(self,n_clusters):
        liste_vehicules =  list(self.agents['vehicles'].values())
        clients = [[client.lat, client.lon] for client in self.agents['clients'].values()]
        clustering = AgglomerativeClustering(n_clusters, compute_distances=True)
        results = clustering.fit_predict(clients)
        
        grouped_clients = [[]]*n_clusters
        cluster_costs_weight = [0]*n_clusters
        cluster_costs_volume = [0]*n_clusters
        
        for i in range(len(results)):
            c = list(self.agents['clients'].values())[i]
            grouped_clients[results[i]].append(c)
            cluster_costs_weight[results[i]] += c.total_weight_kg
            cluster_costs_volume[results[i]] += c.total_volume_m3
        
        
        
        print(results,grouped_clients,cluster_costs_weight,cluster_costs_volume)    
        
        for i,client in enumerate(self.agents['clients']):
            self.agents['clients'][client].route_id = results[i]

    def assign_clients_to_vehicles(self,l):
        liste_vehicules =  list(self.agents['vehicles'].values())
        for v in liste_vehicules:
            v.clients = []
            j = 0
            while j < len(l) and v.add_client_order(l[j]) != False:
                v.attribute_client_to_vehicle(l[j])
                l.pop(j)
                j += 1
    
    def assign_heuristics_to_vehicles(self):
        self.schedule = mesa.time.RandomActivation(self)
        for v in self.agents['vehicles'].values():
            v.algorithm = []
            v.attribute_algorithm_to_vehicle(self,0.5,0.2,100,0.0,0.0,"genetic")
            v.attribute_algorithm_to_vehicle(self,0.0,0.0,50,0.0,0.0,"taboo")
            v.attribute_algorithm_to_vehicle(self,0.0,0.0,0,10,0.9,"rs")
            self.schedule.add(v)

    def remove_road(self,typea,liste_vehicules):
        nb_clients = []
        i_selec = 0
        
        for v in liste_vehicules:
            nb_clients.append(len(v.clients))
        
        if typea == "smallest":
            min_clients = nb_clients[0]
            for i in range(len(liste_vehicules)):
                if min_clients > nb_clients[i] and nb_clients[i] != 0:
                    min_clients = nb_clients[i]
                    i_selec = i
        elif typea == "random":
            i_selec = random.randint(0,len(liste_vehicules)-1)
            if nb_clients[i_selec] == 0:
                while nb_clients[i_selec] == 0:
                    i_selec = random.randint(0,len(liste_vehicules)-1)
        
        redistrib = liste_vehicules[i_selec].clients.copy()
        liste_vehicules[i_selec].clients = []
        liste_vehicules[i_selec].vehicle_weight = 0
        liste_vehicules[i_selec].vehicle_volume = 0
        nb_clients[i_selec] = 0
        
        for i in range(len(liste_vehicules)):
            if nb_clients[i] != 0:
                for j in range(len(redistrib)):
                    val = v.attribute_client_to_vehicle(redistrib[j])
                    if val == True:
                        redistrib[j] = 0
                        
        for k in redistrib:
            liste_vehicules[i_selec].attribute_client_to_vehicle(k)

    def step(self):
        self.schedule.step()
    