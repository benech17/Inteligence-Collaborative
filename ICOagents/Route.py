import mesa

from ICOagents import Client, Deposit, Vehicle

class Agent(mesa.Agent):
    '''Agent that represents a route'''
    def __init__(self, model, code):
        super().__init__(model.next_id(), model)
        self.code = code
        self.agents = {"deposits": {},"vehicles": {}, "clients": {}, "routes":{}}
        self.vehicles = {}
    def add_agent(self,agent):
        if type(agent) is Vehicle.Agent:
            self.vehicles[agent.code] = agent
        else:
            print("Nah")