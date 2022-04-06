from ICOagents import Geo

class Agent(Geo.Agent):
    '''Client Agent'''
    def __init__(self, model, series):
        super().__init__(model, series['CUSTOMER_CODE'], series['CUSTOMER_LATITUDE'], series['CUSTOMER_LONGITUDE'])
        self.number_of_articles = series['NUMBER_OF_ARTICLES']
        self.total_weight_kg = series['TOTAL_WEIGHT_KG']
        self.total_volume_m3 = series['TOTAL_VOLUME_M3']
    def step():
        pass