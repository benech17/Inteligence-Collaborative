from ICOagents import Geo, Client, Vehicle
import mesa

class Agent(Geo.Agent):
    '''Deposit Agent'''
    def __init__(self, model, series):
        super().__init__(model, series['DEPOT_CODE'],series['DEPOT_LATITUDE'],series['DEPOT_LONGITUDE'])