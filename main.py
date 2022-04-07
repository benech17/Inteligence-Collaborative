from ICOinterface import Streamlit
from ICOmodel import Global
# from ICOinterface import Streamlit

if __name__ == "__main__":
    '''Main function of the program'''
    # Creates the model and read files
    model = Global.Model(verbose = True)
    # Model reads files and create agents
    model.read_deposits('Data/4_detail_table_depots.csv')
    model.read_vehicles('Data/3_detail_table_vehicles.csv', w = 0)
    model.read_clients('Data/2_detail_table_customers.csv')
    # Assign clients to vehicles
    # model.assign_clients_to_vehicles()
    # model.assign_heuristics_to_vehicles()
    # model.step() 
    # model.planning = False
    # nb_ite = 100
    # for i in range(nb_ite):
    #     model.step() 
    # model.plot_graphs(nb_ite)
    print("Finished!")

# Notes du Q-Learning
# processus de markov:
# a parte em vermelha no slide indica que tu não precisa (e nem deveria) precisar guardar o passado. Todas as informações úteis para a tomada de decisão devem ser vistas pelo estado presente).
# Programar 8 algos de voisinage (slide 44 acho)
# slide 35 (wtf? está fora de ordem) comparar as curvas
# bonus: aplicar o qlearning nos três algoritmos (slide 57)
# bonus: explicar para qual problema podemos utilizar x algoritmo ou y algoritmo
# usar reseaux de neurone (perceptron com uma de entrada, uma saida e duas intermediárias (30 neuronios dentro?)) para fazer um deep reinforcment learning..