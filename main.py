# from ICOinterface import Streamlit
from ICOmodel import Global
import random

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
    
    nb_ite = 50
    nb_permut = 1
    route_num = 0
    nb_algs = 3
    l = model.agents['routes'][route_num]
    cout = 0
    permutations_f = []
    couts_f = []
    for i in range(nb_permut):
        sol = []
        a = l.copy()
        random.shuffle(a)
        model.agents['vehicles'].clear()
        model.read_vehicles('Data/3_detail_table_vehicles.csv', w = 0)
        model.assign_clients_to_vehicles(a)
        model.assign_heuristics_to_vehicles()
        
        for i in range(nb_ite):
            model.step()
        
        #test algo QLearning
        list_vehicles = []
        for v in model.agents['vehicles'].values():
            list_vehicles.append(v)
        
        for h in list_vehicles: 
            b = []
            for k in h.clients:
                b.append(k.code) 
            sol.append(b)
        print(sol)
            
        list_vehicles[2].intra_route_swap()
        list_vehicles[1].inter_route_swap(list_vehicles[3])
        list_vehicles[0].intra_route_shift()
        list_vehicles[3].inter_route_shift(list_vehicles[4])
        list_vehicles[5].two_intra_route_swap()
        list_vehicles[6].two_intra_route_shift()
        
        
        sol = []
        for h in list_vehicles: 
            b = []
            for k in h.clients:
                b.append(k.code) 
            sol.append(b)
        
        print(sol)
        
        sol = []
        # Parte cout
        total = [0]*nb_algs
        for v in model.agents['vehicles'].values():
            if len(v.algorithm) != 0:
                for i in range(nb_algs):
                    # plt.plot(v.algorithm[i].mins)
                    # plt.title("Courbe de résultats de l'algorithme " + type(v.algorithm[i]).__name__)
                    # plt.xlabel("Nombre d'itérations")
                    # plt.ylabel('Coût trouvé')
                    # plt.show()
                    if len(v.algorithm[i].mins) == 0 :
                        total[i] += 0
                    else :
                        total[i] += v.algorithm[i].mins[-1]
        cout = total
        for v in model.agents['vehicles'].values():
            b = []
            for k in v.algorithm:
                for h in k.prev_solus[-1]:
                    b.append(h.code) 
            sol.append(b)
        permutations_f.append(sol) #permet de récupérer la meilleure solution associée à chaque route
        couts_f.append(cout)
    simultaneous = []
    for i in range(nb_algs):
        liste = []
        for j in range(nb_permut):
            liste.append(couts_f[j][i])
        simultaneous.append(liste)
    #Streamlit.plot_solutions(simultaneous)
