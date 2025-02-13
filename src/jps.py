from queue import PriorityQueue
from grid import *
from map_handler import MapHandler
from math import sqrt, copysign
from time import time
import heapq
import cProfile
import re



class Jump_point_search:
    """
    A class to perform the Jump Point Search (jps) pathfinding algorithm on a grid.

    Attributes:
        grid (Grid): the grid
        cameFrom (dict): saves the predecessor if each visited tile
        route (list): the path from start to finish
        order (list): the order in which the tiles were visited
    """
    def __init__(self, grid) -> None:
        """
        Initializes the jps algorithm

        Parameters:
            grid (Grid): the grid
        """
        self.grid = grid
        self.setup_grid()
        self.grid.start.g_score = 0
        self.grid.start.f_score = self.heuristic(self.grid.start)
        self.cameFrom = {}
        self.route = []
        self.order = []

    
    def setup_grid(self):
        """
        Sets up the grid for jps and updates neighbors for every tile.
        """
        self.grid.grid = [[JPS_tile.from_Tile(tile) for tile in row] for row in self.grid.grid]
        self.grid.start = self.grid.get_tile(self.grid.start.x, self.grid.start.y)
        self.grid.end = self.grid.get_tile(self.grid.end.x, self.grid.end.y)
        self.grid.update_all_neighbors(diagonal=True)
    
    
    def prune_neighbors(self, came_from, tile):
        """
        Prunes neighbors according to the rules described in the jps article and saves to tile's natural_neighbors and forced_neighbors.

        Parameters:
            came_from (Tile): the previous tile
            tile (Tile): current tile
        """
        d = self.direction(came_from, tile)
        
        # rule 1: if an orthogonal move, remove others but the one which comes next after the tile as seen from the parent.
        if not d[2]:
            natural_neighbor = self.grid.get_free_tile(tile.x + d[0], tile.y + d[1])
            if natural_neighbor and natural_neighbor not in tile.natural_neighbors:
                tile.natural_neighbors.append(natural_neighbor)
        
        # rule 2: for diagonal movement...
        if d[2]:
            natural_neighbors = [
                self.grid.get_free_tile(tile.x + d[0], tile.y + d[1]),
                self.grid.get_free_tile(tile.x, tile.y + d[1]),
                self.grid.get_free_tile(tile.x + d[0], tile.y)
            ]
            for natural_neighbor in natural_neighbors:
                if natural_neighbor and natural_neighbor not in tile.natural_neighbors:
                    tile.natural_neighbors.append(natural_neighbor)
        
        # rule 3: add forced neighbors
        adjacent_coordinates = []
        forced_neighbor = None
        if d[0] == 0: # moving vertically
            adjacent_coordinates = [(tile.x-1, tile.y),(tile.x+1,tile.y)]
        if d[1] == 0: # moving horizontally
            adjacent_coordinates = [(tile.x, tile.y-1),(tile.x, tile.y+1)]
        if d[0] > 0 and d[1] > 0: # moving from top left to bottom right
            adjacent_coordinates = [(tile.x-1, tile.y),(tile.x, tile.y-1)]
        if d[0] < 0 and d[1] < 0: # moving from bottom right to top left
            adjacent_coordinates = [(tile.x+1, tile.y),(tile.x, tile.y+1)]
        if d[0] > 0 and d[1] < 0: # moving from bottom left to top right
            adjacent_coordinates = [(tile.x-1, tile.y),(tile.x, tile.y+1)]
        if d[0] < 0 and d[1] > 0: # moving from top right to bottom left
            adjacent_coordinates = [(tile.x+1, tile.y),(tile.x, tile.y-1)]
        for c in adjacent_coordinates:
            x,y = c[0],c[1]
            adjacent_neighbor = self.grid.get_tile(x,y)
            if adjacent_neighbor and adjacent_neighbor.blocked:
                if not d[2]:
                    forced_neighbor = self.grid.get_free_tile(x+d[0], y+d[1])
                else:
                    d2 = self.direction(came_from, adjacent_neighbor)
                    forced_neighbor = self.grid.get_free_tile(x+d2[0], y+d2[1])        
        if forced_neighbor:
            tile.forced_neighbors.append(forced_neighbor)

    
    def identify_successors(self, came_from, tile): 
        """
        Indentifies successors

        Parameters:
            came_from (Tile): the previous tile
            tile (Tile): current tile

        Returns:
            list: a list of successor tiles
        """
        successors = []
        self.prune_neighbors(came_from, tile)
        pruned_neighbors = tile.natural_neighbors + tile.forced_neighbors
        for n in pruned_neighbors:
            n = self.jump(tile,self.direction(tile, n))
            if n:
                successors.append(n)
        return successors

    
    # def jump2(self,tile,d):
    #     """
    #     not in use, remove
    #     """
    #     n = self.grid.get_free_tile(tile.x + d[0], tile.y + d[1])
    #     if not n:
    #         return None
    #     if n == self.grid.end:
    #         return n
    #     self.prune_neighbors(tile, n)
    #     if n.forced_neighbors: #checks if one of the neighbors is forced
    #         return n
    #     if d[2]:
    #         orthagonals = ((d[0],0,False),(0,d[1],False))
    #         for i in range(2):
    #             direction = orthagonals[i]
    #             if self.jump(n,direction):
    #                 return n
    #     return self.jump(n,d)
    
    def jump(self, tile, d):
        """
        Jumps from tile towards the given direction

        Parameters:
            tile (Tile): The tile from which the jump is initiated.
            d (3-tuple): direction of movement (right/left, up/down, diagonal(bool))

        Returns:
            Tile: the next tile, or None
        """
        while True:
            next_tile = self.grid.get_free_tile(tile.x + d[0], tile.y + d[1])
            if not next_tile:
                return None
            if next_tile == self.grid.end:
                return next_tile

            self.prune_neighbors(tile, next_tile)
            if next_tile.forced_neighbors:
                return next_tile

            if d[2]:
                orthagonals = ((d[0],0,False),(0,d[1],False))
                for direction in orthagonals:
                    if self.jump(next_tile,direction):
                        return next_tile
            
            tile = next_tile

    
    def run_jps(self):
        """
        Jump Poin Search algorithm to find a path from the start to the end tile.

        Returns:
            bool: True if a path is found, False otherwise.
        """
        grid = self.grid
        start = grid.start
        count = 0
        open_set = []
        heapq.heappush(open_set, (start.g_score, count, start))
        open_set_hash = {start}
        close_set = set()

        while open_set:
            current = heapq.heappop(open_set)[2]
            open_set_hash.remove(current)
            self.order.append(current)
            if current == grid.end:
                self.get_route()
                return True
            
            close_set.add(current)

            if current is start:
                successors = start.neighbors
            else:
                successors = self.identify_successors(self.cameFrom[current], current)

            for s in successors:
                jump_point = s
                if jump_point in close_set:
                    continue

                temp_g_score = current.g_score + self.neighbor_g_score(current, jump_point)
                if temp_g_score < jump_point.g_score:
                    self.cameFrom[jump_point] = current
                    jump_point.g_score = temp_g_score
                    jump_point.f_score = temp_g_score + self.heuristic(jump_point)
                    if jump_point not in open_set_hash:
                        count += 1
                        heapq.heappush(open_set, (jump_point.f_score, count, jump_point))
                        open_set_hash.add(jump_point)
        return False

    
    def neighbor_g_score(self, a, b):
        """
        Calculates the g score between two tiles.

        Parameters:
            a (Tile): first tile
            b (Tile): second tile

        Returns:
            float: the g score between tiles a and b
        """
        d = self.direction(a,b)
        dx = abs(d[0])
        dy = abs(d[1])
        lx = abs(a.x-b.x)
        ly = abs(a.y-b.y)
        if dx != 0 and dy != 0:
            return lx * 14
        else:
            return (dx * lx + dy * ly) * 10
    
    
    def heuristic(self, tile):
        """
        Calculates the heuristic cost from the given tile to the end tile.

        Parameters:
            tile (Tile): The tile for which the heuristic is calculated.

        Returns:
            float: the estimated cost form the given tile to the end tile.
        """
        end = self.grid.end
        dx = abs(tile.x-end.x)
        dy = abs(tile.y-end.y)
        if dx > dy:
            return 14 * dy + 10 * (dx - dy)
        else:
            return 14 * dx + 10 * (dy - dx)
    
    
    def get_route(self):
        """
        Reconstructs the path from the end to the start using the 'cameFrom' dict and saves it to 'route'.
        """
        current = self.grid.end
        while current in self.cameFrom:
            self.route.append(current)
            current = self.cameFrom[current]
        self.route.append(self.grid.start)
        self.route = self.route[::-1]

    
    def get_dist(self):
        """
        Calculates the length of the route

        Returns:
            int: route length
        """
        distance = 0
        for i in range(len(self.route)-1):
            distance += self.get_distance_between_points(self.route[i], self.route[i+1])
        return distance
        
    
    def get_distance_between_points(self,a,b):
        """
        Gives the distance between two tiles.

        Parameters:
            a (Tile): first tile
            b (Tile): second tile

        Returns:
            int: number of tiles from a to b 
        """
        dx = abs(a.x-b.x)
        dy = abs(a.y-b.y)
        return max(dx,dy)
    

    def direction(self,a,b):
        """
        Gives the direction when going from tile a to tile b. Also tells if the direction is diagonal.

        Parameters:
            a (Tile): first tile
            b (Tile): second tile
        
        Returns:
            tuple (int, int, bool): horisontal direction (-1 or 1), vertical direction (-1 or 1), diagonal movement (True or False)
        """
        dh = b.x-a.x
        if dh != 0:
            dh = int(copysign(1,(b.x-a.x)))
        dv = b.y-a.y
        if dv != 0:
            dv = int(copysign(1,(b.y-a.y)))
        diagonal = dh != 0 and dv != 0
        return(dh, dv, diagonal)
