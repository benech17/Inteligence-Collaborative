
import mesa
import mesa.time

import genetic
import graph
import rs
import taboo
import util
import viz

class GlobalModel(mesa.Model):
    def __init__(self, N):
        # RandomActivation va randomizer la ordre des step de chaque agent
        self.schedule = mesa.time.RandomActivation(self)
        # Initializer N agents, n'oublier pas d'envoyer le model
        for i in range(N):
            self.schedule.add(taboo.TabooAgent(i,self))
    def step(self):
        self.schedule.step()
        print("------")


def main():
    model = GlobalModel(3)
    model.step() 
    depot = util.read_files()
    viz.map(depot,[])
    
    # Completer

if __name__ == "__main__":
    main()