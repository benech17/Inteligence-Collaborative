from ICOinterface import Streamlit
from ICOmodel import Global

if __name__ == "__main__":
    '''Main function of the program'''
    # Creates the model and read files
    model = Global.Model(verbose = True)
    # Model reads files and create agents
    model.read_deposits('Data/4_detail_table_depots.csv')
    model.read_clients('Data/2_detail_table_customers.csv')
    model.planning = False
    nb_ite = 50
    nb_permut = 10
    model.find_best_sol(0,nb_permut,nb_ite)
    print("Finished!")