import mesa
import numpy as np
from random import randint
import random
from ICOagents import Vehicle
import matplotlib.pyplot as plt

class Q_agent(mesa.Agent):
    def __init__(self, model, vhl_list_base, vhl_list_init, ni, st, eps, de_rate, le_rate, di_rate):
        super().__init__(model.next_id(), model)
        self.sol = vhl_list_init
        self.best_sol = vhl_list_base
        self.Q = np.zeros((8,8),float)
        self.no_improvement = 0
        self.max_iter_no_improvement = ni
        self.max_nb_states = st
        self.epsilon = eps
        self.decay_rate = de_rate
        self.learn_rate = le_rate
        self.disc_rate = di_rate
    
    #une des actions du Q-Learning, pouvant retirer la plus petite route non vide ou une route non vide au hasard
    def remove_road(self,typea,liste_vehicules):
        nb_clients = []
        i_selec = 0
        
        for v in liste_vehicules:
            nb_clients.append(len(v.clients))
        
        if typea == "smallest":
            min_clients = nb_clients[0]
            for i in range(len(liste_vehicules)):
                if min_clients > nb_clients[i] and nb_clients[i] != 0:
                    min_clients = nb_clients[i]
                    i_selec = i
        elif typea == "random":
            i_selec = random.randint(0,len(liste_vehicules)-1)
            if nb_clients[i_selec] == 0:
                while nb_clients[i_selec] == 0:
                    i_selec = random.randint(0,len(liste_vehicules)-1)
        
        redistrib = liste_vehicules[i_selec].clients.copy()
        liste_vehicules[i_selec].clients = []
        liste_vehicules[i_selec].vehicle_weight = 0
        liste_vehicules[i_selec].vehicle_volume = 0
        nb_clients[i_selec] = 0
        
        for i in range(len(liste_vehicules)):
            if nb_clients[i] != 0:
                for j in range(len(redistrib)):
                    val = v.attribute_client_to_vehicle(redistrib[j])
                    if val == True:
                        redistrib[j] = 0
                        
        for k in redistrib:
            liste_vehicules[i_selec].attribute_client_to_vehicle(k)
    
    def eps_greedy(self,state):
        if random.uniform(0, 1) < self.epsilon: #random action
            action = randint(0, 7)
        else: # or greedy action
            action = np.argmax(self.Q,axis = 1)[state]
        return action
    
    def choose_action(self,state,typea):
        if typea == 1:
            next_state = self.eps_greedy(state)
        if typea == 2:
            next_state = randint(0, 7)
        return(next_state)
    
    #fonction pour assurer l'intégrité des solutions
    def verifSolu(self, resultat, liste) :
        Absents = []
        Doublons = []
        resultatf = resultat.copy()
        for i in liste :
            instances = 0
            for j in range(len(resultat)):
                if resultat[j].code == i.code and instances == 0 :
                    instances += 1
                elif resultat[j].code == i.code and instances == 1 :
                    Doublons.append([i,j])
            if instances == 0 :
                Absents.append(i)
        for k in range(len(Doublons)) :
            resultatf[Doublons[k][1]] = Absents[k]
        if len(Absents) > len(Doublons) :
            for l in range(len(Doublons), len(Absents)) :
                resultatf.append(Absents[l])
        return(resultatf)
    
    #fonction chargée de faire appliquer les actions sur des véhicules au hasard
    def apply_action(self,action):
        if action == 0:
            i = random.randint(0,len(self.sol)-1)
            verif = self.sol[i].clients.copy()
            self.sol[i].intra_route_swap()
            self.sol[i].clients = self.verifSolu(self.sol[i].clients, verif)
        elif action == 1:
            i = random.randint(0,len(self.sol)-1)
            j = random.randint(0,len(self.sol)-1)
            while i == j :
                j = random.randint(0,len(self.sol)-1)
            self.sol[i].inter_route_swap(self.sol[j])
        elif action == 2:
            i = random.randint(0,len(self.sol)-1)
            verif = self.sol[i].clients.copy()
            self.sol[i].intra_route_shift()
            self.sol[i].clients = self.verifSolu(self.sol[i].clients, verif)
        elif action == 3:
            i = random.randint(0,len(self.sol)-1)
            j = random.randint(0,len(self.sol)-1)
            while i == j :
                j = random.randint(0,len(self.sol)-1)
            self.sol[i].inter_route_shift(self.sol[j])
        elif action == 4:
            i = random.randint(0,len(self.sol)-1)
            verif = self.sol[i].clients.copy()
            self.sol[i].two_intra_route_swap()
            self.sol[i].clients = self.verifSolu(self.sol[i].clients, verif)
        elif action == 5:
            i = random.randint(0,len(self.sol)-1)
            verif = self.sol[i].clients.copy()
            self.sol[i].two_intra_route_shift()
            self.sol[i].clients = self.verifSolu(self.sol[i].clients, verif)
        elif action == 6:
            self.remove_road("smallest", self.sol)
        elif action == 7:
            self.remove_road("random",self.sol)

    def Q_learning(self,nb_ite,pcross,pmut,taille_pop,iter_cycle,refroidissement,typea_list,mode):
        #conditions initiales
        cost_values = [self.model.solution_cost(self.best_sol)[0]]
        cost_values_by_alg = [[self.model.solution_cost(self.best_sol)[0]]*len(typea_list)]
        improved = True
        no_improvement = 0
        state = 0
        
        #on remplit la solution modifiable en copiant la solution initiale/de référence
        for i in range(len(self.best_sol)):
            self.sol[i].clients = self.best_sol[i].clients.copy()
        
        while improved == True: #Tant que l'algo arrive à trouver de meilleures solutions, on refait des épisodes
            #sert à montrer l'évolution du coût pour voir que tout marche bien
            plt.plot(cost_values)
            plt.title("Q-Learning meilleur résultat, mode " + mode)
            plt.xlabel("Nombre d'itérations")
            plt.ylabel('Coût trouvé')
            plt.show()
            
            #paramètres remis à  pour l'épisode
            reward = 0
            states_visited = 0
            state_list = []
            
            #on fait le premier cycle et on regarde si notre nouvelle solution est mieux que la solution de référence
            next_state = self.choose_action(0,2)
            state_list.append(next_state)
            self.apply_action(next_state) #on met à jour self.sol avec la nouvelle action
            self.sol,total_by_alg = self.model.find_best_sol(nb_ite,self.sol,pcross,pmut,taille_pop,iter_cycle,refroidissement,typea_list)
            if self.model.solution_cost(self.sol)[0] < self.model.solution_cost(self.best_sol)[0]:
                reward = self.model.solution_cost(self.best_sol)[0] - self.model.solution_cost(self.sol)[0]
                for i in range(len(self.best_sol)):
                    self.best_sol[i].clients = self.sol[i].clients.copy() #si c'est le cas on met à jour la solution de référence en copiant la solution actuelle
                cost_values.append(self.model.solution_cost(self.best_sol)[0])
                cost_values_by_alg.append(total_by_alg)
            
            #sinon on continue à chercher tant que la solution n'est pas améliorée ou qu'on a dépassé le temps imparti
            else:
                states_visited += 1
                state_list.append(next_state)
                while self.model.solution_cost(self.sol)[0] >= self.model.solution_cost(self.best_sol)[0]:
                    #on choisit et on applique une nouvelle action (qui est aussi l'état suivant)
                    if no_improvement == 0:
                        state = next_state
                        next_state = self.choose_action(state,1)
                    else:
                        next_state = self.choose_action(0,2)
                    self.apply_action(next_state)
                    self.sol,total_by_alg = self.model.find_best_sol(nb_ite,self.sol,pcross,pmut,taille_pop,iter_cycle,refroidissement,typea_list)
                    
                    #si c'est mieux, on garde et on met à jour la matrice Q
                    if self.model.solution_cost(self.sol)[0] < self.model.solution_cost(self.best_sol)[0]:
                        reward += self.model.solution_cost(self.best_sol)[0] - self.model.solution_cost(self.sol)[0]
                        for i in range(len(self.best_sol)):
                            self.best_sol[i].clients = self.sol[i].clients.copy()
                        cost_values.append(self.model.solution_cost(self.best_sol)[0])
                        cost_values_by_alg.append(total_by_alg)
                        improved = True
                        no_improvement = 0
                        self.Q[state,next_state] = (1 - self.learn_rate)*self.Q[state,next_state] + self.learn_rate*(reward + self.disc_rate*np.argmax(self.Q,axis = 1)[next_state])
                        break
                    
                    #sinon on continue à chercher
                    else:
                        if next_state in state_list:
                            states_visited += 1
                        else:
                            state_list.append(next_state)
                        no_improvement += 1
                        if no_improvement > self.max_iter_no_improvement and states_visited == self.max_nb_states:
                            improved = False
                            break
                self.epsilon *= self.decay_rate
        return(self.best_sol,cost_values,cost_values_by_alg,self.Q)
        
        
        
        
        
        
        
        
        


        






































