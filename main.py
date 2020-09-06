
"""
Created on Sun Sep  6 15:19:49 2020

@author: Raul Ortega
"""
import pygame

# define the two colors of the grid RGB
black = (0, 0, 0)
white = (255, 255, 255)

# set the height/width of each location on the grid
height = 20
width = height # i want the grid square
margin = 2 # sets margin between grid locations


# initialize the grid array full of zeros
grid = []
num_rows = 20
num_columns = num_rows # i want it squared
for row in range(num_rows):
    grid.append([])
    for column in range(num_columns):
        grid[row].append(0)

# initialize pygame
pygame.init()

# congiguration of the window
WINDOW_SIZE = [1000, 1000]
screen = pygame.display.set_mode(WINDOW_SIZE)
# screen title
pygame.display.set_caption("Cellular automata")
 

# loop until done
done = False

clock = pygame.time.Clock() # to manage how fast the screen updates

# main program
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change to grid coordinates
            column = pos[0] // (width + margin)
            row = pos[1] // (height + margin)
            # Set that location to one
            if grid[row][column] == 1:
                grid[row][column] = 0
            else:
                grid[row][column] = 1
            
    
    screen.fill(black) # fill background in black
    
    for row in range(num_rows):
        for column in range(num_columns):
            color = white
            if grid[row][column] == 1:
                color = black
            else:
                color = white
            pygame.draw.rect(screen,
                             color,
                             [(margin + width) * column + margin,
                              (margin + height) * row + margin,
                              width,
                              height])
    
    # set limit to 60 frames per second
    clock.tick(60)
    
    # update screen
    pygame.display.flip()
    
pygame.quit() # so that it doesnt "hang" on exit
