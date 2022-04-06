from ICOinterface import Streamlit
from ICOmodel import Global

if __name__ == "__main__":
    '''Main function of the program'''
    # Creates the model and read files
    model = Global.Model(verbose = True)
    # Model reads files and create agents
    model.read_deposits('Data/4_detail_table_depots.csv')
    model.read_vehicles('Data/3_detail_table_vehicles.csv', w = 0)
    model.read_clients('Data/2_detail_table_customers.csv')
    # Assign clients to vehicles
    model.assign_clients_to_vehicles()
    model.assign_heuristics_to_vehicles()
    model.step() 
    model.planning = False
    model.step() 