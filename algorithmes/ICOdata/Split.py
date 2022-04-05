import mesa.time

class Agent(mesa.Agent):
  def __init__(self,id, model):
    super().__init__(id, model)
    self.id = id
    
  def assign_clients(self,liste_vehicules,liste_client,depot):
    j = 0
    for i in range(len(liste_vehicules)):
      while liste_vehicules[i].add_client_order(liste_client.liste[j]) != False:
        liste_vehicules[i].attribute_client_to_vehicle(liste_client.liste[j])
        j += 1
      liste_vehicules[i].liste_clients.append(depot)
    
