import csv
import random as rd
from math import sin, cos, sqrt, atan2, radians, exp

class Depot:
    def __init__(self, dept_code, dpt_lat, dpt_long):
        self.depot_code = dept_code
        self.depot_latitude = dpt_lat
        self.depot_longitude = dpt_long

class Client:
    def __init__(self, c_code, c_lat, c_long, dtc_km, dtc_time, ctd_km, ctd_time, num_of_art, wght_kg, vol_m3):
        self.customer_code = c_code
        self.customer_latitude = c_lat
        self.customer_longitude = c_long
        self.depot_to_customer_in_km = dtc_km
        self.depot_to_customer_in_time = dtc_time
        self.customer_to_depot_in_km = ctd_km
        self.customer_to_depot_in_time = ctd_time
        self.number_of_articles = num_of_art
        self.total_weight_kg = wght_kg
        self.total_volume_m3 = vol_m3
    
    def calc_dist(self, Client client):
        k=6373.0 #rayon de la terre
        d_long = radians(client.customer_longitude) - radians(self.customer_longitude)
        d_lat = radians(client.customer_latitude) - radians(self.customer_longitude)
        x = sin(d_lat / 2)**2 + cos(radians(lat_a)) * cos(radians(lat_b)) * sin(d_long / 2)**2
        z = 2 * atan2(sqrt(x), sqrt(1 - x))
        return(k*z)

class Vehicules:
    def __init__(self, vh_cd, vh_total_wght, vh_total_vol, vh_fx_cost_km, vh_vr_cost_time):
        self.vehicle_code = vh_cd
        self.vehicle_total_weight = vh_total_wght
        self.vehicle_total_volume = vh_total_vol
        self.vehicle_weight = 0
        self.vehicle_volume = 0
        self.vehicle_fixed_cost_km = vh_fx_cost_km
        self.vehicle_variable_cost_km = vh_vr_cost_time
    
    def add_client_order(self, Client client):
        self.vehicle_weight += client.total_weight_kg
        self.vehicle_volume += client.total_volume_m3
        if (self.vehicle_weight > self.vehicle_total_weight) or (self.vehicle_volume > self.vehicle_total_volume):
            return(True)
        return(False)

class Liste_Clients:
    def __init__(self, unique_id):
        self.id = unique_id
        self.liste = []
    
    def shuffle_list(self):
        self.liste = rd.shuffle(self.liste)

    def permutation_list(self):
        n=len(self.list)
        i=rd.randint(0,n-1)
        j=rd.randint(0,n-1)
        while(i==j):
            j=rd.randint(1,n-2)
        x=self.list[i]
        self.list[i]=self.list[j]
        self.list[j]=x
    
    #Le croisement ne marche que si les deux listes sont de même longueur
    def croisement_list(self, Liste_Clients liste_clients):
        for i in range(len(self.liste)):
            if p[1][i] in p[0]:    # cannot risk crossover, keep basic gene
                offspring.append(p[0][i])
            else:                  # standard uniform crossover
                offspring.append(p[random.randint(0, 1)][i])

    #Avant de modifier une liste, on peut créer une nouvelle instance dans laquelle on copie le contenu histoire de conserver l'originale
    def copy_list(self, Liste_Clients liste_clients_init):
        self.liste = liste_clients_init.liste.copy()

    def add_client_to_list(self, Client client):
        self.liste.append(client)

def read_files():
    file = open("2_detail_table_customers.csv")
    csvreader = csv.reader(file)
    header = next(csvreader)
    rows_table_customers = []
    for row in csvreader:
        rows_table_customers.append(row)
    file.close()
    file = open("3_detail_table_vehicles.csv")
    csvreader = csv.reader(file)
    header = next(csvreader)
    rows_table_vehicles = []
    for row in csvreader:
        rows_table_vehicles.append(row)
    file.close()
    
    file = open("4_detail_table_depots.csv")
    csvreader = csv.reader(file)
    header = next(csvreader)
    rows_table_depots = []
    for row in csvreader:
        rows_table_depots.append(row)
    file.close()
    
    file = open("6_detail_table_cust_depots_distances.csv")
    csvreader = csv.reader(file)
    header = next(csvreader)
    rows_table_cust_depots_distances = []
    for row in csvreader:
        rows_table_cust_depots_distances.append(row)
    file.close()
    
    #définition du dépôt
    depot = Depot(int(rows_table_depots[0][2]), float(rows_table_depots[0][3]), float(rows_table_depots[0][4]))
    
    #construction de la liste des routes, qui sont constituées elles-mêmes d'une liste de clients associées à une demande
    liste_routes = []
    route = []
    i = 0
    while i < len(rows_table_customers) :
        if (i == 0 or rows_table_customers[i][0] == rows_table_customers[i-1][0]) :
            client = Client(rows_table_customers[i][2], float(rows_table_customers[i][3]), float(rows_table_customers[i][4]), float(rows_table_cust_depots_distances[2*i][5]), float(rows_table_cust_depots_distances[2*i][6]), float(rows_table_cust_depots_distances[2*i+1][5]), float(rows_table_cust_depots_distances[2*i+1][6]), float(rows_table_customers[i][7]), float(rows_table_customers[i][8]), float(rows_table_customers[i][9]))
            route.append(client)
        else :
            liste_routes.append(route)
            route = []
        i += 1
    return rows_table_customers, rows_table_vehicles, rows_table_depots, rows_table_cust_depots_distances, liste_routes, route