import mesa
import mesa.time
import pandas

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
                self.agents['routes'][route_id] = Client.Liste_Clients(self)
            self.agents['routes'][route_id].add_client_to_list(self.agents['clients'][id])
        # Transforms routes in list
        self.agents['routes'] = list(self.agents['routes'].values())
        if self.verbose:
            print(df.shape,len(self.agents['clients']),"Clients.",len(self.agents['routes']),"Routes")
        return df

    def assign_clients_to_vehicle(self):
        liste_vehicules =  list(self.agents['vehicles'].values())
        # l = self.agents['routes'][2946091]
        l = self.agents['routes'][0]
        print(len(l.liste))
        for l in self.agents['routes']:
            for v in liste_vehicules:
                j = 0
                while v.add_client_order(l.liste[j]) != False:
                    v.attribute_client_to_vehicle(l.liste[j])
                    j += 1

    def verify_vehicles(self):
        total = 0
        for v in self.agents['vehicles'].values():
            t = len(v.clients.liste)
            total+=t
            print(t)
        print(total)
    
    def step(self):
        if self.planning:
            print("Planning!")

        else:
            print("Delivering!")
