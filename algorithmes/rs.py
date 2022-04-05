import mesa.time
import random as rd
from math import exp


class RSAgent(mesa.Agent):

    def __init__(self,id, model, vehicule):
        super().__init__(id, model)
        self.id = id        
        #self.s_et=vehicule.liste_clients  #solution actuelle
        self.nb_iter =0  #nombre d'itérations
        self.nb_iter_cycle = 2    #☻nombre d'itérations par cycle
        self.nv_cycle = True   #s'agit-il d'un nouveau cycle ou non
        self.t=100   #température
        self.cout = 0    #cout de la solution actuelle
        self.a = 0.5
        self.w = 100
         
    def step(self, vehicule):
        vehicule_s = vehicule
        agent_eval = EvalAgent()
        while(self.nv_cycle):
            self.nb_iter=0
            self.nv_cycle=False
            while(self.nb_iter<self.nb_iter_cycle and self.t!=0):
                self.nb_iter+=1
                vehicule_s1 = vehicule_s
                vehicule_s1.liste_clients = self.neighbour(vehicule_s.liste_clients)
                vehicule_s1.cout = agent_eval.f_cout(vehicule_s1)
                df=vehicule_s1.cout - vehicule_s.cout
                if(df<0):
                    vehicule_s=vehicule_s1
                    self.nv_cycle=True
                else:
                    prob=exp(-df/self.t)
                    q=rd.random()
                    if(q<prob):
                        vehicule_s=vehicule_s1
                        self.nv_cycle=True
                if(vehicule_s.cout < vehicule.cout):
                    vehicule = vehicule_s
            self.t*=self.a


    
    def neighbour(s):
        """fonction qui, pour une solution s donnée, renvoie une solution N(s) voisine de s
            voisine veut dire ici qu'il n'y a qu'une permutation entre les deux solutions"""
        n=len(s)
        i=rd.randint(1,n-2)
        j=rd.randint(1,n-2)
        while(i==j):
            j=rd.randint(1,n-2)
        x=s[i]
        s[i]=s[j]
        s[j]=x
        return s



