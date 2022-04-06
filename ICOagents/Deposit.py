from ICOagents import Geo, Client, Vehicle
import mesa

class Agent(Geo.Agent):
    '''Deposit Agent'''
    def __init__(self, model, series):
        super().__init__(model, series['DEPOT_CODE'],series['DEPOT_LATITUDE'],series['DEPOT_LONGITUDE'])
    
    def assign_clients(self, vehicles, clients):
        pass
    def step():
        pass

class Route(mesa.Agent):
    '''Agent that represents a route'''
    def __init__(self, model, code):
        super().__init__(model.next_id(), model)
        self.id = model.current_id
        self.code = code
        self.agents = {"deposits": {},"vehicles": {}, "clients": {}}
        self.vehicles = []
    def add_agent(self,agent, verbose = False):
        if type(agent) is Agent:
            self.agents['deposits'][agent.code] = agent
        elif type(agent) is Vehicle.Agent:
            self.agents['vehicles'][agent.code] = agent
        elif type(agent) is Client.Agent:
            self.agents['clients'][agent.code] = agent
        elif verbose:
            print("Entity not found")
    def 


# def assign_clients(self,liste_vehicules,liste_client):
#         # adapt
#         j = 0
#         for i in range(len(liste_vehicules)):
#             while liste_vehicules[i].add_client_order(liste_client.liste[j]) != False:
#                 liste_vehicules[i].attribute_client_to_vehicle(liste_client.liste[j])
#                 j += 1

# class Liste_Clients:
#     '''Special list object that contains clients'''
#     
#         self.id = unique_id
#         self.liste = []
    
#     def shuffle_list(self):
#         self.liste = random.shuffle(self.liste)

#     def permutation_list(self):
#         result = self.liste.copy()
#         n=len(result)
#         i=random.randint(0,n-1)
#         j=random.randint(0,n-1)
#         while(i==j):
#             j=random.randint(1,n-2)
#         x=result[i]
#         result[i]=result[j]
#         result[j]=x
#         return(result)
    
#     #Le croisement ne marche que si les deux listes sont de même longueur
#     def croisement_list(self, liste_clients):
#         s = len(self.liste)
#         resultat1 = self.liste.copy()
#         resultat2 = liste_clients.liste.copy()
#         point = random.randint(0, s-1)
#         for i in range(point, s) :
#             resultat1[i], resultat2[i] = resultat2[i], resultat1[i]
#         resultat1 = self.verifSolu(resultat1, self)
#         resultat2 = self.verifSolu(resultat2, self)
#         return(resultat1, resultat2)

#     def add_client_to_list(self, client):
#         self.liste.append(client)
    
#     def verifSolu(resultat, self) :
#         Absents = []
#         Doublons = []
#         resultatf = resultat.copy()
#         for i in self.liste :
#             instances = 0
#             for j in range(len(resultat)):
#                 if resultat[j].customer_code == i.customer_code and instances == 0 :
#                     instances += 1
#                 elif resultat[j].customer_code == i.customer_code and instances == 1 :
#                     Doublons.append([i,j])
#             if instances == 0 :
#                 Absents.append(i)
#         for k in range(len(Doublons)) :
#             resultatf[Doublons[k][1]] = Absents[k]
#         if len(Absents) > len(Doublons) :
#             for l in range(len(Doublons), len(Absents)) :
#                 resultatf.append(Absents[l])
#         return(resultatf)
