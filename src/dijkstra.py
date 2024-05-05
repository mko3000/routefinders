from queue import PriorityQueue
from grid import *
from math import sqrt



class Dijkstra:
    def __init__(self, grid, allow_diagonal = False):
        self.grid = grid
        self.setup_grid(allow_diagonal)
        self.handled = {tile: False for row in grid.grid for tile in row}
        self.route = []
        self.order = []

    
    def setup_grid(self, diagonal):
        self.grid.grid = [[Dijkstra_tile.from_Tile(tile) for tile in row] for row in self.grid.grid]
        self.grid.start = self.grid.get_tile(self.grid.start.x, self.grid.start.y)
        self.grid.end = self.grid.get_tile(self.grid.end.x, self.grid.end.y)
        self.grid.update_all_neighbors(diagonal)
    
    
    def run_dijkstra(self):
        start = self.grid.start
        end = self.grid.end
        start.dist = 0
        heap = PriorityQueue()
        heap.put((start.dist,start))

        while not heap.empty():
            tile = heap.get()[1]
            self.order.append(tile)
            if self.handled[tile] == True:
                continue
            self.handled[tile] = True
            if end in tile.neighbors:
                self.handled[end] = True
                end.dist = tile.dist+1
                self.get_route()
                return True
            for neighbor in tile.neighbors:
                cur = neighbor.dist
                new = tile.dist + self.neighbor_distance(tile, neighbor)
                if new < cur:
                    neighbor.dist = new
                    heap.put((new, neighbor))
        return False
    
    
    def neighbor_distance(self, tile, neighbor):
        if abs(neighbor.x-tile.x) == 1 and abs(neighbor.y-tile.y) == 1:
            return sqrt(2)
        return 1

    
    def get_route(self):
        start = self.grid.start
        step = self.grid.end
        while self.handled[step]:
            self.route.append(step)
            if start in step.neighbors:
                break
            step = min([n for n in step.neighbors if self.handled[n]])