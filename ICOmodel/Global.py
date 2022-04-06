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
        self.agents = {"deposits": {},"vehicles": {}, "clients": {}, "routes":{}}

    def add_agent_in_routes(self,row,agent):
        id = row['ROUTE_ID']
        if not id in self.agents['routes']:
            self.agents['routes'][id] = Deposit.Route(self,id)
        self.agents['routes'][id].add_agent(agent, verbose = self.verbose)
        return row

    def read_deposits(self, path):
        '''Reads deposits from file and returns pandas dataframe'''
        df = pandas.read_csv(path).reset_index()
        for index, row in df.iterrows():
            id = row['DEPOT_CODE']
            if not id in self.agents['deposits']:
                self.agents['deposits'][id] = Deposit.Agent(self,row)
            self.add_agent_in_routes(row,self.agents['deposits'][id])
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
            self.add_agent_in_routes(row,self.agents['vehicles'][id])
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
            self.add_agent_in_routes(row,self.agents['clients'][id])
        if self.verbose:
            print(df.shape,len(self.agents['clients']),"Clients")
        return df


    def step(self):
        if self.planning:
            print("Planning!")
        else:
            print("Delivering!")
