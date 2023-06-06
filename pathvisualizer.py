import pygame 
import math
from queue import PriorityQueue

width =800
window = pygame.display.set_mode((width,width))
pygame.display.set_caption("A* Path Finding Algorithm")


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.color = (0,0,0)
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def has_closed(self):
        return self.color == (255,0,0)

    def is_open(self):
       return self.color == (0,0,255)

    def is_barrier(self):
       return self.color == (255,255,255)

    def is_start(self):
       return self.color == (0,255,0)

    def is_end(self):
       return self.color == (255,255,0)

    def reset(self):
       self.color = (0,0,0)

    def make_start(self):
        self.color = (0,255,0)

    def make_closed(self):
        self.color = (255,0,0)
    
    def make_open(self):
        self.color = (0,0,255)

    def make_barrier(self):
        self.color = (255,255,255)

    def make_end(self):
        self.color = (255,255,0)

    def make_path(self):
        self.color = (0,255,255)

    def draw(self,window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows-1 and not grid[self.row +1][self.col].is_barrier(): #down
             self.neighbors.append(grid[self.row+1][self.col])

        if self.row > 0 and not grid[self.row -1][self.col].is_barrier(): #up
             self.neighbors.append(grid[self.row-1][self.col])

        if self.col < self.total_rows-1 and not grid[self.row ][self.col+1].is_barrier(): #right
             self.neighbors.append(grid[self.row][self.col+1])  

        if self.col > 0 and not grid[self.row][self.col-1].is_barrier(): #left
             self.neighbors.append(grid[self.row][self.col-1])     

    def less_than(self, other):
        return False

def h(p1, p2):
    x1,y1 = p1
    x2,y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def drawPath(prev_node, current, draw):
    while current in prev_node:
         current = prev_node[current]
         current.make_path()
         draw()

#A* algorithm
def algorithm(draw, grid, start, end):
    count =0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    prev_node = {}
    g_score = {node: float("inf") for row in grid for node in row} #distance from start node to current node
    g_score[start]=0
    f_score = {node: float("inf") for row in grid for node in row} #approximate distance from current node to end node
    f_score[start]=h(start.get_pos(), end.get_pos())

    open_set_hash = {start} #Check items in priority queue

    while not open_set.empty():
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                pygame.quit()   

        current = open_set.get()[2] #get node with smallest f score value (minimum heap)
        open_set_hash.remove(current) #Sync with opensethash

        if current == end: #End node reached
             drawPath(prev_node, end , draw)
             end.make_end()
             return True
        
        for neighbor in current.neighbors: #Check all neighbors
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                 prev_node[neighbor] = current
                 g_score[neighbor] = temp_g_score
                 f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                 if neighbor not in open_set_hash:
                      count+=1
                      open_set.put((f_score[neighbor], count, neighbor))
                      open_set_hash.add(neighbor)
                      neighbor.make_open()
        draw()     

        if current != start:
            current.make_closed()   

    return False      

def make_grid(rows,width):
       grid =[]
       gap = width // rows #integer division

       for i in range(rows):
              grid.append([])
              for j in range(rows):
                     node = Node(i,j, gap, rows)
                     grid[i].append(node)

       return grid
def draw_borders(window, rows, width):
       gap = width // rows
       for i in range(rows):
            pygame.draw.line(window, (255,255,255),(0, i*gap), (width, i*gap)  )
            for j in range(rows):
                pygame.draw.line(window, (255,255,255),(j*gap, 0), (j*gap, width)  )

def draw (window, grid, rows, width):
        window.fill((0,0,0))

        for row in grid:
            for node in row:
                node.draw(window)

        draw_borders(window,rows,width)
        pygame.display.update()

def get_clicked_pos(pos, rows, width):
       gap = width // rows
       y,x = pos

       row = y // gap
       col = x // gap

       return row, col

def main(window, width):
        numRows = 20
        grid = make_grid(numRows, width)

        startPos = None
        endPos = None
        running = True

        #Events handler
        while running:
            draw(window, grid, numRows, width)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                       running = False
                
                if pygame.mouse.get_pressed()[0]: #left mouse button
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, numRows, width)
                    node = grid[row][col]
                    
                    if not startPos and node != endPos:
                        startPos = node
                        startPos.make_start()

                    elif not endPos and node!=startPos:
                        endPos = node
                        endPos.make_end() 
                    
                    elif node != endPos and node != startPos:
                        node.make_barrier()


                elif pygame.mouse.get_pressed()[2]: #right mouse button       
                        pos = pygame.mouse.get_pos()
                        row, col = get_clicked_pos(pos, numRows, width)
                        node = grid[row][col] 
                        node.reset()
                        
                        if node == startPos:
                             startPos = None
                        elif node == endPos:
                             endPos = None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and startPos and endPos:
                        for row in grid:
                            for node in row:
                                node.update_neighbors(grid)

                        algorithm(lambda: draw(window, grid, numRows, width), grid, startPos, endPos)

                    if event.key == pygame.K_c:
                         startPos= None
                         endPos = None
                         grid = make_grid(numRows, width)
                        

        pygame.quit()

main(window, width)