import pandas
import mesa

class Agent(mesa.Agent):
    '''Agent that reads the files'''
    
    def __init__(self,model):
        '''Read Agent constructor'''
        super().__init__(model.next_id(), model)

    def read_and_drop(self, path, drop_code):
        '''Reads a CSV and drops duplicates by code'''
        return pandas.read_csv(path).drop_duplicates(subset = [drop_code]).reset_index()

    def read_deposits(self, path = 'Data/4_detail_table_depots.csv'):
        '''Reads deposits from file and returns pandas dataframe'''
        self.deposits = self.read_and_drop(path,'DEPOT_CODE')[['DEPOT_NUMBER','DEPOT_CODE','DEPOT_LATITUDE','DEPOT_LONGITUDE']]

    def read_clients(self, path = 'Data/2_detail_table_customers.csv'):
        '''Reads clients from file and returns pandas dataframe'''
        self.clients = self.read_and_drop(path,'CUSTOMER_CODE')[['CUSTOMER_NUMBER','CUSTOMER_CODE','CUSTOMER_LATITUDE','CUSTOMER_LONGITUDE','NUMBER_OF_ARTICLES','TOTAL_WEIGHT_KG','TOTAL_VOLUME_M3']]
    
    def read_vehicles(self, path = 'Data/3_detail_table_vehicles.csv'):
        '''Reads vehicles from file and returns pandas dataframe'''
        self.vehicles = self.read_and_drop(path,'VEHICLE_CODE')[['VEHICLE_CODE','VEHICLE_TOTAL_VOLUME_M3','VEHICLE_TOTAL_WEIGHT_KG','VEHICLE_FIXED_COST_KM','VEHICLE_VARIABLE_COST_KM']]
    
    def read_cost_distances(self, path = 'Data/6_detail_table_cust_depots_distances.csv'):
        '''Reads the cost distance (customer->deposit and vice-versa) from file and returns pandas dataframe'''
        self.costs = pandas.read_csv(path).reset_index()
        self.costs = self.costs[['CUSTOMER_NUMBER','DEPOT_CODE','CUSTOMER_CODE','DIRECTION','DISTANCE_KM','TIME_DISTANCE_MIN']]
    
    def __str__(self):
        dep = '['+str(self.deposits.shape[0])+','+str(self.deposits.shape[1])+'] deposits'
        cli = '['+str(self.clients.shape[0])+','+str(self.clients.shape[1])+'] clients'
        veh = '['+str(self.vehicles.shape[0])+','+str(self.vehicles.shape[1])+'] vehicles'
        cos = '['+str(self.costs.shape[0])+','+str(self.costs.shape[1])+'] costs'
        return "Reader with "+', '.join([dep,cli,veh,cos])

    def step():
        pass









