#### direction mechanism
class node():
    def __init__(self, val):
        self.val = val
        self.L = None
        self.R = None

#### initialize the two ways linked list 
left = node(lambda x,y: (x-1, y))
up = node(lambda x,y: (x, y+1))
right = node(lambda x,y: (x+1, y))
down = node(lambda x,y: (x, y-1))

#### setting the relative directions
left.L, up.L, right.L, down.L = down, left, up, right
left.R, up.R, right.R, down.R = up, right, down, left  



#### define snake object
class snake():
    def __init__(self):
        self.body = [(i,0) for i in range(30)]
        self.direction = left  ## two_ways linked list 
        self.dead = False ## vital status
        self.completed = False ## game completeness status
        
    def move(self):
        del self.body[-1]
        newhead = self.direction.val(*self.body[0])
        if newhead in self.body:
            self.dead = True
        elif self.__reach_edge(newhead):
            sefl.complete = True
        self.body.insert(0, newhead)
    def __reach_edge(self, point):
        return any(axis<=-500 or axis>=500 for axis in point)
      
    def change_dir(self, clockwise=False): ### default: turn left
        if clockwise:
            self.direction = self.direction.R
        else:
            self.direction = self.direction.L  



#### import modules
import pandas as pd
import numpy as np
from math import ceil
from random import *
import os

#### specify directory
cwd = os.getcwd()  


#### if record=True, save the footage file to wd
def simulate_once(record=False):
    my_snake = snake()
    if record:
        footage = pd.DataFrame(my_snake.body)
        file = os.path.join(cwd,'snake_footage.csv')
    while True:
        ###Turn every 5 seconds in average
        seconds = ceil(expovariate(0.2))
        
        ##before every turn, move forward in current direction
        for i in range(seconds):
            my_snake.move()
            if record:
                footage = pd.concat([footage, pd.DataFrame(my_snake.body)], axis=1)
            if my_snake.dead:
                if record:
                    footage.to_csv(file, header=None, index=False)
                return 0
            elif my_snake.completed:
                if record:
                    footage.to_csv(file, header=None, index=False)
                return 1
              
        ### change direction
        turn = choice(['left', 'right'])
        if turn == 'left':
            my_snake.change_dir(clockwise=False)
        else:
            my_snake.change_dir(clockwise=True)  




#### Visualization ####################
from matplotlib import pyplot as plt
from matplotlib import animation

#### record snake footage to wd
simulate_once(record=True)

#### load the footage file
file = os.path.join(cwd,'snake_footage.csv')
dot_data = pd.read_csv(file, header=None)

#### pyplot animation setting
fig, ax = plt.subplots()
curr_x, curr_y = 0, 1
steps = dot_data.shape[1]
def animate(i):
    global curr_x, curr_y
    try:
        x = np.array(dot_data[curr_x])
        y = np.array(dot_data[curr_y])
    except:
        curr_x, curr_y = 0, 1
    else:
        head = [x[0],y[0]]
        ax.clear()
        plt.plot(x,y, c='DarkBlue', marker='.')
        plt.plot(head[0],head[1], c='DarkRed', marker='.')
        plt.xlim(head[0]-35, head[0]+35)
        plt.ylim(head[1]-35, head[1]+35)
        curr_x += 2
        curr_y += 2

#### execute animation
ani = animation.FuncAnimation(fig, animate, interval=500, blit=False)
plt.show()
#### Visualization end ###############


#### simulate many
def simulate_many(times):
    total = positive = 0
    for i in range(times):
        positive += simulate_once()
    return positive/times

#### execute simulate_many, return the probability of success
print(simulate_many(100000))
