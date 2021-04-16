"""
Created on Fri April 9 2021
@author: Raul Ortega
"""
import pygame
import numpy as np
import random
import argparse
import copy
from time import sleep
import matplotlib.pyplot as plt
from numba import jit

# RGB colors of cells
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (211,211,211)

# Dimension of the cells
height = 3
width = height
margin = 0

@jit(nopython=True)
def rules(state, alive):
        """
        1. Any live cell with two or three live neighbours survives.
        2. Any dead cell with three live neighbours becomes a live cell.
        3. All other live cells die in the next generation. Similarly, all other dead cells stay dead.
        """
        if state == 1: # cell was alive
            if alive - 1 in [2,3]:
                return 1 # lives
            else:
                return 0 # dies
        else: # cell was dead
            if alive in [3]:
                return 1 # revives
            else:
                return 0 # stays dead

@jit(nopython=True)
def update_world_(world_size, world, temp):
     # updates the world according to rules

        m, n = world_size, world_size
        for row in range(1, m-1): # edges are buffer zones
            for column in range(1, n-1): # edges are buffer zones
                
                alive = 0 # alive neighbors counter
                # loop over its 8 neighbours
                for i in [row-1, row, row+1]:
                    for j in [column-1, column, column+1]:
                          
                         # if alive and not itself count as alive
                        if (world[i,j] == 1): # and ([i, j] != [row, column]):
                            alive = alive + 1
                                
                        # rules function decides whether it lives or dies
                temp[row,column] = rules(world[row,column], alive)
        return temp

class World:
    def __init__(self, grid_dim):
        self.__create_world(grid_dim)
        self.world_size = (grid_dim)
        self.alive = np.sum(np.sum(self.world))

    def __create_world(self, grid_dim):
        # initialize world full of dead cells
        self.world = np.zeros((grid_dim, grid_dim))

    def rules(self, state, alive):
        """
        1. Any live cell with two or three live neighbours survives.
        2. Any dead cell with three live neighbours becomes a live cell.
        3. All other live cells die in the next generation. Similarly, all other dead cells stay dead.
        """
        if state == 1: # cell was alive
            if alive - 1 in [2,3]:
                return 1 # lives
            else:
                return 0 # dies
        else: # cell was dead
            if alive in [3]:
                return 1 # revives
            else:
                return 0 # stays dead

    def update_world(self):
        temp = copy.deepcopy(self.world)
        temp = update_world_(self.world_size, self.world, temp)
       
        self.world = temp
        self.alive = np.sum(np.sum(self.world))

    def spawn(self, frac=0.01):
        """
        Revive a fraction frac of the total number of cells at random postions
        """
        num_cells = (self.world_size**2 - self.alive) * frac
        spawned = 0
        while spawned < num_cells:
            row = random.randint(1,self.world_size-1)
            col = random.randint(1,self.world_size-1)
            self.world[row,col] = 1
            spawned +=1
        self.alive = np.sum(np.sum(self.world))
    

def draw(world):
    # draw the grid of the world
    for row in range(world.world_size):
        for column in range(world.world_size):
            color = BLACK
            if world.world[row,column] == 1:
                color = WHITE
            pygame.draw.rect(screen, color, [(margin + width) * column + margin, 
                            (margin + height) * row + margin, width, height])
    
    clock.tick(60) # 60 frames per second
    pygame.display.flip() # update screen

def plot_statistics(num_iteration, num_alive, num_perc_alive):
    # plot 1
    plt.plot(num_iteration, num_perc_alive)
    plt.xlabel("Iterations")
    plt.ylabel(" (%) alive cells")
    plt.title("Percentage of alive cells vs number of iterations")
    plt.savefig("files/percentage_cells_iterations.png")
    plt.show()

    # plot 2
    plt.plot(num_iteration, num_alive)
    plt.xlabel("Iterations")
    plt.ylabel("Alive cells")
    plt.title("Alive cells vs number of iterations")
    plt.savefig("files/cells_iterations.png")
    plt.show()
    


if __name__ == "__main__":
    # parsing user input
    # example: python generations.py --size=50 --spawn_freq=10
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", dest="size", help="World size (e.g 100)", default=200, type=int)
    parser.add_argument("--spawn_freq", dest="spawn_freq", help="Spawn freq (e.g 100)", default=10, type=int)
    args = parser.parse_args()

    # create world
    world = World(grid_dim=args.size)

    # arrays to store stats of simulation
    num_iteration, num_alive, num_perc_alive = [], [], []

    # init pygame, window set up
    pygame.init()
    clock = pygame.time.Clock() # to manage how fast the screen updates
    screen = pygame.display.set_mode([600, 600])
    pygame.display.set_caption("Cellular automata")
    screen.fill(GRAY) # fill background in black
    draw(world)

    # main loop
    done, run = False, False
    iterations = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
            elif (event.type == pygame.KEYDOWN) and (event.key==pygame.K_RETURN):
                    run = True
            
        if run:
            world.update_world()

            if (iterations % args.spawn_freq == 0):
                world.spawn(frac=0.01)

            draw(world)

            num_iteration.append(iterations)
            num_alive.append(world.alive)
            num_perc_alive.append(world.alive*100/(world.world_size**2))


        iterations += 1

    print("User terminated world.")
    pygame.quit() # so that it doesnt "hang" on exit

    plot_statistics(num_iteration, num_alive, num_perc_alive)
    exit(0)