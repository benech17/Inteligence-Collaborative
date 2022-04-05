from ICOinterface import Streamlit
from ICOmodel import Global

if __name__ == "__main__":
    '''Main function of the program'''
    # Creates the model and read files
    model = Global.Model(verbose = True, interface = None)
    # Model reads files
    model.read_clients()
    model.read_cost_distances()
    model.read_deposits()
    model.read_vehicles()
    # Model now creates agents
    model.create_deposits()
    model.create_vehicles()

    model.step() 