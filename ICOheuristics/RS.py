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
        self.mins = []
        self.liste_clients_f = self.prev_solus[-1].copy()
        self.a = refroidissement
        #self.dc = DataCollector({"solution": lambda m: self.f_main() })
    
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
        if(self.nv_cycle):
            self.nb_iter = 0
            self.nv_cycle = False
            while self.nb_iter < self.nb_iter_cycle :
                self.nb_iter += 1
                solu_voisine = self.permutation_list(self.liste_clients_f)
                df = self.vehicule.f_cout(solu_voisine) - self.vehicule.f_cout(self.liste_clients_f)
                if df < 0 :
                    self.liste_clients_f = solu_voisine
                    self.nv_cycle=True
                else:
                    prob = exp(-df/self.temp)
                    q=rd.random()
                    if q < prob :
                        self.liste_clients_f = solu_voisine
                        self.nv_cycle=True
                if self.vehicule.f_cout(self.liste_clients_f) < self.vehicule.f_cout(self.prev_solus[-1]) :
                    self.prev_solus.append(self.liste_clients_f)
                    self.mins.append(self.vehicule.f_cout(self.liste_clients_f))
            self.temp *= self.a
        print("je suis dans le step")
        return(self.liste_clients_f)


