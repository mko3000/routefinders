from queue import PriorityQueue
from grid import *
from map_handler import MapHandler
from math import sqrt, copysign
from time import time
import heapq



class A_star:
    def __init__(self, grid, allow_diagonal = False) -> None:
        self.grid = grid
        self.diagonal = allow_diagonal        
        self.setup_grid()
        self.grid.start.g_score = 0
        self.grid.start.f_score = self.heuristic(self.grid.start)
        self.cameFrom = {}
        self.route = []
        self.order = []


    def setup_grid(self):
        self.grid.grid = [[Astar_tile.from_Tile(tile) for tile in row] for row in self.grid.grid]
        self.grid.start = self.grid.get_tile(self.grid.start.x, self.grid.start.y)
        self.grid.end = self.grid.get_tile(self.grid.end.x, self.grid.end.y)
        self.grid.update_all_neighbors(self.diagonal)
    

    def run_a_star(self):
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
        if diagonal:
            return self.heuristic_diagonal(tile)
        return self.heuristic_orthogonal(tile)
    
        
    def heuristic_orthogonal(self, tile):
        end = self.grid.end
        return abs(tile.x-end.x)+abs(tile.y-end.y)
    
    
    def heuristic_diagonal(self, tile):
        end = self.grid.end
        D_orth = 1
        D_diag = sqrt(2)
        dx = abs(tile.x-end.x)
        dy = abs(tile.y-end.y)
        return D_orth * max(dx, dy) + (D_diag - D_orth) * min(dx, dy)
    

    def neighbor_g_score(self, current, neighbor):
        if abs(neighbor.x-current.x) == 1 and abs(neighbor.y-current.y) == 1:
            return sqrt(2)
        return 1
    
    
    def get_route(self):
        current = self.grid.end
        while current in self.cameFrom:
            current = self.cameFrom[current]
            self.route.append(current)