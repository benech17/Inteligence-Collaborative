import csv

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

class Vehicules:
    def __init__(self, vh_cd, vh_total_wght, vh_total_vol, vh_fx_cost_km, vh_vr_cost_time,vh_speed):
        self.vehicle_code = vh_cd
        self.vehicle_total_weight = vh_total_wght
        self.vehicle_total_volume = vh_total_vol
        self.vehicle_fixed_cost_km = vh_fx_cost_km
        self.vehicle_variable_cost_km = vh_vr_cost_time
        self.vehicle_speed = vh_speed

class Routes:
    def __init__(self, unique_id):
        self.id = unique_id

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