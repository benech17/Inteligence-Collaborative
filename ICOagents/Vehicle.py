import random
import mesa
    
class Agent(mesa.Agent):
    '''Vehicle Agent'''
    def __init__(self, model, series, w):
        super().__init__(model.next_id(), model)
        self.id = model.current_id
        self.code = series['VEHICLE_CODE']
        self.vehicle_total_weight = series['VEHICLE_TOTAL_WEIGHT_KG']
        self.vehicle_total_volume = series['VEHICLE_TOTAL_VOLUME_M3']
        self.vehicle_fixed_cost_km = series['VEHICLE_FIXED_COST_KM']
        self.vehicle_variable_cost_km = series['VEHICLE_VARIABLE_COST_KM']
        self.vehicle_weight = 0
        self.vehicle_volume = 0
        self.omega = w
        # A list of clients. Attention: Deposits should not be added
        self.clients = []
        self.algorithm = []
        self.verifier = 0
    
    def add_client_order(self, client):
        if (self.vehicle_weight + client.total_weight_kg > self.vehicle_total_weight) or (self.vehicle_volume + client.total_volume_m3 > self.vehicle_total_volume):
            return(False)
        self.vehicle_weight += client.total_weight_kg
        self.vehicle_volume += client.total_volume_m3
        return(True)
    
    def f_cout(self, liste_client):
        d=0
        n=len(liste_client)
        for i in range(n-1):
            d += liste_client[i].calc_dist(liste_client[i+1])
        d+=liste_client[0].depot_to_customer
        d+=liste_client[n-1].customer_to_depot
        return self.omega + d*self.vehicle_fixed_cost_km

    def attribute_client_to_vehicle(self, client):
        if self.add_client_order(client) == True:
            self.liste_clients.append(client)

    def step():
        pass
