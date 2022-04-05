import mesa.time
import random as rd
from math import sin, cos, sqrt, atan2, radians, exp


#s=random_sol()

class RSAgent(mesa.Agent):
    
  def __init__(self,id, model, vehicule):
     super().__init__(id, model)
     self.id = id        
     self.s_et=vehicule.liste_clients  #solution actuelle
     self.nb_iter =0  #nombre d'itérations
     self.nb_iter_cycle = 2    #☻nombre d'itérations par cycle
     self.nv_cycle = True   #s'agit-il d'un nouveau cycle ou non
     self.t=100   #température
     self.cout = 0    #cout de la solution actuelle
     self.a = 0.5
     self.w = 100
    
  def step(self,s, vehicule):
     self.nb_iter=0
     self.nv_cycle=False
     while(self.nb_iter<self.nb_iter_cycle and self.t!=0):
         self.nb_iter+=1
         s1=neighbour(s)
         cout_s=vehicule.cout
         vehicule.liste_clients=s1
         vehicule.cout = vehicule.f_cout()
         cout_s1=vehicule.cout
         df=cout_s1 - cout_s
         if(df<0):
             #s=s1
             self.nv_cycle=True
         else:
             prob=exp(-df/self.t)
             q=rd.random()
             if(q<prob):
                 #s=s1
                 self.nv_cycle=True
             else:
                 vehicule.liste_clients =s
                 vehicule.cout = cout_s
         if(f(s,self.w)<f(self.s_et,self.w)):
             self.s_et=s
     self.t*=self.a
     self.cout = f(self.s_et,self.w)



     def random_sol():
         s=[1, 2, 4, 3, 7, 8, 9, 5, 6]
         for k in range(1,nb_camions):
             s.append(0)
         rd.shuffle(s)
         s = [0]+s+[0]
         return s
    
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
    
    
    
     def distance(long_a,lat_a,long_b,lat_b):
         k=6373.0 #rayon de la terre
         d_long = radians(long_b) - radians(long_a)
         d_lat = radians(lat_b) - radians(lat_a)
         x = sin(d_lat / 2)**2 + cos(radians(lat_a)) * cos(radians(lat_b)) * sin(d_long / 2)**2
         z = 2 * atan2(sqrt(x), sqrt(1 - x))
         return k*z
    
    
     def f(s,w,rows_table_customers):
         somme=0
         for i in range(len(s)):
             for j in range(len(s[0])-1):
                 somme+=distance(rows_table_customers[s[i],4],rows_table_customers[s[i],3],rows_table_customers[s[j],4],rows_table_customers[s[j],3])
         return w*K(s)+somme
    
     def K(s):
         return len(s)
