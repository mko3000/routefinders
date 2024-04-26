from queue import PriorityQueue
from grid import *
from map_handler import MapHandler
from math import sqrt, copysign
from time import time
import heapq



class Direction:
    def __init__(self,a:Tile=None,b:Tile=None):
        if not a or not b:
            self.horizontal = 0
            self.vertical = 0
            self.diagonal = False
        else:
            dh = b.x-a.x
            if dh != 0:
                dh = int(copysign(1,(b.x-a.x)))
            self.horizontal = dh
            dv = b.y-a.y
            if dv != 0:
                dv = int(copysign(1,(b.y-a.y)))
            self.vertical = dv
            self.diagonal = self.horizontal != 0 and self.vertical != 0

    def set_direction(self, h, v):
        if h not in range(-1,2) or v not in range(-1,2):
            return
        self.horizontal = h
        self.vertical = v
        self.diagonal = self.horizontal != 0 and self.vertical != 0

    def get_orthagonal(self):
        horizontal = Direction()
        horizontal.set_direction(self.horizontal, 0)
        vertical = Direction()
        vertical.set_direction(0,self.vertical)
        return (horizontal, vertical)

    def __str__(self) -> str:
        return f'h:{self.horizontal}, v:{self.vertical}, diagonal:{self.diagonal}'


class Jump_point_search:
    def __init__(self, grid) -> None:
        self.grid = grid
        self.setup_grid()
        self.grid.start.g_score = 0
        self.grid.start.f_score = self.heuristic(self.grid.start)
        self.cameFrom = {}
        self.route = []
        self.order = []

    
    def setup_grid(self):
        self.grid.grid = [[JPS_tile.from_Tile(tile) for tile in row] for row in self.grid.grid]
        self.grid.start = self.grid.get_tile(self.grid.start.x, self.grid.start.y)
        self.grid.end = self.grid.get_tile(self.grid.end.x, self.grid.end.y)
        self.grid.update_all_neighbors(diagonal=True)
    
    
    def prune_neighbors(self, came_from, tile):
        d = Direction(came_from, tile)
        
        # sääntö 1, jos ortogonaalinen liike, poistetaan muut paitsi se, mikä on parentista katsottuna tilestä seuraava
        if not d.diagonal:
            natural_neighbor = self.grid.get_free_tile(tile.x + d.horizontal, tile.y + d.vertical)
            if natural_neighbor and natural_neighbor not in tile.natural_neighbors:
                tile.natural_neighbors.append(natural_neighbor)
        
        # sääntö 2, jos diagonaalinen liike, ...
        if d.diagonal:
            natural_neighbors = [
                self.grid.get_free_tile(tile.x + d.horizontal, tile.y + d.vertical),
                self.grid.get_free_tile(tile.x, tile.y + d.vertical),
                self.grid.get_free_tile(tile.x + d.horizontal, tile.y)
            ]
            for natural_neighbor in natural_neighbors:
                if natural_neighbor and natural_neighbor not in tile.natural_neighbors:
                    tile.natural_neighbors.append(natural_neighbor)
        
        # sääntö 3, lisätään forced neighboreita
        adjacent_coordinates = []
        forced_neighbor = None
        if d.horizontal == 0: # moving vertically
            adjacent_coordinates = [(tile.x-1, tile.y),(tile.x+1,tile.y)]
        if d.vertical == 0: # moving horizontally
            adjacent_coordinates = [(tile.x, tile.y-1),(tile.x, tile.y+1)]
        if d.horizontal > 0 and d.vertical > 0: # moving from top left to bottom right
            adjacent_coordinates = [(tile.x-1, tile.y),(tile.x, tile.y-1)]
        if d.horizontal < 0 and d.vertical < 0: # moving from bottom right to top left
            adjacent_coordinates = [(tile.x+1, tile.y),(tile.x, tile.y+1)]
        if d.horizontal > 0 and d.vertical < 0: # moving from bottom left to top right
            adjacent_coordinates = [(tile.x-1, tile.y),(tile.x, tile.y+1)]
        if d.horizontal < 0 and d.vertical > 0: # moving from top right to bottom left
            adjacent_coordinates = [(tile.x+1, tile.y),(tile.x, tile.y-1)]
        for c in adjacent_coordinates:
            x,y = c[0],c[1]
            adjacent_neighbor = self.grid.get_tile(x,y)
            if adjacent_neighbor and adjacent_neighbor.blocked:
                if not d.diagonal:
                    forced_neighbor = self.grid.get_free_tile(x+d.horizontal, y+d.vertical)
                else:
                    d2 = Direction(came_from, adjacent_neighbor)
                    forced_neighbor = self.grid.get_free_tile(x+d2.horizontal, y+d2.vertical)        
        if forced_neighbor and forced_neighbor not in tile.forced_neighbors:
            tile.forced_neighbors.append(forced_neighbor)

    
    def identify_successors(self, came_from, tile): 
        successors = []
        self.prune_neighbors(came_from, tile)
        pruned_neighbors = tile.natural_neighbors + tile.forced_neighbors
        for n in pruned_neighbors:
            n = self.jump(tile,Direction(tile, n))
            if n:
                successors.append(n)
        return successors

    
    def jump(self,tile,d):
        n = self.grid.get_free_tile(tile.x + d.horizontal, tile.y + d.vertical)
        if not n:
            return None
        if n == self.grid.end:
            return n
        self.prune_neighbors(tile, n)
        if n.forced_neighbors: #checks if one of the neighbors is forced
            return n
        if d.diagonal:
            for i in range(2):
                direction = d.get_orthagonal()[i]
                if self.jump(n,direction):
                    return n
        return self.jump(n,d)
    
    
    def run_jps(self):
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
        d = Direction(a,b)
        dx = abs(d.horizontal)
        dy = abs(d.vertical)
        lx = abs(a.x-b.x)
        ly = abs(a.y-b.y)
        if dx != 0 and dy != 0:
            return lx * 14
        else:
            return (dx * lx + dy * ly) * 10
    
    
    def heuristic(self, tile):
        end = self.grid.end
        dx = abs(tile.x-end.x)
        dy = abs(tile.y-end.y)
        if dx > dy:
            return 14 * dy + 10 * (dx - dy)
        else:
            return 14 * dx + 10 * (dy - dx)
        #return abs(tile.x-end.x)+abs(tile.y-end.y)
    
    
    def get_route(self):
        current = self.grid.end
        while current in self.cameFrom:
            self.route.append(current)
            current = self.cameFrom[current]
        self.route.append(self.grid.start)
        self.route = self.route[::-1]

    
    def get_dist(self):
        distance = 0
        for i in range(len(self.route)-1):
            distance += self.get_distance_between_points(self.route[i], self.route[i+1])
        return distance
        
    
    def get_distance_between_points(self,a,b):
        dx = abs(a.x-b.x)
        dy = abs(a.y-b.y)
        return max(dx,dy)
    

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


