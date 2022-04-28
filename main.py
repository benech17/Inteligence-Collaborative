from ICOinterface import Streamlit
from ICOmodel import Global
from ICOheuristics import Q_Learning
import random
import matplotlib.pyplot as plt

if __name__ == "__main__":
    '''Main function of the program'''
    # Creates the model and read files
    model = Global.Model(verbose = True, bar = Streamlit.bar())
    # Model reads files and create agents
    deps = model.read_deposits('Data/4_detail_table_depots.csv')
    clis = model.read_clients('Data/2_detail_table_customers.csv')

    # Comment everything here if you don't want streamlit viz!
    Streamlit.title('Welcolme to ICOnprend Rien')
    Streamlit.text("Created by Andreis, Colin, Mehdi, Yaniv, Paul and James")
    Streamlit.header("1. Data")
    Streamlit.text("Let's start by reading the data with Pandas")
    Streamlit.text("Here are the deposits")
    Streamlit.table(deps)
    Streamlit.text("Here are the clients")
    Streamlit.table(clis)
    Streamlit.header("2. Map")
    Streamlit.text("Let's start by plotting the map with the clustering")
    Streamlit.plot_clustering(model.assign_clusters_to_vehicles())
    Streamlit.map(model)
        
    nb_ite = 2
    route_num = 0
    nb_algs = 3
    max_iter_no_improvement = 10
    max_nb_states = 8
    epsilon = 0.5
    decay_rate = 0.9
    learn_rate = 0.1
    disc_rate = 0.9
    
    Streamlit.header("3. Results")
    #on créé la solution initiale
    l = model.agents['routes'][route_num]
    
    model.read_vehicles('Data/3_detail_table_vehicles.csv', w = 0)
    sol_init = list(model.agents['vehicles_dupl'].values())
    sol_base = model.assign_clients_to_vehicles(l,list(model.agents['vehicles'].values()))
    
    learner = Q_Learning.Q_agent(model,sol_base,sol_init,max_iter_no_improvement,max_nb_states,epsilon,decay_rate,learn_rate,disc_rate)
    solu_f,liste_couts,liste_couts_par_algo,Q = learner.Q_learning(nb_ite,nb_algs)
    
    simultaneous = []
    for i in range(nb_algs):
        liste = []
        for j in liste_couts_par_algo:
            liste.append(j[i])
        simultaneous.append(liste)
    print("Finished")
    fig = plt.figure()
    plt.plot(liste_couts)
    plt.title("Courbe de résultats de l'algorithme ")
    plt.xlabel("Nombre d'itérations")
    plt.ylabel('Coût trouvé')
    Streamlit.plot(fig)
    
    fig = plt.figure()
    for i in range(nb_algs):
        print(simultaneous[i])
        plt.plot(simultaneous[i])
    plt.title("Courbe de résultats par algorithme ")
    plt.xlabel("Nombre d'itérations")
    plt.ylabel('Coût trouvé')
    Streamlit.plot(fig)
    plt.show()
    
    # Streamlit.top()
    Streamlit.network(model)