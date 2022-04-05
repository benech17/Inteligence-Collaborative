import mesa
import mesa.time
import pandas

from ICOagents import Client, Deposit, Vehicle

class Model(mesa.Model):
    '''Model is the name for the global model controller'''
    def __init__(self, verbose = False, interface = None):
        super().__init__()
        # Is in planning phase
        self.planning = True
        self.interface = interface
        self.verbose = verbose
        self.deposits = []
        self.vehicles = []
        self.clients = []

    def verbose(verbose):
        '''Changes verbose mode'''
        self.verbose = verbose

    def read_and_drop(self, path, drop_code):
        '''Reads a CSV and drops duplicates by code'''
        return pandas.read_csv(path).drop_duplicates(subset = [drop_code]).reset_index()

    def read_deposits(self, path = 'Data/4_detail_table_depots.csv'):
        '''Reads deposits from file and returns pandas dataframe'''
        self.deposits_df = self.read_and_drop(path,'DEPOT_CODE')[['DEPOT_CODE','DEPOT_LATITUDE','DEPOT_LONGITUDE']]
        if self.verbose:
            print('Read ['+str(self.deposits_df.shape[0])+','+str(self.deposits_df.shape[1])+'] deposits')
            return self.deposits_df

    def read_vehicles(self, path = 'Data/3_detail_table_vehicles.csv'):
        '''Reads vehicles from file and returns pandas dataframe'''
        self.vehicles_df = self.read_and_drop(path,'VEHICLE_CODE')[['VEHICLE_CODE','VEHICLE_TOTAL_VOLUME_M3','VEHICLE_TOTAL_WEIGHT_KG','VEHICLE_FIXED_COST_KM','VEHICLE_VARIABLE_COST_KM']]
        if self.verbose:
            print('Read ['+str(self.vehicles_df.shape[0])+','+str(self.vehicles_df.shape[1])+'] vehicles')
            return self.vehicles_df

    def read_clients(self, path = 'Data/2_detail_table_customers.csv'):
        '''Reads clients from file and returns pandas dataframe''' 
        self.clients_df = self.read_and_drop(path,'CUSTOMER_CODE')[['CUSTOMER_CODE','CUSTOMER_LATITUDE','CUSTOMER_LONGITUDE','NUMBER_OF_ARTICLES','TOTAL_WEIGHT_KG','TOTAL_VOLUME_M3']]
        if self.verbose:
            print('Read ['+str(self.clients_df.shape[0])+','+str(self.clients_df.shape[1])+'] clients')
            return self.clients_df

    def read_cost_distances(self, path = 'Data/6_detail_table_cust_depots_distances.csv'):
        '''Reads the cost distance (customer->deposit and vice-versa) from file and returns pandas dataframe'''
        self.costs_df = pandas.read_csv(path).reset_index()
        self.costs_df = self.costs_df[['CUSTOMER_NUMBER','DEPOT_CODE','CUSTOMER_CODE','DIRECTION','DISTANCE_KM','TIME_DISTANCE_MIN']]
        if self.verbose:
            print('Read ['+str(self.costs_df.shape[0])+','+str(self.costs_df.shape[1])+'] costs')
            return self.costs_df

    def create_deposits(self, df = None):
        '''Creates deposit from DataFrame'''
        if not df:
            df = self.deposits_df
        for index, row in df.iterrows():
            self.deposits.append(Deposit.Agent(self,row))
        if self.verbose:
            print(len(self.deposits),"deposits")
            return self.deposits

    def create_vehicles(self, df = None):
        '''Creates vehicles from DataFrame'''
        if not df:
            df = self.vehicles_df    
        # 0 is the equivalent of w. This needs to be fixed. What is w?
        for index, row in df.iterrows():
            self.vehicles.append(Vehicle.Agent(self,row,0))
        if self.verbose:
            print(len(self.vehicles),"vehicles")
            return self.vehicles

    def step(self):
        if self.planning:
            print("Planning!")
        else:
            print("Delivering!")



#     #construction de la liste des routes, qui sont constituées elles-mêmes d'une liste de clients associées à une demande
#     liste_routes = []
#     route = Liste_Clients(rows_table_customers[0][0])
#     i = 0
#     while i < len(rows_table_customers) :
#         if (i == 0 or rows_table_customers[i][0] == rows_table_customers[i-1][0]) :
#             client = Client(rows_table_customers[i][2], float(rows_table_customers[i][3]), float(rows_table_customers[i][4]), float(rows_table_cust_depots_distances[2*i][5]), float(rows_table_cust_depots_distances[2*i][6]), float(rows_table_cust_depots_distances[2*i+1][5]), float(rows_table_cust_depots_distances[2*i+1][6]), float(rows_table_customers[i][7]), float(rows_table_customers[i][8]), float(rows_table_customers[i][9]))
#             route.add_client_to_list(client)
#         else :
#             liste_routes.append(route)
#             route = Liste_Clients(rows_table_customers[i][0])
#         i += 1
