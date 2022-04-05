import mesa

class RSAgent(mesa.Agent):
    def __init__(self,id, model):
        super().__init__(id, model)
        self.id = id
        self.s = 0
    def step(self):
        print("C'est le step",self.s,"du agent",self.id)
        self.s+=1