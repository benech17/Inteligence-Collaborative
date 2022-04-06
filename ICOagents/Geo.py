from math import sin, cos, sqrt, atan2, radians, exp
import mesa

class Agent(mesa.Agent):
    '''Geoagent is an abstract object that has map information'''
    def __init__(self, model, code, lat, lon):
        super().__init__(model.next_id(), model)
        self.code = code
        self.lat = lat
        self.lon = lon
    def distance(self, other):
        '''Calculates distance between object and other point'''
        # K is the radius of the earth
        k = 6373.0 
        d_long = radians(other.lon) - radians(self.lon)
        d_lat = radians(other.lat) - radians(self.lat)
        x = sin(d_lat / 2)**2 + cos(radians(other.lat)) * cos(radians(self.lat)) * sin(d_long / 2)**2
        z = 2 * atan2(sqrt(x), sqrt(1 - x))
        return(k*z)

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
