import time
import curses
import random

changing = True

map = [
        [0,0,0,0,0,0,0,0,0,0], 
        [0,0,0,0,0,0,0,0,0,0], 
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,1,0,1,0,0,0,0,0], 
        [0,0,0,0,1,0,0,0,0,0], 
        [0,0,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0]]

randomMap = str(input("Should the map be random? [Y/N] "))

if randomMap == "Y" or randomMap == "y":

    for row in range(len(map)):
        for col in range(len(map[row])):
            map[row][col] = random.randint(0,1)

map2 = [
    [0,0,0,0], 
    [0,1,1,1], 
    [0,0,0,0]]

def count_neighbours(map, row, col):
    neighbours = 0
    num_rows = len(map)
    num_cols = len(map[0])
    # Check cell to the left
    if row - 1 >= 0 and map[row-1][col] == 1:
        neighbours = neighbours + 1
    if row + 1 < num_rows and map[row + 1][col] == 1:
        neighbours = neighbours + 1
    if col - 1 >= 0 and map[row][col - 1] == 1:
        neighbours = neighbours + 1
    if col + 1 < num_cols and map[row][col + 1] == 1:
        neighbours = neighbours + 1
    if col - 1 >= 0 and row - 1 >= 0 and map[row - 1][col - 1] == 1:
        neighbours = neighbours + 1
    if col + 1 < num_cols and row + 1 < num_rows and map[row + 1][col + 1] == 1:
        neighbours = neighbours + 1
    if col - 1 >= 0 and row + 1 < num_rows and map[row + 1][col - 1] == 1:
        neighbours = neighbours + 1
    if col + 1 < num_cols and row - 1 >= 0 and map[row - 1][col + 1] == 1:
        neighbours = neighbours + 1
    return neighbours

def draw_map(map):
    s = ""
    for x in range(len(map)):
        for y in range(len(map[x])):
            if map[x][y] == 0:
                s = s + "   "
            else:
                s = s + " * "
        s = s + "\n"
    return s

def init_curses():
    scr = curses.initscr()
    scr.keypad(0)
    curses.noecho()
    return scr

def curses_draw_map(scr, map):
    scr.addstr(0, 0, map)
    scr.refresh()
    #scr.getch()

def process_cells(map):
    # Any live cell with two or three live neighbours survives.
    # Any dead cell with three live neighbours becomes a live cell.
    # All other live cells die in the next generation. Similarly, all other dead cells stay dead.
    new_map = [[0]*len(map[0]) for i in range(len(map))]
    for row in range(len(map)):
        for col in range(len(map[row])):
            neighbours = count_neighbours(map, row, col)
            cell = map[row][col]
            if cell == 1 and (neighbours == 3 or neighbours == 2):
                #print(row, col, "survives")
                new_map[row][col] = 1
            if cell == 0 and neighbours == 3:
                #print(row, col, "is born")
                new_map[row][col] = 1
            if cell == 1 and (neighbours > 3 or neighbours < 2):
                #print(row, col, "dies")
                new_map[row][col] = 0

    return new_map

scr = init_curses()
the_map = map

while changing == True:

    if the_map == process_cells (the_map):
        changing = False

    the_map = process_cells(the_map)
    s = draw_map(the_map)
    #print(s)
    curses_draw_map(scr, s)

    
    #print("map2")
    #processed_map = process_cells(map2)   
    #draw_map(processed_map) 
    time.sleep(0.5)
