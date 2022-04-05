from ICOagents import Geo

class Agent(Geo.Agent):
    '''Client Agent'''
    
    def __init__(self, model, series):
        super().__init__(model, series['CUSTOMER_CODE'], series['CUSTOMER_LATITUDE'], series['CUSTOMER_LONGITUDE'])
        self.deposit_to_client_in_km = dtc_km
        self.deposit_to_client_in_time = dtc_time
        self.client_to_deposit_in_km = ctd_km
        self.client_to_deposit_in_time = ctd_time
        self.number_of_articles = series['NUMBER_OF_ARTICLES']
        self.total_weight_kg = series['TOTAL_WEIGHT_KG']
        self.total_volume_m3 = series['TOTAL_VOLUME_M3']
    def step():
        pass