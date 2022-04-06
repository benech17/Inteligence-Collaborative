from ICOinterface import Streamlit
from ICOmodel import Global

if __name__ == "__main__":
    '''Main function of the program'''
    # Creates the model and read files
    model = Global.Model(verbose = True)
    # Model reads files and create agents
    # model.read_clients('Data/2_detail_table_customers.csv')
    model.read_vehicles('Data/3_detail_table_vehicles.csv')
    # model.verify_v()
    print(len(model.vehicles))
    for v in model.vehicles:
        model.vehicles[v].verify0()
    print("--------")
    for r in model.agents['routes']:
        print("-")
        for v in model.agents['routes'][r].vehicles:
            model.agents['routes'][r].vehicles[v].verify1()
    print("--------")
    for v in model.vehicles:
        model.vehicles[v].verify0()
    # model.read_deposits('Data/4_detail_table_depots.csv')
    # Now create routes
    # model.create_routes()
    # Model now relates the agents

    model.step() 