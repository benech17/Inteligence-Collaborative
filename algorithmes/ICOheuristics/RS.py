import mesa.time
import random as rd
from math import exp


class RSAgent(mesa.Agent):
    
    def __init__(self,id, model):
        super().__init__(id, model)
        self.id = id        
        #self.s_et=vehicule.liste_clients  #solution actuelle
        self.nb_iter =0  #nombre d'itérations
        self.nb_iter_cycle = 2    #nombre d'itérations par cycle
        self.nv_cycle = True   #s'agit-il d'un nouveau cycle ou non
        self.t=100   #température
        self.cout = 0    #cout de la solution actuelle
        self.a = 0.5
        self.w = 100
         
    def step(self, vehicule):
        s=vehicule.liste_clients
        cout_s = self.f_cout(s)
        while(self.nv_cycle):
            self.nb_iter=0
            self.nv_cycle=False
            while(self.nb_iter<self.nb_iter_cycle and self.t!=0):
                self.nb_iter+=1
                s1 = self.neighbour(s)
                cout_s1 = self.f_cout(s1)
                df=cout_s1 - cout_s
                if(df<0):
                    s=s1
                    cout_s=cout_s1
                    self.nv_cycle=True
                else:
                    prob=exp(-df/self.t)
                    q=rd.random()
                    if(q<prob):
                        s=s1
                        cout_s=cout_s1
                        self.nv_cycle=True
                if(cout_s < self.f_cout(vehicule.liste_clients)):
                    vehicule.liste_clients = s
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



