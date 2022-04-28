import mesa.time
import random as rd
from math import exp
from mesa.datacollection import DataCollector

class RSAgent(mesa.Agent):
    def __init__(self,model,vhl,iter_cycle,refroidissement):
        super().__init__(model.next_id (), model)
        self.vehicule = vhl
        self.nb_iter =0  #nombre d'itérations
        self.nb_iter_cycle = iter_cycle    #nombre d'itérations par cycle
        self.nb_iter =0  #nombre d'itérations
        self.nv_cycle = True   #s'agit-il d'un nouveau cycle ou non
        self.temp = 100   #température
        self.prev_solus = [self.vehicule.clients.copy()]
        self.mins = [self.vehicule.f_cout(self.vehicule.clients)]
        self.liste_clients_f = self.prev_solus[-1].copy()
        self.a = refroidissement
    
    def permutation_list(self, liste):
        result = liste.copy()
        n=len(result)
        i=rd.randint(0,n-1)
        j=rd.randint(0,n-1)
        while(i==j):
            j=rd.randint(0,n-1)
        x=result[i]
        result[i]=result[j]
        result[j]=x
        return(result)

    def step(self):
        #on exploite les informations des autres algos si elles sont meilleures que la solution trouvée
        if self.liste_clients_f != self.vehicule.clients and self.vehicule.mode == "collab" :
            self.liste_clients_f = self.vehicule.clients.copy()
        
        #on vérifie qu'on se situe dans un nouveau cycle
        if(self.nv_cycle):
            self.nb_iter = 0
            self.nv_cycle = False
            
            #on vérifie qu'on reste dans le cycle
            while self.nb_iter < self.nb_iter_cycle :
                self.nb_iter += 1
                
                #on détermine une solution voisine
                solu_voisine = self.permutation_list(self.liste_clients_f)
                df = self.vehicule.f_cout(solu_voisine) - self.vehicule.f_cout(self.liste_clients_f)
                
                #si elle est meilleure que la solution actuelle on la garde et on peut faire un cycle de plus
                if df < 0 :
                    self.liste_clients_f = solu_voisine
                    self.nv_cycle = True
                
                #sinon on choisit si on la garde ou pas de façon probabiliste
                else:
                    prob = exp(-df/self.temp)
                    q=rd.random()
                    if q < prob :
                        self.liste_clients_f = solu_voisine
                        self.nv_cycle = True
                
                #on conserve la solution seulement si elle est meilleure que la dernière en date
                if self.vehicule.f_cout(self.liste_clients_f) <= self.vehicule.f_cout(self.prev_solus[-1]) :
                    self.prev_solus.append(self.liste_clients_f)
                    self.mins.append(self.vehicule.f_cout(self.liste_clients_f))
            self.temp *= self.a
        return(self.liste_clients_f)


