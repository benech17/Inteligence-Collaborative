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
        super().__init__(model.next_id(), model)
        self.eps =
        self.state = 
        self.actions = [eps_greedy(self.state),intra_route_swap(self),inter_route_swap(self,vhl2),intra_route_shift(self),inter_route_shift(self,vhl2),two_intra_route_swap(self),two_intra_route_shift(self),remove_road(self,"smallest",liste_vehicules),remove_road(self,"random",liste_vehicules)]
        self.next_state = 0
        self.lr_rate =0
        self.r = 0
        self.dis_rate =0
        
        
    def eps_greedy(self):
        if random.uniform(0, 1) < eps:
            action = randint(1, 9)
        else: # Or greedy action
            action = np.argmax(Q[st])
        return action
        
    
    def choose_action(self,type_function,Q_size):
        
        if type_function ==1:
            self.next_state = 0
        else:
            if type_function ==2:
                
                self.next_state = randint(1,8)
            
    def Q_learning(self):
        Q = np.ones((8,8),float)
        
        for k in range(0,10):
            self.state = 
            
        
    def step(self):
        
        
        
        
        
        
        
        
        
        
    def intra_route_swap(self):
        a = randint(0,len(self.clients))
        b = randint(0,len(self.clients))
        c = self.clients[a]
        d = self.clients[b]
        self.clients[a] = d
        self.clients[b] = c
        
    def inter_route_swap(self,vhl2):
        
        a = randint(0,len(self.clients))
        b = randint(0,len(vhl2.clients))
        c = self.clients[a]
        d = vhl2.clients[b]
        # voir si c'est compatible
        if (vhl2.vehicle_weight + c.total_weight_kg - d.total_weight_kg > vhl2.vehicle_total_weight) or (self.vehicle_weight + d.total_weight_kg - c.total_weight_kg > self.vehicle_total_weight) or (vhl2.vehicle_volume + c.total_volume_m3 - d.total_volume_m3 > vhl2.vehicle_total_volume) or (self.vehicle_volume - c.total_volume_m3 + d.total_volume_m3 > self.vehicle_total_volume) or (d in self.clients) or (c in vhl2.clients):
            break
        else:
            self.clients[a] = d
            vhl2.clients[b] = c
        
    
    
    def intra_route_shift(self):
        
        a = randint(0,len(self.clients))
        b = randint(0,len(self.clients))
        c = self.clients[a]
        d = self.clients[b]
        L = self.clients
        
        if a ==b:
            while (a==b):
                b = randint(0,len(self.clients))
        self.clients[b] = c
        if b > a:
            for k in range(b-1,a-1,-1):
                self.clients[k] = L[k+1]
        else: 
            for k in range(b+1,a+1):
                self.clients[k] = L[k-1]
            
        
        
    def inter_route_shift(self,vhl2):
        
        b = self.clients[-1]
        
        if (vhl2.vehicle_weight + b.total_weight_kg > vhl2.vehicle_total_weight) or (vhl2.vehicle_volume + b.total_volume_m3 > vhl2.vehicle_total_volume) or (b in vhl2.clients):
            break
        else:
            vhl2.clients.append(b)
            self.clients.pop([-1])
        
    
    def two_intra_route_swap(self):
        a = randint(0,len(self.clients)-1)
        b = randint(0,len(self.clients)-1)
        
        c1,c2 = self.clients[a],self.clients[a+1]
        d1,d2 = self.clients[b],self.clients[b+1]
        
        self.clients[a],self.clients[a+1] = d1,d2
        self.clients[b],self.clients[b+1] = c1,c2
        
    def two_intra_route_shift(self):
        
        
        a = randint(0,len(self.clients)-1)
        b = randint(0,len(self.clients)-1)
        c1,c2 = self.clients[a],self.clients[a+1]
        d1,d2 = self.clients[b],self.clients[b+1]
        L = self.clients
        
        if a == b:
            while (a==b):
                b = randint(0,len(self.clients))
                
        self.clients[b],self.clients[b+1] = c1,c2
        
        if b > a:
            for k in range(b-1,a,-1):
                self.clients[k-1],self.clients[k] = L[k+1],L[k+2]
                
        else: 
            for k in range(b,a-1):
                self.clients[k+2],self.clients[k+3] = L[k],L[k+1]
        
        
        
        
    def remove_road(self,typea,liste_vehicules):

        






































