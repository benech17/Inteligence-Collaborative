from ssl import PROTOCOL_TLS_SERVER
import mesa
import numpy as np
import random as rd
from mesa.datacollection import DataCollector

class TabouAgent(mesa.Agent):
    def __init__(self,id, model,vhl,taille):
        super().__init__(id, model)
        self.id = id
        self.s = 0
        self.vehicule = vhl
        self.pop_size = taille
        self.dc = DataCollector({"solution": lambda m: self.f_main() })
        
        


    
    def ordre(solu,demande):
        newq=[];
        newq.clear();
        for i in range(len(solu)):
            for j in range(len(demande)):
                if j+1==solu[i]:
                    newq.append(demande[j])
        return newq
    
    def routes(solu,dmd):
        soma=0;
        tabu=[];
        R=len(solu)
        i=0
        while i<R:
            soma=soma+dmd[i]
            if soma<=Q:
                tabu.append(solu[i])
                i=i+1
            else:
                tabu.append(0)
                soma=0
        tabu.append(0)
        tabu.insert(0,0)
        return tabu
        
    def f_cout(solu):
        cout=0;
        for i in range(len(solu)):
            if i<len(solu)-1:
                cc=C[solu[i],solu[i+1]]
                cout=cout+cc
        return cout
        
    def f_main(self):
        coutf=100000000000001 #cout final initial
        ite=0; #compteur du nombre d'iterations
        cfinal=[]
        liste_client =[]
        solution =[]

        for i in it.permutations(N,n):
            if ite==1000:
                break
            else:
                soli = i          #solution initial
                demandf = self.ordre(soli,q) #Demande de chaque arrêt
                sol = self.routes(soli,demandf)#Solution initial
                couti = self.f_cout(sol) #Coût total de cette solution
                
                cfinal.append(couti)
                ite=ite+1;
                if couti<coutf:
                    coutf=couti   #cout final
                    solf=sol #solution finale
                    solution.append(solf)
                    
    
        return(solution)
    
    def step(self):
        print("C'est le step",self.s,"du agent",self.id)
        self.s+=1
        self.dc.collect(self)
