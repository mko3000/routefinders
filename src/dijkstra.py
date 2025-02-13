from queue import PriorityQueue
from grid import *
from math import sqrt



class Dijkstra:
    """
    A class to perform the Dijkstra pathfinding algorithm on a grid.

    Attributes:
        grid (Grid): the grid
        handled (dict): a 2d matrix initialized with False for every tile in the grid
        route (list): the path from start to finish
        order (list): the order in which the tiles were visited
    """
    def __init__(self, grid, allow_diagonal = False):
        """
        Initializes the Dijkstra algorithm

        Parameters:
            grid (Grid): the grid
            allow_diagonal: (bool, optional): if true, diagonal movement is allowed. False by default.
        """
        self.grid = grid
        self.setup_grid(allow_diagonal)
        self.handled = {tile: False for row in grid.grid for tile in row}
        self.route = []
        self.order = []

    
    def setup_grid(self, diagonal):
        """
        Sets up the grid for Dijkstra and updates neighbors for every tile.
        """
        self.grid.grid = [[Dijkstra_tile.from_Tile(tile) for tile in row] for row in self.grid.grid]
        self.grid.start = self.grid.get_tile(self.grid.start.x, self.grid.start.y)
        self.grid.end = self.grid.get_tile(self.grid.end.x, self.grid.end.y)
        self.grid.update_all_neighbors(diagonal)
    
    
    def run_dijkstra(self):
        """
        Dijkstra search algorithm to find a path from the start to the end tile.

        Returns:
            bool: True if a path is found, False otherwise.
        """
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
    
    
    def neighbor_distance(self, current, neighbor):
        """
        Calculates the movement cost to the neighboring tile.
        
        Parameters:
            current (Tile): the current tile
            neighbor (Tile): the neighboring tile

        Returns:
            float: the distance in tiles to the neighbor. Sqrt(2) if neighbor is diagonal to the current tile, 1 if not.
        """
        if abs(neighbor.x-current.x) == 1 and abs(neighbor.y-current.y) == 1:
            return sqrt(2)
        return 1

    
    def get_route(self):
        """
        Reconstructs the path from the end to the start.
        """
        start = self.grid.start
        step = self.grid.end
        while self.handled[step]:
            self.route.append(step)
            if start in step.neighbors:
                break
            step = min([n for n in step.neighbors if self.handled[n]])