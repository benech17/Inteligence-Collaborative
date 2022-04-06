from ICOagents import Geo, Client, Vehicle
import mesa

class Agent(Geo.Agent):
    '''Deposit Agent'''

    # Back to Deposit class
    def __init__(self, model, series):
        super().__init__(model, series['DEPOT_CODE'],series['DEPOT_LATITUDE'],series['DEPOT_LONGITUDE'])
        self.routes = []
        
    def add_route(self, code):
        pass
    def add_vehicles_in_route(self,vehicle):
        pass

    def assign_clients(self, vehicles, clients):
        pass
    def step():
        pass

# class Route(mesa.Agent):
#     '''Agent that represents a route'''
#     def __init__(self, model, code):
#         super().__init__(model.next_id(), model)
#         self.id = model.current_id
#         self.code = code
#         # Agents is a temporary list for us to organize in the default
#         self.deposit = []
#         # Vehicles is the permanent list to be optimized
#         self.vehicles = {}
#     def add_agent(self,agent, verbose = False):
#         if type(agent) is Agent:
#             self.agents['deposits'][agent.code] = agent
#         elif type(agent) is Vehicle.Agent:
#             self.agents['vehicles'][agent.code] = agent
#         elif type(agent) is Client.Agent:
#             self.agents['clients'][agent.code] = agent
#         elif verbose:
#             print("Entity not found")


# def assign_clients(self,liste_vehicules,liste_client):
#         # adapt
#         j = 0
#         for i in range(len(liste_vehicules)):
#             while liste_vehicules[i].add_client_order(liste_client.liste[j]) != False:
#                 liste_vehicules[i].attribute_client_to_vehicle(liste_client.liste[j])
#                 j += 1

