from ICOagents import Geo

class Agent(Geo.Agent):
    '''Deposit Agent'''
    def __init__(self, model, series):
        super().__init__(model, series['DEPOT_CODE'],series['DEPOT_LATITUDE'],series['DEPOT_LONGITUDE'])
    
    def assign_clients(self, vehicles, clients):
        pass
    def step():
        pass

# def assign_clients(self,liste_vehicules,liste_client):
#         # adapt
#         j = 0
#         for i in range(len(liste_vehicules)):
#             while liste_vehicules[i].add_client_order(liste_client.liste[j]) != False:
#                 liste_vehicules[i].attribute_client_to_vehicle(liste_client.liste[j])
#                 j += 1
