import mesa

class GeneticAgent(mesa.Agent):
    def __init__(self,id, model):
        super().__init__(id, model)
        self.id = id
        self.s = 0
    def step(self):
        print("C'est le step",self.s,"du agent",self.id)
        self.s+=1



class Algo_Gen(mesa.Agent):
    
    def __init__(self, u_id, model,clients,nbClients,demande,capacite,Pcross,Pmut,taille,ite):
        
        self.clients = clients
        self.nbClients = nbClients
        self.demande = demande
        self.capacite = capacite
        self.Pcross = Pcross
        self.Pmut = Pmut
        self.taille = taille
        self.ite = ite
        
        self.dob = id
    
    
    def step(self):
        pass
        # prePop = generateur(self.clients, self.nbClients, self.taille)
        # solf = []
        # coutf = 0
        # t = 0
        # while t <= ite :
        #     forceTriee, prePopTriee = triInsertion(coutsPopulation(prePop, self.demande, self.capacite), prePop)
        #     solf = routes(prePopTriee[0], self.demande, self.capacite)
        #     coutf = coutsPopulation(prePopTriee, self.demande, self.capacite)[0]
        
        #     #construction de S(t)
        #     listeProba = proba(forceTriee, prePopTriee)
        #     #print(listeProba)
        #     S1 = constructS(listeProba, self.taille)
        
        #     #construction de S(t+1)
        #     S2 = []
        #     for i in range(0,len(S1),2) :
        #         if random.random() < self.Pcross :
        #             a,b = croisement(S1[i], S1[i+1], self.clients)
        #             S2.append(a)
        #             S2.append(b)
        #         else :
        #             S2.append(S1[i])
        #             S2.append(S1[i+1])
        
        #     #construction de P(t+1)
        #     prePop = []
        #     for i in S2 :
        #         if random.random() < self.Pmut :
        #             prePop.append(mutations(i,self.clients))
        #         else :
        #             prePop.append(i)
        #     t += 1
        #     #print(prePopTriee,forceTriee)
        # return(solf,coutf)
