from sklearn.cluster import AgglomerativeClustering
from mesa.time import RandomActivation
import pandas
import mesa
import random

import matplotlib.pyplot as plt

from ICOagents import Client, Deposit, Vehicle
from ICOmodel import Cluster

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
        self.agents['routes'] = list(self.agents['routes'].values())
        if self.verbose:
            print(df.shape,len(self.agents['clients']),"Clients.",len(self.agents['routes']),"Routes")
        return df

    def assign_clusters_to_vehicles(self):
        clients = [[client.lat, client.lon] for client in self.agents['clients'].values()]
        n_clusters = len(self.agents['vehicles'])
        # Sorted in increasing order
        vehicles_ordered_weight = sorted(self.agents['vehicles'].items(), key = lambda v: v[1].vehicle_total_weight)
        vehicles_ordered_volume = sorted(self.agents['vehicles'].items(), key = lambda v: v[1].vehicle_total_volume)
        while True:
            clustering = AgglomerativeClustering(n_clusters=n_clusters, compute_distances=True)
            labels = clustering.fit_predict(clients)
            clusters_weight = {label: 0 for label in labels}
            clusters_volume = {label: 0 for label in labels}
            for i,client in enumerate(self.agents['clients'].values()):
                clusters_weight[labels[i]] += client.total_weight_kg
                clusters_volume[labels[i]] += client.total_volume_m3
                # Compare current clusters to vehicles max.
                max_weight = vehicles_ordered_weight[-1][1].vehicle_total_weight
                max_volume = vehicles_ordered_volume[-1][1].vehicle_total_volume
                if clusters_weight[labels[i]] > max_weight or clusters_volume[labels[i]] > max_volume:
                    print(clusters_weight[labels[i]],max_weight)
                    n_clusters += 1
                    break
                # clusters[labels[i]].append(self.agents['clients'][client])
                self.agents['clients'][client].route_id = results[i]

            if(n_clusters > 20):
                break
        clusters_weight = sorted(clusters_weight.items(), key = lambda c: c[1])
        clusters_volume = sorted(clusters_volume.items(), key = lambda c: c[1])
        print(clusters_weight)
        print(clusters_volume)
        clusters = {label: [] for label in labels }

    def assign_clients_to_vehicles(self,l):
        liste_vehicules =  list(self.agents['vehicles'].values())
        for v in liste_vehicules:
            v.clients = []
            j = 0
            while j < len(l) and v.add_client_order(l[j]) != False:
                v.attribute_client_to_vehicle(l[j])
                l.pop(j)
                j += 1
        return(liste_vehicules)
    
    def assign_heuristics_to_vehicles(self,liste_vehicules):
        self.schedule = mesa.time.RandomActivation(self)
        for v in liste_vehicules:
            v.algorithm = []
            v.attribute_algorithm_to_vehicle(self,0.5,0.2,100,0.0,0.0,"genetic")
            v.attribute_algorithm_to_vehicle(self,0.0,0.0,50,0.0,0.0,"taboo")
            v.attribute_algorithm_to_vehicle(self,0.0,0.0,0,10,0.9,"rs")
            # if len(v.clients) == 0 :
            #     for i in v.algorithm:
            #         i.mins.append(0)
            # if len(v.clients) == 1 :
            #     for i in v.algorithm:
            #         i.prev_solus.append(v.clients[0])
            #         i.mins.append(1)
            # else :
            self.schedule.add(v)

    def find_best_sol(self,nb_ite,liste_vehicules,nb_algs):
        self.assign_heuristics_to_vehicles(liste_vehicules)
        for i in range(nb_ite):
            self.step()
        total_by_alg = [0]*nb_algs
        for v in liste_vehicules:
            v.plot_graph_v(nb_algs,total_by_alg)
            min_result = v.algorithm[0].mins[-1]
            min_result_index = 0
            for i in range(len(v.algorithm)):
                if v.algorithm[i].mins[-1] < min_result :
                    min_result = v.algortithm[i].mins[-1]
                    min_result_index = i
            if len(v.clients) > 0:
                v.clients = v.algorithm[min_result_index].prev_solus[-1]
            v.algorithm = []
        return(total_by_alg)

    def solution_cost(self,liste_vehicules):
        total_sol = 0
        for v in liste_vehicules:
            total_sol += v.f_cout(v.clients)
        return(total_sol)

    def step(self):
        self.schedule.step()
    