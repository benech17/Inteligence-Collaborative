import mesa
from mesa.time import RandomActivation
import pandas
import random

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

    def make_clusters(self):
        pass


    def assign_clients_to_vehicles(self,l):
        liste_vehicules =  list(self.agents['vehicles'].values())
        for v in liste_vehicules:
            v.clients = []
            j = 0
            while v.add_client_order(l[j]) != False:
                v.attribute_client_to_vehicle(l[j])
                j += 1
    
    def assign_heuristics_to_vehicles(self):
        self.schedule = mesa.time.RandomActivation(self)
        for v in self.agents['vehicles'].values():
            v.algorithm = []
            v.attribute_algorithm_to_vehicle(self,0.5,0.2,100,"genetic")
            v.attribute_algorithm_to_vehicle(self,0.0,0.0,50,"taboo")
            self.schedule.add(v)
    
    def step(self):
        if self.planning:
            print("Planning!")
        else:
            self.schedule.step()
            print("Delivering!")
    
    def plot_graphs_agents(self,nb_ite):
        total = [0]*nb_ite
        for v in self.agents['vehicles'].values():
            if len(v.clients) == 0:
                evol_cout = [0]*nb_ite #simulation d'un aller-retour au dépot
            elif len(v.clients) == 1:
                evol_cout = [1]*nb_ite #simulation d'un aller-retour au dépot
            else:
                for a in v.algorithm:
                    plt.plot(a.mins)
                    plt.title("Courbe de résultats de l'algorithme " + type(a).__name__)
                    plt.xlabel("Nombre d'itérations")
                    plt.ylabel('Coût trouvé')
                    plt.show()
                    evol_cout = a.mins
            for i in range(nb_ite):
                total[i] += evol_cout[i]
        return(total[-1])
    
    def find_best_sol(self,route_num,nb_permut,nb_ite):
        l = self.agents['routes'][route_num]
        cout = 0
        permutations_f = []
        couts_f = []
        for i in range(nb_permut):
            sol = []
            a = l.copy()
            random.shuffle(a)
            self.agents['vehicles'].clear()
            self.read_vehicles('Data/3_detail_table_vehicles.csv', w = 0)
            self.assign_clients_to_vehicles(a)
            self.assign_heuristics_to_vehicles()
            for i in range(nb_ite):
                self.step()
            cout = self.plot_graphs_agents(nb_ite)
            for v in self.agents['vehicles'].values():
                b = []
                for k in v.algorithm:
                    for h in k.prev_solus[-1]:
                        b.append(h.code) 
                sol.append(b)
            permutations_f.append(sol) #permet de récupérer la meilleure solution associée à chaque route
            couts_f.append(cout)
        print(permutations_f[0])
        print(permutations_f[9])
        # plt.plot(couts_f)
        # plt.title("Evolution ")
        # plt.xlabel("Nombre d'itérations")
        # plt.ylabel('Coût trouvé')
        # plt.show()