# Cellular Automata (Conway's Game of Life)

## About
Python implementation of a simple 2-dimensional cellular automata with the original rules of Conway's Game of life. The world is a grid where cells can be black (alive) or white (dead). The user can select by clicking on the cells which cells to initialize as alive and then to start the execution presses return/enter key.

 The following rules specified the transitions:
```
-- Any live cell with fewer than two live neighbours dies, as if by underpopulation.
-- Any live cell with two or three live neighbours lives on to the next generation.
-- Any live cell with more than three live neighbours dies, as if by overpopulation.
-- Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
```
These rules, which compare the behavior of the automaton to real life, can be condensed into the following:
```
1.- Any live cell with two or three live neighbours survives.
2.- Any dead cell with three live neighbours becomes a live cell.
3.- All other live cells die in the next generation. Similarly, all other dead cells stay dead.
```
more info: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

## Requirements
* Pygame
* Numpy

## Usage
* Install requirements `pip install -r requirements.txt`
* Run main program `python main.py`
* Select cells to initialize as alive, when finished then press `enter/return key`
* To stop the execution of the program press `esc key`

## Examples
<figure>
  <img src = "files/gun_automata.gif" height="250"/>
  <figcaption>Fig. 1: Gun automata <figcaption/>
<figure/>

<figure>
  <img src = "files/spaceships_automata.gif" height="250"/>
  <figcaption>Fig. 2: Spaceships and other patterns <figcaption/>
<figure/>

## Structure
* main.py: contains main loop of updating the visualization with Pygame
* heloers.py: contains main logical function for execution of program (e.g Rules of the automata)

