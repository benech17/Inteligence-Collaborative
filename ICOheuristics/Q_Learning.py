import mesa
import numpy as np
from random import randint
import random

class EnvGrid(object):
 
    def __init__(self):
        super(EnvGrid, self).__init__()

        self.grid = [
            [0, 0, 1],
            [0, -1, 0],
            [0, 0, 0]
        ]
        # Starting position
        self.y = 2
        self.x = 0

        self.actions = [
            [-1, 0], # Up
            [1, 0], #Down
            [0, -1], # Left
            [0, 1] # Right
        ]

    def reset(self):
        """
            Reset world
        """
        self.y = 2
        self.x = 0
        return (self.y*3+self.x+1)

    def step(self, action):
        """
            Action: 0, 1, 2, 3
        """
        self.y = max(0, min(self.y + self.actions[action][0],2))
        self.x = max(0, min(self.x + self.actions[action][1],2))

        return (self.y*3+self.x+1) , self.grid[self.y][self.x]

    def show(self):
        """
            Show the grid
        """
        print("---------------------")
        y = 0
        for line in self.grid:
            x = 0
            for pt in line:
                print("%s\t" % (pt if y != self.y or x != self.x else "X"), end="")
                x += 1
            y += 1
            print("")

    def is_finished(self):
        return self.grid[self.y][self.x] == 1

def take_action(st, Q, eps):
    # Take an action
    if random.uniform(0, 1) < eps:
        action = randint(0, 3)
    else: # Or greedy action
        action = np.argmax(Q[st])
    return action

if __name__ == '__main__':
    env = EnvGrid()
    st = env.reset()

    Q = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    for _ in range(100):
        # Reset the game
        st = env.reset()
        while not env.is_finished():
            #env.show()
            #at = int(input("$>"))
            at = take_action(st, Q, 0.4)

            stp1, r = env.step(at)
            #print("s", stp1)
            #print("r", r)

            # Update Q function
            atp1 = take_action(stp1, Q, 0.0)
            Q[st][at] = Q[st][at] + 0.1*(r + 0.9*Q[stp1][atp1] - Q[st][at])

            st = stp1

    for s in range(1, 10):
        print(s, Q[s])



class Q_agent(mesa.Agent):
    def __init__(self, model, vhl, client):
        super().__init__(model.next_id(), model,vhl)
        self.eps =
        self.state = 
        self.actions = vhl.liste_fonctions
        self.next_state = vhl.clients
        self.lr_rate =0
        self.r = 0
        self.dis_rate =0
        self.liste_vehicules = vhl.liste_vehicules
        self.liste_fonctions =
        self.grid = np.zeros((8,8),float)
        
        
        
    def eps_greedy(self):
        if random.uniform(0, 1) < eps:
            action = self.liste_fonctions[randint(0, 7)]
        else: # Or greedy action
            action = np.argmax(Q[st])
        return action
        
        
    
    def choose_action(self,type_function):
        
        if type_function ==1: # fcts avec 1 arguments
            self.next_state = self.liste_fonctions[eps_greedy(self.liste_vehicules)](self.liste_vehicules)
        else:
            if type_function ==2: # fcts avec 2 arguments
                
                self.next_state =self.liste_fonctions[eps_greedy(self.liste_vehicules)](self.liste_vehicules,vhl)
            
            
            
    def Q_learning(self):
        Q = np.ones((8,8),float) * 1
        
        for k in range(0,10):
            self.state = k
            for j in range(0,10):
                action = eps_greedy(self.liste_vehicules)
                if action in #[numéro de fcts ac un argument]
                    self.liste_fonctions[action](self.liste_vehicules)
                else: self.liste_fonctions[action](self.liste_vehicules,vhl)
                
                Q[st,at] = #  moyenne coûts - côuts
                r = self.grid[k][action]
                self.next_state =
                Q[st,at] += self.lr_rate*(r+self.dis_rate*Q[stp1][atp1] - Q[st][at])
                self.state = self.next_state
                
    def reset(self):
        self.grid = np.zeros((8,8),float)
    
        return (self.grid)
    
    
    def is_finished(self):
    
        return self.grid[,] ==
    
    
    def reward(self):
        
            
        
    def step(self, action):
    
        return(
        
        
        
        
        
        
        
        
        


        






































