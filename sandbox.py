"""
Created on Fri April 16 2021
@author: Raul Ortega
"""
import pygame
import numpy as np
import random
import argparse
import copy
from time import sleep

# RGB colors of cells
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (211,211,211)

# Dimension of the cells
height = 10
width = height
margin = 1

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
        # updates the world according to rules

        m, n = self.world_size, self.world_size
        temp = copy.deepcopy(self.world)
        for row in range(1, m-1): # edges are buffer zones
            for column in range(1, n-1): # edges are buffer zones
                
                alive = 0 # alive neighbors counter
                # loop over its 8 neighbours
                for i in [row-1, row, row+1]:
                    for j in [column-1, column, column+1]:
                          
                         # if alive and not itself count as alive
                        if (self.world[i,j] == 1): # and ([i, j] != [row, column]):
                            alive = alive + 1
                                
                        # rules function decides whether it lives or dies
                temp[row,column] = self.rules(self.world[row,column], alive)
        self.world = temp
        self.alive = np.sum(np.sum(self.world))

    def is_alive(self):
        if self.alive != 0:
            return True
        else:
            return False
    

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


if __name__ == "__main__":
    # parsing user input
    # example: python generations.py --size=50
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", dest="size", help="World size (e.g 100)", default=54, type=int)
    args = parser.parse_args()

    # create world
    world = World(grid_dim=args.size)

    # init pygame, window set up
    pygame.init()
    clock = pygame.time.Clock() # to manage how fast the screen updates
    screen = pygame.display.set_mode([600, 600])
    pygame.display.set_caption("Cellular automata Sandbox")
    screen.fill(GRAY) # fill background in gray
    draw(world)

    # main loop
    done, run = False, False
    iterations = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                print("User terminated world.")
            
            # Only if not running allow to draw pattern
            elif (event.type == pygame.MOUSEBUTTONDOWN) and (run == False):

                # get mouse click position
                pos = pygame.mouse.get_pos()
                column = pos[0] // (width + margin)
                row = pos[1] // (height + margin)

                # Change state of clicked cell
                if world.world[row, column] == 1:
                    world.world[row, column] = 0
                else:
                    world.world[row, column] = 1

                draw(world)

            elif (event.type == pygame.KEYDOWN) and (event.key==pygame.K_RETURN):
                    run = True

        if run:
            sleep(0.05)

            world.update_world()
            draw(world)

            if not world.is_alive():
                done = True
                print("No cells left alive. App will close in 5 sec.")
                sleep(5)
            
    pygame.quit() # so that it doesnt "hang" on exit
    exit(0)