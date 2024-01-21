#!/usr/bin/env -S pkgx java -jar processing-py.jar .
import random

width, height = 1000, 1000
# Box size for the grid
factor = 50

grid = []
stack = []

current = None
first_run = True

def setup():
    size(width, height)
    # frameRate(5)

    cols = int(width/factor)
    rows = int(height/factor)
    print("cols:", cols, "rows:", rows, 'total > ', cols*rows)

    # instantiate every needed cell
    for row in range(rows):
        for col in range(cols):
            cell = Cell(col, row)
            grid.append(cell)

    current = grid[0]
    stack.append(current)

def draw():
    global current
    global first_run
    global stack
    background(51)

    for cell in grid:
        cell.show()

    if(current is None):
        if first_run:
            first_run = False
            current = grid[0]
        return

    current.hightlight(True)
    current.visited = True
    next = current.checkNeighbors()

    if (next is not None):
        next.visited = True
        current.removeWalls(next)
        current = next
        stack.append(current)

    else:
        newStack = []
        for i in range(len(stack)):
            if (stack[i].checkNeighbors() is not None):
                newStack.append(stack[i])

        stack = newStack
        if len(stack) is 0:
            current = grid[0]
        else:
            stack[-1].hightlight(False)
            current = stack[-1]


def Index(i, j):
    cols = int(width/factor)
    rows = int(height/factor)

    if (i < 0 or j < 0 or i >= cols or j >= rows):
        return -1
    return i + j * cols

class Cell():
    def __init__(self, col,row):
        self.col = col
        self.row = row
        self.visited = False
        self.walls = [
            True, # top
            True, # right
            True, # bottom
            True  # left
        ]



    def removeWalls(self, neighbor):
        x = self.col - neighbor.col
        y = self.row - neighbor.row
        
        if(x is 1): # left
            self.walls[3] = False
            neighbor.walls[1] = False
        elif x is -1: # right
            self.walls[1] = False
            neighbor.walls[3] = False
        elif y is 1: # top
            self.walls[0] = False
            neighbor.walls[2] = False
        elif y is -1: # bottom
            self.walls[2] = False
            neighbor.walls[0] = False

    def checkNeighbors(self):
        neighbors = []

        top    = Index(self.col + 0, self.row - 1)
        right  = Index(self.col + 1, self.row - 0)
        bottom = Index(self.col - 0, self.row + 1)
        left   = Index(self.col - 1, self.row + 0)

        if (top != -1 and
            not grid[top].visited):
            neighbors.append(grid[top])
        if (right != -1 and
            not grid[right].visited):
            neighbors.append(grid[right])
        if (bottom != -1 and
            not grid[bottom].visited):
            neighbors.append(grid[bottom])
        if (left != -1 and
            not grid[left].visited):
            neighbors.append(grid[left])
        
        if(len(neighbors) > 0):
            r = random.randint(0, len(neighbors) - 1)
            return neighbors[r]
        else:
            return None

    def hightlight(self, isCurrent):
        ix = self.col * factor
        iy = self.row * factor
        fx = ix + factor
        fy = iy + factor
        
        noStroke()
        if(isCurrent):
            fill(0, 255, 0, 1000)
            rect(ix,iy, factor,factor)
        else:
            fill(200, 0, 0, 100)
            rect(ix,iy, factor,factor)

    def show(self):
        ix = self.col * factor
        iy = self.row * factor
        fx = ix + factor
        fy = iy + factor

        stroke(255)

        if(self.walls[0]):
            line(fx, iy, ix, iy) # top
        if(self.walls[1]):
            line(fx, iy, fx, fy) # right
        if(self.walls[2]):
            line(fx, fy, ix, fy) # botom
        if(self.walls[3]):
            line(ix, fy, ix, iy) # left


        noStroke()
        if(self.visited):
            fill(0, 200, 100, 100)
            rect(ix,iy, factor,factor)
      
