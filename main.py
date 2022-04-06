from ICOinterface import Streamlit
from ICOmodel import Global

if __name__ == "__main__":
    '''Main function of the program'''
    # Creates the model and read files
    model = Global.Model(verbose = True)
    # Model reads files and create agents
    model.read_clients('Data/2_detail_table_customers.csv')
    model.read_vehicles('Data/3_detail_table_vehicles.csv', w = 0)
    model.read_deposits('Data/4_detail_table_depots.csv')
    # Here's some code to verify object mutability in the route and global

    # for v in model.agents['vehicles']:
    #     model.agents['vehicles'][v].verify0()
    # print("--------")
    # for r in model.agents['routes']:
    #     print("-", r)
    #     for v in model.agents['routes'][r].vehicles:
    #         model.agents['routes'][r].vehicles[v].verify1()
    # print("--------")
    # for v in model.agents['vehicles']:
    #     model.agents['vehicles'][v].verify0()
    # print("-------")
    # for v in model.agents['routes'][2946091].vehicles:
    #     model.agents['routes'][2946091].vehicles[v].verify1()
    # print("-------")
    # for v in model.agents['vehicles']:
    #     model.agents['vehicles'][v].verify0()

    # Now create routes
    # model.create_routes()
    # Model now relates the agents

    model.step() 