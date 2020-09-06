# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 16:49:41 2020

@author: Raul Ortega
"""

def load_pattern(grid):
    
    # pattern given by the coordinates of the black grids
    pattern = [[15, 15], [15, 14], [15, 16], [16, 15]]
    
    # initialize the grid array full of zeros, when at position of 
    # pattern turn grid sqaure black, set 1
    for pattern_dot in pattern:
        # initialize the grid array full of zeros
        grid[pattern_dot[0]][pattern_dot[1]] = 1
    return grid

# ===========================
# function that given the grid computes the number of neighbors alive for each
# node of the grid
def alive_neighbors(grid):
    m = len(grid)
    n = len(grid[0])
    temp = grid
    
    for row in range(1, m-1): # exclude edges for now
            for column in range(1, n-1): # exclude edges for now
                alive = 0 # alive neighbors counter
                
                # loop over its 8 neighbours
                for i in [row-1, row, row+1]:
                    for j in [column-1, column, column+1]:
                        
                        # if alive and not itself count as alive
                        if (grid[i][j] == 1) and ([i, j] != [row, column]):
                            alive = alive+1
                            
                        # rules function decides whether it lives or dies
                temp[row][column] = rules(grid[row][column], alive)
    return temp
# ============================
# function that given a number of alive neighbors decides weather the cell
# lives or dies
def rules(state, alive):
    if state == 1: # cell was alive
        if alive in [2, 3]:
            return 1 # lives
        else:
            return 0 # dies
    else: # cell was dead
        if alive in [3]:
            return 1 # lives
        else:
            return 0 # dies
                        
                        
                
            
    