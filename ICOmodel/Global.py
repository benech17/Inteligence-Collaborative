from sklearn.cluster import AgglomerativeClustering
from mesa.time import RandomActivation
from ICOheuristics import Q_Learning
import pandas
import mesa
import random

import matplotlib.pyplot as plt

from ICOagents import Client, Deposit, Vehicle

class Model(mesa.Model):
    '''Model is the name for the global model controller'''
    def __init__(self, verbose = False):
        super().__init__()
        self.verbose = verbose
        self.agents = {"deposits": {},"vehicles": {}, "vehicles_dupl": {}, "clients": {}, "routes": {}}

    #fonctions de lecture des csv
    def read_deposits(self, path):
        '''Reads deposits from file and returns pandas dataframe'''
        df = pandas.read_csv(path).reset_index()
        for index, row in df.iterrows():
            id = row['DEPOT_CODE']
            if not id in self.agents['deposits']:
                self.agents['deposits'][id] = Deposit.Agent(self,row)
        if self.verbose:
            print(df.shape,len(self.agents['deposits']),"Deposits")
        return df
    #fonctions de lecture des csv
    def read_vehicles(self, path, mode, depot, w = 0):
        '''Reads vehicles from file and returns pandas dataframe'''
        df = pandas.read_csv(path).reset_index()
        for index, row in df.iterrows():
            id = row['VEHICLE_CODE']
            if not id in self.agents['vehicles']:
                self.agents['vehicles'][id] = Vehicle.Agent(self,row,w,mode,depot);
                self.agents['vehicles_dupl'][id] = Vehicle.Agent(self,row,w,mode,depot);
        if self.verbose:
            print(df.shape,len(self.agents['vehicles']),"Vehicles")
        return df
    #fonctions de lecture des csv
    def read_clients(self, path):
        '''Reads clients from file and returns pandas dataframe''' 
        df = pandas.read_csv(path).reset_index()
        for index, row in df.iterrows():
            id = row['CUSTOMER_CODE']
            route_id = row['ROUTE_ID']
            if not id in self.agents['clients']:
                self.agents['clients'][id] = Client.Agent(self,row)
            if not route_id in self.agents['routes']:
                self.agents['routes'][route_id] = []
            self.agents['routes'][route_id].append(self.agents['clients'][id])
        # Transforms routes in list
        self.agents['routes'] = list(self.agents['routes'].values())
        if self.verbose:
            print(df.shape,len(self.agents['clients']),"Clients.",len(self.agents['routes']),"Routes")
        return df

    def make_clusters(self):
        model = AgglomerativeClustering(n_clusters=10, compute_distances=True)
        X = clients[['CUSTOMER_LATITUDE','CUSTOMER_LONGITUDE']]
        model = model.fit(X)

    #fonction pour attribuer les clusters
    def assign_clusters_to_vehicles(self,n_clusters):
        liste_vehicules =  list(self.agents['vehicles'].values())
        clients = [[client.lat, client.lon] for client in self.agents['clients'].values()]
        clustering = AgglomerativeClustering(n_clusters, compute_distances=True)
        results = clustering.fit_predict(clients)
        
        grouped_clients = [[]]*n_clusters
        cluster_costs_weight = [0]*n_clusters
        cluster_costs_volume = [0]*n_clusters
        
        for i in range(len(results)):
            c = list(self.agents['clients'].values())[i]
            grouped_clients[results[i]].append(c)
            cluster_costs_weight[results[i]] += c.total_weight_kg
            cluster_costs_volume[results[i]] += c.total_volume_m3
        
        print(results,grouped_clients,cluster_costs_weight,cluster_costs_volume)    
        
        for i,client in enumerate(self.agents['clients']):
            self.agents['clients'][client].route_id = results[i]

    #fonction pour attribuer des clients sans clusters
    def assign_clients_to_vehicles(self,l,liste_vehicules):
        for v in liste_vehicules:
            v.clients = []
            j = 0
            while j < len(l) and v.add_client_order(l[j]) != False:
                v.attribute_client_to_vehicle(l[j])
                l.pop(j)
                j += 1
        return(liste_vehicules)
    
    def assign_heuristics_to_vehicles(self,liste_vehicules, pcross, pmut, taille_pop, iter_cycle, refroidissement, typea_list):
        self.schedule = mesa.time.RandomActivation(self)
        for v in liste_vehicules:
            v.algorithm = []
            for k in typea_list:
                taille = taille_pop
                if k == "genetic":
                    taille = 2*taille_pop
                v.attribute_algorithm_to_vehicle(self, pcross, pmut, taille, iter_cycle, refroidissement, k)
            self.schedule.add(v)

    #fonction faisant tourner le step des algos pour déterminer la meilleure solution
    def find_best_sol(self,nb_ite,liste_vehicules,pcross,pmut,taille_pop,iter_cycle,refroidissement,typea_list):
        #les vehicules récupèrent les algos heuristiques dans typea_list
        self.assign_heuristics_to_vehicles(liste_vehicules,pcross,pmut,taille_pop,iter_cycle,refroidissement,typea_list)
        
        #on fait tourner les algos
        for i in range(nb_ite):
            self.step()
        
        #une fois que chaque algo a tourné, pour chaque client
        total_by_alg = [0]*len(typea_list)
        for v in liste_vehicules:
            
            #on actualise un multiplet qui contiendra les valeurs de la solution optimale trouvée par chaque algo
            if len(v.algorithm) > 0:
                for i in range(len(v.algorithm)):
                    total_by_alg[i] += v.algorithm[i].mins[-1]
            
            #on met à jour la liste des clients du véhicule et on vide les algos lui ayant été attribués
            if v.mode != "collab":
                #v.plot_graph_v(nb_algs,total_by_alg)
                if len(v.algorithm) > 0:
                    min_result = v.algorithm[0].mins[-1]
                    min_result_index = 0
                    for i in range(len(v.algorithm)):
                        total_by_alg[i] += v.algorithm[i].mins[-1]
                        if v.algorithm[i].mins[-1] < min_result :
                            min_result = v.algorithm[i].mins[-1]
                            min_result_index = i
                    v.clients = v.algorithm[min_result_index].prev_solus[-1]
            v.algorithm = []
        
        return(liste_vehicules,total_by_alg)

    #fonction calculant le cout d'une solution complète et renvoyant aussi la solution sous forme de liste des codes des clients associés à chaque véhicule
    def solution_cost(self,liste_vehicules):
        sol = []
        total_sol = 0
        for v in liste_vehicules:
            liste_codes_clients = []
            total_sol += v.f_cout(v.clients)
            for k in v.clients:
                liste_codes_clients.append(k.code)
            sol.append(liste_codes_clients)
        return(total_sol,sol)
    
    #fonction d'eéécution des divers algos depuis le main
    def exec_alg_spec(self,alg_type,mode,sol_base,sol_init,nb_ite,pcross,pmut,taille_pop,iter_cycle,refroidissement,typea_list,max_iter_no_improvement,max_nb_states,epsilon,decay_rate,learn_rate,disc_rate):
        result = [0]*len(typea_list)
        
        #implémentation heuristique indépendants
        if alg_type == "heuristique":
            for v in sol_base :
                v.mode = "enemy"
            for i in range(len(typea_list)):
                self.assign_heuristics_to_vehicles(sol_base,pcross,pmut,taille_pop,iter_cycle,refroidissement,[typea_list[i]])
                for j in range(nb_ite):
                    self.step()
                total_sol = [0]
                for v in sol_base:
                    v.plot_graph_v(1,total_sol)
                    v.algorithm = []
                result[i] = total_sol[0]
            return(result)
        
        #implémentation sma simple
        elif alg_type == "sma":
            self.assign_heuristics_to_vehicles(sol_base,pcross,pmut,taille_pop,iter_cycle,refroidissement,typea_list)
            for i in range(nb_ite):
                self.step()
            for v in sol_base:
                v.plot_graph_v(len(typea_list),result)
                if v.mode != "collab":
                    if len(v.algorithm) > 0:
                        min_result = v.algorithm[0].mins[-1]
                        min_result_index = 0
                        for i in range(len(v.algorithm)):
                            if v.algorithm[i].mins[-1] < min_result :
                                min_result = v.algorithm[i].mins[-1]
                                min_result_index = i
                        v.clients = v.algorithm[min_result_index].prev_solus[-1]
                v.algorithm = []
            
            if mode != "independance":
                result = self.solution_cost(sol_base)[0]
            return(result)
            
        #implémentation avec Q-Learning
        elif alg_type == "qlearn":
            learner = Q_Learning.Q_agent(self,sol_base,sol_init,max_iter_no_improvement,max_nb_states,epsilon,decay_rate,learn_rate,disc_rate)
            solu_f,liste_couts,liste_couts_par_algo,Q = learner.Q_learning(nb_ite,pcross,pmut,taille_pop,iter_cycle,refroidissement,typea_list,mode)
            result = liste_couts_par_algo[-1]
            
            simultaneous = []
            for i in range(len(typea_list)):
                liste = []
                for j in liste_couts_par_algo:
                    liste.append(j[i])
                simultaneous.append(liste)
            
            for i in range(len(typea_list)):
                plt.plot(simultaneous[i])
            plt.title("Q-Learning par algo, mode " + mode)
            plt.xlabel("Nombre d'itérations")
            plt.ylabel('Coût trouvé')
            plt.show()
            
            if mode != "independance":
                result = self.solution_cost(sol_base)[0]
            return(result)
        
        else:
            print("Unrecognized alg type")

    def step(self):
        self.schedule.step()
    