from collections import deque
import pygame
import math
from queue import PriorityQueue

WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE= (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot: #square
    def __init__(self, row, col, width, total_rows):
        self.row = row #where
        self.col = col
        self.x = row * width
        self.y = col * width #track the width of the square - translation of the position the spot on my arr to the
        self.color = WHITE #because change the color
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col #location

    def is_closed(self):
        return self.color == RED #where we already look there

    def is_open(self):
        return self.color == GREEN #we are open place

    def is_barrier(self):
        return self.color == BLACK #barreira

    def is_start(self):
        return self.color == ORANGE #start point

    def is_end(self):
        return self.color == TURQUOISE #

    def is_blank(self):
        return self.color == WHITE

    def reset(self):
        self.color = WHITE #clean

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED #closed

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width)) #draw the square

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): #LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): #RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #UP
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): #DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        # if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): #DOWN
        #     self.neighbors.append(grid[self.row + 1][self.col])
        #
        # if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #UP
        #     self.neighbors.append(grid[self.row - 1][self.col])
        #
        # if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): #RIGHT
        #     self.neighbors.append(grid[self.row][self.col + 1])
        #
        # if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): #LEFT
        #     self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other): #last them. compare two spots together
        return False

#Heuristic function
#Marathan Distance
def h(p1, p2): #point one, point two
    x1, y1 = p1 #p1(3,4)
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def a_star(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end: # create the path
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()
    return False

def dfs(draw, grid, start_spot, end):
    visited = []
    stack = deque()
    came_from = {}
    current_spot = start_spot
    visited.append(current_spot)
    stack.append(current_spot)

    while stack:
        current_spot = stack.pop()
        if current_spot == end:
            current_spot.make_path()
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
        #print(current_spot, end = " ")

        for n in current_spot.neighbors:
            if n.is_blank() or n.is_end() and n not in visited:
                came_from[n] = current_spot
                visited.append(n)
                stack.append(n)
                n.make_open()
        if current_spot!= start_spot:
            current_spot.make_closed()

        draw()
    return False

def bfs(draw, grid, start_spot, end):
    visited = []
    queue = []
    came_from = {}
    current_spot = start_spot
    visited.append(current_spot)
    queue.append(current_spot)

    while queue:
        current_spot = queue.pop(0)
        if current_spot == end:
            current_spot.make_path()
            reconstruct_path(came_from, end, draw)
            end.make_end()
            #end.make_path()
            return True

        for n in current_spot.neighbors:
            if n.is_blank() or n.is_end() and n not in visited:
                came_from[n] = current_spot
                visited.append(n)
                queue.append(n)
                n.make_open()
        if current_spot != start_spot:
            current_spot.make_closed()

        draw()
    return False

#Making grid
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0,i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width, start, end):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)
    #start.draw(win)
    #end.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    #started = False
    while run:
        draw(win, grid, ROWS, width, start, end)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # L
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # R
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    a_star(lambda: draw(win, grid, ROWS, width, start, end), grid, start, end)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    dfs(lambda: draw(win, grid, ROWS, width, start, end), grid, start, end)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b and start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)

                        bfs(lambda: draw(win, grid, ROWS, width, start, end), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(WIN, WIDTH)