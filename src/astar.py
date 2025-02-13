from queue import PriorityQueue
from grid import *
from map_handler import MapHandler
from math import sqrt, copysign
from time import time
import heapq



class A_star:
    """
    A class to perform the A* pathfinding algorithm on a grid.

    Attributes:
        grid (Grid): the grid
        diagonal (bool): if true, diagonal movement is allowed
        cameFrom (dict): saves the predecessor if each visited tile
        route (list): the path from start to finish
        order (list): the order in which the tiles were visited
    """
    def __init__(self, grid, allow_diagonal = False) -> None:
        """
        Initializes the A* algorithm

        Parameters:
            grid (Grid): the grid
            allow_diagonal: (bool, optional): if true, diagonal movement is allowed. False by default.
        """
        self.grid = grid
        self.diagonal = allow_diagonal        
        self.setup_grid()
        self.grid.start.g_score = 0
        self.grid.start.f_score = self.heuristic(self.grid.start)
        self.cameFrom = {}
        self.route = []
        self.order = []


    def setup_grid(self):
        """
        Sets up the grid for A* and updates neighbors for every tile.
        """
        self.grid.grid = [[Astar_tile.from_Tile(tile) for tile in row] for row in self.grid.grid]
        self.grid.start = self.grid.get_tile(self.grid.start.x, self.grid.start.y)
        self.grid.end = self.grid.get_tile(self.grid.end.x, self.grid.end.y)
        self.grid.update_all_neighbors(self.diagonal)
    

    def run_a_star(self):
        """
        A* search algorithm to find a path from the start to the end tile.

        Returns:
            bool: True if a path is found, False otherwise.
        """
        grid = self.grid
        start = grid.start
        count = 0
        queue = []
        heapq.heappush(queue, (start.g_score, count, start))
        queue_hash = {start}  # For checking items in the priority queue

        while queue:
            current = heapq.heappop(queue)[2]
            queue_hash.remove(current)
            self.order.append(current)

            if current == grid.end:
                self.get_route()
                return True

            for neighbor in current.neighbors:
                temp_g_score = current.g_score + self.neighbor_g_score(current, neighbor)
                if temp_g_score < neighbor.g_score:
                    self.cameFrom[neighbor] = current
                    neighbor.g_score = temp_g_score
                    neighbor.f_score = temp_g_score + self.heuristic(neighbor, self.diagonal)
                    if neighbor not in queue_hash:
                        count += 1
                        heapq.heappush(queue, (neighbor.f_score, count, neighbor))
                        queue_hash.add(neighbor)

        return False
    
    
    def heuristic(self, tile, diagonal=False):
        """
        Selects eather the diagonal or otrhogonal heuristic cost fuction.

        Parameters:
            tile (Tile): The tile for which the distance is calculated.
            diagonal (bool, optional): If true, uses the heuristic which allows diagonal (45deg) movement in the grid. False by default.

        Returns:
            the estimated cost from the tile to the end tile.
        """
        if diagonal:
            return self.heuristic_diagonal(tile)
        return self.heuristic_orthogonal(tile)
    
        
    def heuristic_orthogonal(self, tile):
        """
        Calculates the Manhattan distance between the given tile and the end tile.

        Parameters:
            tile (Tile): The tile for which the distance is calculated.

        Returns:
            float: The Manhattan distance to the end tile.
        """
        end = self.grid.end
        return abs(tile.x-end.x)+abs(tile.y-end.y)
    
    
    def heuristic_diagonal(self, tile):
        """
        Calculates the diagonal distance heuristic between the given tile and the end tile when diagonal (45deg) movement is allowed.       

        Parameters:
            tile (Tile): The tile for which the distance is calculated.

        Returns:
            float: The distance to the end tile.
        """
        end = self.grid.end
        D_orth = 1
        D_diag = sqrt(2)
        dx = abs(tile.x-end.x)
        dy = abs(tile.y-end.y)
        return D_orth * max(dx, dy) + (D_diag - D_orth) * min(dx, dy)
    

    def neighbor_g_score(self, current, neighbor):
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
        Reconstructs the path from the end to the start using the 'cameFrom' dict and saves it to 'route'.
        """
        current = self.grid.end
        while current in self.cameFrom:
            current = self.cameFrom[current]
            self.route.append(current)