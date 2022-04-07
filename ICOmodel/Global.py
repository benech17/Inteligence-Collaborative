import mesa
from mesa.time import RandomActivation
import pandas
import matplotlib.pyplot as plt

from ICOagents import Client, Deposit, Vehicle

class Model(mesa.Model):
    '''Model is the name for the global model controller'''
    def __init__(self, verbose = False):
        super().__init__()
        self.planning = True
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
            if not id in self.agents['clients']:
                self.agents['clients'][id] = Client.Agent(self,row)
            route_id = row['ROUTE_ID']
            if not route_id in self.agents['routes']:
                self.agents['routes'][route_id] = []
            self.agents['routes'][route_id].append(self.agents['clients'][id])
        # Transforms routes in list
        self.agents['routes'] = list(self.agents['routes'].values())
        if self.verbose:
            print(df.shape,len(self.agents['clients']),"Clients.",len(self.agents['routes']),"Routes")
        return df

    def assign_clients_to_vehicles(self):
        liste_vehicules =  list(self.agents['vehicles'].values())
        l = self.agents['routes'][0]
        for v in liste_vehicules:
            j = 0
            while v.add_client_order(l[j]) != False:
                v.attribute_client_to_vehicle(l[j])
                j += 1
    
    def assign_heuristics_to_vehicles(self):
        self.schedule = mesa.time.RandomActivation(self)
        for v in self.agents['vehicles'].values():
            v.attribute_algorithm_to_vehicle(self,0.01,0.01,100,"genetic")
            self.schedule.add(v)
    
    def step(self):
        if self.planning:
            print("Planning!")
        else:
            self.schedule.step()
            print("Delivering!")
    
    def plot_graphs(self,nb_ite):
        total = [0]*nb_ite
        for v in self.agents['vehicles'].values():
            for a in v.algorithm:
                plt.plot(a.mins)
                plt.title("Courbe de résultats de l'algorithme génétique")
                plt.xlabel("Nombre d'itérations")
                plt.ylabel('Coût trouvé')
                plt.show()
                for i in range(len(a.mins)):
                    total[i] += a.mins[i]
        plt.plot(total)
        plt.title("Courbe de résultats de l'algorithme génétique sur l'ensemble des véhicules")
        plt.xlabel("Nombre d'itérations")
        plt.ylabel('Coût trouvé')
        plt.show()   
