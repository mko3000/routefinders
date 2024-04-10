from queue import PriorityQueue
from collections import deque
from grid import *
from map_handler import MapHandler
from math import sqrt


class Jump_point_search:
    def __init__(self, grid) -> None:
        self.grid = grid
        self.setup_grid()
        start = self.grid.start
        self.g_score = {tile: float("inf") for row in grid.grid for tile in row}
        self.g_score[start] = 0
        self.f_score = {tile: float("inf") for row in grid.grid for tile in row}
        self.f_score[start] = self.heuristic(start)
        self.cameFrom = {}
        self.route = []
        self.order = []

    def setup_grid(self):
        self.grid.grid = [[JPS_tile.from_Tile(tile) for tile in row] for row in self.grid.grid]
        self.grid.start = self.grid.get_tile(self.grid.start.x, self.grid.start.y)
        self.grid.end = self.grid.get_tile(self.grid.end.x, self.grid.end.y)
        self.grid.update_all_neighbors() # pitäiskö tässä tehdä jo jotain muuta?
    
    def heuristic(self, tile):
        end = self.grid.end
        return abs(tile.x-end.x)+abs(tile.y-end.y)
    
    def jst_neighbors(self, tile):
        neighbors = []
        for neighbor in tile.natural_neighbors:
            dx = neighbor.x - tile.x
            dy = neighbor.y - tile.y
            x = tile.x
            y = tile.y
            while self.grid.valid_coordinates(x,y):
                if self.grid.get_tile(x,y).blocked:
                    break
                if self.grid.get_tile(x,y) != tile:
                    neighbors.append(self.grid.get_tile(x,y))
                x += dx
                y += dy
        return neighbors


class A_star:
    def __init__(self, grid, allow_diagonal = False) -> None:
        self.grid = grid
        self.diagonal = allow_diagonal        
        self.setup_grid()
        self.grid.start.g_score = 0
        self.grid.start.f_scpre = self.heuristic(self.grid.start)
        self.cameFrom = {}
        self.route = []
        self.order = []

    def setup_grid(self):
        self.grid.grid = [[Astar_tile.from_Tile(tile) for tile in row] for row in self.grid.grid]
        self.grid.start = self.grid.get_tile(self.grid.start.x, self.grid.start.y)
        self.grid.end = self.grid.get_tile(self.grid.end.x, self.grid.end.y)
        self.grid.update_all_neighbors(self.diagonal)
    
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

    def run_a_star(self):
        grid = self.grid
        start = self.grid.start

        count = 0
        open_set = PriorityQueue()
        open_set.put((start.g_score,count,start))

        open_set_hash = {start} #for checkning items in the prioirity queue

        while not open_set.empty():

            current = open_set.get()[2]
            open_set_hash.remove(current)
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
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((neighbor.f_score, count, neighbor))
                        open_set_hash.add(neighbor)
                        
            if current != start:
                neighbor.visited = True

        return False
    
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
    small_grid = Grid(4,3)
    small_grid.change_tile_state(1,1)
    small_grid.change_tile_state(1,2)
    # small_grid.change_tile_state(1,0)
    small_grid.set_end(2,2)
    print(small_grid)
    #screen = pygame.display.set_mode((small_grid.w*30, small_grid.h*30))
    screen = None
    small_grid.update_all_neighbors()
    #[[tile.update_neighbors(small_grid)for tile in row] for row in small_grid.grid]
    # small_grid.start.update_neighbors(small_grid)
    # small_grid.end.update_neighbors(small_grid)

    # old = dijkstra(small_grid, screen, (225,0,225))
    # print(old)
    if not True:
        d = Dijkstra(small_grid, screen, (225,0,225))
        results = d.run_dijkstra()
        order = results[0]
        print("order",order)
        for t in order:
            #print(t)
            print(order.index(t),":",t)
        route = d.get_route()
        handled = results[1]

        print("handled")
        for t in handled:
            if handled[t]:
                print(t)
        
        print(f'end {id(small_grid.end)} handled: {small_grid.end in handled}')
        print(route)
    # for tile in d[0]:
    #     print(f'{tile[1]}')
    # # print("dist")
    # # for tile in d[0]:
    # #     print(f'{tile} - {d[0][tile]}')
    # print("handled")



    # handler = MapHandler()
    # test_map = handler.load_map("test_map")
    # print(test_map)
    # [[tile.update_neighbors(test_map)for tile in row] for row in test_map.grid]
    # screen = pygame.display.set_mode((test_map.w*30, test_map.h*30))

    # d = dijkstra(test_map, screen, (225,0,225))
    # print(d)
    # for tile in d[0]:
    #     print(f'{tile[1]}')
    # # print("dist")
    # # for tile in d[0]:
    # #     print(f'{tile} - {d[0][tile]}')
    # print("handled")
    # for tile in d[1]:
    #     print(f'{tile} - {d[1][tile]}')

    a = A_star(small_grid)
    a_result = a.run_a_star()
    print(a_result)
    route = a.route
    print(route)
    for x in route:
        print(x)

    d = Dijkstra(small_grid)
    d_result = d.run_dijkstra()
    print(d_result)
    route = d.route
    for x in route:
        print(x)

    # for tile in result[1]:
    #     print(tile,":",result[1][tile])

    # cameFrom = result[1]
    # current = small_grid.end
    # while current in cameFrom:
    #     current = cameFrom[current]
    #     print(current)