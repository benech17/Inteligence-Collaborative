import mesa
import mesa.time

import genetic
import graph
import rs
import taboo
import util
import viz

class GlobalMASModel(mesa.Model):
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
    model = GlobalMASModel(3)
    model.step() 
    rows_table_customers, rows_table_vehicles, rows_table_depots, rows_table_cust_depots_distances, liste_routes, route = util.read_files()
    # Completer

if __name__ == "__main__":
    main()