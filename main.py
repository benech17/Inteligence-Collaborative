# from ICOinterface import Streamlit
from ICOmodel import Global
import random
import matplotlib.pyplot as plt

if __name__ == "__main__":
    '''Main function of the program'''
    # Creates the model and read files
    model = Global.Model(verbose = True)
    # Model reads files and create agents
    deps = model.read_deposits('Data/4_detail_table_depots.csv')
    clis = model.read_clients('Data/2_detail_table_customers.csv')
    # model.assign_clusters_to_vehicles()
    
    # Comment everything here if you don't want streamlit viz!
    # Streamlit.title('Welcolme to ICOnprend Rien')
    # Streamlit.text("Created by Andreis, Colin, Mehdi, Yaniv, Paul and James")
    # Streamlit.header("1. Data")
    # Streamlit.text("Let's start by reading the data with Pandas")
    # Streamlit.text("Here are the deposits")
    # Streamlit.table(deps)
    # Streamlit.text("Here are the clients")
    # Streamlit.table(clis)
    # Streamlit.header("2. Map")
    # Streamlit.text("Let's start by plotting the map with the clustering")
    # Streamlit.map(model)
    
    nb_ite = 20
    route_num = len(model.agents['routes'])
    nb_algs = 3
    
    #Q-Learning params
    max_iter_no_improvement = 10
    max_nb_states = 8
    epsilon = 0.8
    decay_rate = 0.8
    learn_rate = 0.4
    disc_rate = 0.6
    
    #Heuristic params
    pcross = 0.2
    pmut = 0.5
    taille_pop = 25
    iter_cycle = 10
    refroidissement = 0.9
    w = 0
    
    typea_list = ["genetic","taboo","rs"]
    
    #décommenter pour le premier tableau (mode indépendance des algos heuristiques)
    alg_list = ["heuristique","sma","qlearn"]
    mode = "independance"
    res_heurist1 = []
    res_sma1 = []
    res_qlearn1 = []
    total1 = [res_heurist1,res_sma1,res_qlearn1]
    for i in range(route_num):
        for j in range(len(alg_list)):
            l = model.agents['routes'][i].copy()
            model.agents['vehicles'].clear()
            model.agents['vehicles_dupl'].clear()
            model.read_vehicles('Data/3_detail_table_vehicles.csv', mode, list(model.agents['deposits'].values())[0], w)
            sol_init = list(model.agents['vehicles_dupl'].values())
            sol_base = model.assign_clients_to_vehicles(l,list(model.agents['vehicles'].values()))
            res = model.exec_alg_spec(alg_list[j],"independance",sol_base,sol_init,nb_ite,pcross,pmut,taille_pop,iter_cycle,refroidissement,typea_list,max_iter_no_improvement,max_nb_states,epsilon,decay_rate,learn_rate,disc_rate)
            total1[j].append(res)
    
    for k in range(len(total1)):
        simultaneous = []
        for i in range(len(typea_list)):
            liste = []
            for j in total1[k]:
                liste.append(j[i])
            simultaneous.append(liste)
        
        for i in range(len(typea_list)):
            plt.plot(simultaneous[i])
        if k == 0:
            alg = "heuristique "
        elif k == 1:
            alg = "SMA "
        elif k == 2:
            alg = "Q-Learning "
        plt.title("Affichage des solutions par algo " + alg + mode)
        plt.xlabel("Route")
        plt.ylabel('Coût trouvé')
        plt.show()
    
    #décommenter pour le second tableau (mode interaction des algos heuristiques) attention c long
    # alg_list = ["sma","qlearn"]
    # mode = "collab"
    # res_sma2 = [[],[]]
    # res_qlearn2 = [[],[]]
    # total2 = [res_sma2,res_qlearn2]
    # for i in range(route_num):
    #     for j in range(len(alg_list)):
    #         optimums = []
    #         mode = "collab"
    #         for k in range(4):
    #             if k == 0:
    #                 heuristic_comb = [typea_list[0],typea_list[1]]
    #             if k == 1:
    #                 heuristic_comb = [typea_list[0],typea_list[2]]
    #             if k == 2:
    #                 heuristic_comb = [typea_list[1],typea_list[2]]
    #             if k == 3:
    #                 heuristic_comb = typea_list
    #             l = model.agents['routes'][i].copy()
    #             model.agents['vehicles'].clear()
    #             model.agents['vehicles_dupl'].clear()
    #             model.read_vehicles('Data/3_detail_table_vehicles.csv', mode, list(model.agents['deposits'].values())[0], w)
    #             sol_init = list(model.agents['vehicles_dupl'].values())
    #             sol_base = model.assign_clients_to_vehicles(l,list(model.agents['vehicles'].values()))
    #             opt = model.exec_alg_spec(alg_list[j],mode,sol_base,sol_init,nb_ite,pcross,pmut,taille_pop,iter_cycle,refroidissement,heuristic_comb,max_iter_no_improvement,max_nb_states,epsilon,decay_rate,learn_rate,disc_rate)
    #             optimums.append(opt)
    #         total2[j][0].append(optimums)
            
    #         optimums = []
    #         mode = "ennemi"
    #         for k in range(4):
    #             if k == 0:
    #                 heuristic_comb = [typea_list[0],typea_list[1]]
    #             if k == 1:
    #                 heuristic_comb = [typea_list[0],typea_list[2]]
    #             if k == 2:
    #                 heuristic_comb = [typea_list[1],typea_list[2]]
    #             if k == 3:
    #                 heuristic_comb = typea_list
    #             l = model.agents['routes'][i].copy()
    #             model.agents['vehicles'].clear()
    #             model.agents['vehicles_dupl'].clear()
    #             model.read_vehicles('Data/3_detail_table_vehicles.csv', mode, list(model.agents['deposits'].values())[0], w)
    #             sol_init = list(model.agents['vehicles_dupl'].values())
    #             sol_base = model.assign_clients_to_vehicles(l,list(model.agents['vehicles'].values()))
    #             opt = model.exec_alg_spec(alg_list[j],mode,sol_base,sol_init,nb_ite,pcross,pmut,taille_pop,iter_cycle,refroidissement,heuristic_comb,max_iter_no_improvement,max_nb_states,epsilon,decay_rate,learn_rate,disc_rate)
    #             optimums.append(opt)
    #         total2[j][1].append(optimums)
        
    # for k in range(len(total2)):
    #     for h in range(total2[k]):
    #         simultaneous = []
    #         for i in range(4):
    #             liste = []
    #             for j in k[h]:
    #                 liste.append(j[i])
    #             simultaneous.append(liste)
        
    #         for i in range(4):
    #             plt.plot(simultaneous[i])
    #         if k == 0:
    #             alg = "SMA "
    #         elif k == 1:
    #             alg = "Q-Learning "
    #         if h == 0:
    #             mode = "collab"
    #         elif h == 1:
    #             mode = "ennemi"
    #         plt.title("Affichage des solutions pour " + alg + mode)
    #         plt.xlabel("Route")
    #         plt.ylabel('Coût trouvé')
    #         plt.show()
    