if __name__ == "__main__":
    
    if  True:
        mh = MapHandler()
        test_map = mh.load_movingai_map('movingai-maps/street-map/','Berlin_0_256.map')
        
        # test_map = mh.load_map("s3")
        # test_map.set_start(0,berlin.h-1)
        # test_map.set_end(berlin.w-1,0)
        test_map.set_random_start()
        test_map.set_random_end()
        # test_map.set_start(93,56)
        # test_map.set_end(134,77)
        start = test_map.start
        end = test_map.end
        print(test_map)
        print(f'start: {test_map.start}, end: {test_map.end}')

        jps = Jump_point_search(test_map)
        s = time()
        jps_result = jps.run_jps()
        e = time()
        print(f'JPS: {jps_result}, visited: {len(jps.order)}, length: {jps.get_dist()}, time: {round(e-s,6)}')


        #berlin = mh.reload_map()
        test_map = mh.load_movingai_map('movingai-maps/street-map/','Berlin_0_256.map')
        #berlin = mh.load_map("s3")
        test_map.set_start(start.x,start.y)
        test_map.set_end(end.x,end.y)
        astar = A_star(test_map, allow_diagonal=True)
        s = time()
        astar_result = astar.run_a_star()
        e = time()
        print(f'ASTAR: {astar_result}, visited: {len(astar.order)}, length: {len(astar.route)}, time: {round(e-s,6)}')

        #berlin = mh.reload_map()
        test_map = mh.load_movingai_map('movingai-maps/street-map/','Berlin_0_256.map')
        #berlin = mh.load_map("s3")
        test_map.set_start(start.x,start.y)
        test_map.set_end(end.x,end.y)
        dijksta = Dijkstra(test_map, allow_diagonal=True)
        s = time()
        dijksta_result = dijksta.run_dijkstra()
        e = time()
        print(f'DIJKSTRA: {dijksta_result}, visited: {len(dijksta.order)}, length: {len(dijksta.route)}, time: {round(e-s,6)}')
