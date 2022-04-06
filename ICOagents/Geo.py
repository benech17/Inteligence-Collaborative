from math import sin, cos, sqrt, atan2, radians, exp
import mesa

class Agent(mesa.Agent):
    '''Geoagent is an abstract object that has map information'''
    def __init__(self, model, code, lat, lon):
        super().__init__(model.next_id(), model)
        self.id = model.current_id
        self.code = code
        self.lat = lat
        self.lon = lon
    def distance(self, other):
        '''Calculates distance between object and other point'''
        # K is the radius of the earth
        k = 6373.0 
        d_long = radians(other.lon) - radians(self.lon)
        d_lat = radians(other.lat) - radians(self.lat)
        x = sin(d_lat / 2)**2 + cos(radians(other.lat)) * cos(radians(self.lat)) * sin(d_long / 2)**2
        z = 2 * atan2(sqrt(x), sqrt(1 - x))
        return(k*z)
