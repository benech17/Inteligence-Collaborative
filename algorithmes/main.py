import mesa
import mesa.time

from ICOinterface import Streamlit
from ICOheuristics import Taboo, Genetic, RS
from ICOdata import Split, Read

class GlobalModel(mesa.Model):
    def __init__(self):
        super().__init__()
        self.planning = True
        # A list with all the planning agents
        self.planners = []
        # self.schedule = mesa.time.RandomActivation(self)
        # self.planning = False
        # for i in range(N):
        #     self.schedule.add(Taboo.Agent(i,self))
    def create_planner_agent(self,agent):
        '''Creates planning agents in list and returns them'''
        newAgent = agent(self)
        self.planners.append(newAgent)
        return newAgent

    def step(self):
        if self.planning:
            print("Planning!")
        else:
            print("Delivering!")

def main():
    '''Main function of the program'''
    # Creates the model and read files
    model = GlobalModel()
    reader = model.create_planner_agent(Read.Agent)
    reader.read_clients()
    reader.read_cost_distances()
    reader.read_deposits()
    reader.read_vehicles()
    
    print(reader)

    # Starts by reading the different files. You can also send the path inside the functions to get other data. ICOData Read file.
    # Creates the 
    model.step() 

if __name__ == "__main__":
    main()