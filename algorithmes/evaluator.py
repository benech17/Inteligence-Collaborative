import mesa

class EvalAgent(mesa.Agent):
    def __init__(self,w,vh):
        self.omega = w
        self.cout = 0
        self.vehicule=vh
    
    def f_cout(self, vehicule):
        d=0
        n=len(vehicule.liste_clients)
        for i in range(n-1):
            d += vehicule.liste_clients[i].calc_dist(vehicule.liste_clients[i+1])
        d+=vehicule.liste_clients[0].depot_to_customer
        d+=vehicule.liste_clients[n-1].customer_to_depot
        return self.omega + d*vehicule.vehicle_fixed_cost_km