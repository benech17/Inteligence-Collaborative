from ICOinterface import Streamlit
from ICOmodel import Global

if __name__ == "__main__":
    '''Main function of the program'''
    # Creates the model and read files
    model = Global.Model(verbose = True)
    # Model reads files and create agents
    deps = model.read_deposits('Data/4_detail_table_depots.csv')
    clis = model.read_clients('Data/2_detail_table_customers.csv')
    model.assign_clusters_to_vehicles()

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
    Streamlit.map(model)
    
    plots = model.find_best_sol(0,50,10,3)
    Streamlit.plot_solutions(plots)