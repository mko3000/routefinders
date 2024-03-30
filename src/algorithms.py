from queue import PriorityQueue
from collections import deque
from grid import Grid, Tile
from map_handler import MapHandler
#import pygame

# def quit_condition():
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()

def a_star(grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0,count,start))
    cameFrom = {}
    g_score = {tile: float("inf") for row in grid for tile in row}
    g_score[start] = 0

    open_set_hash = {start} #for checknig items in the prioirity queue

    while not open_set.empty():
        #quit_condition()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == grid.get_tile(grid.end[0], grid.end[1]):
            return True
        

class Dijkstra:
    def __init__(self, grid, screen, c):
        self.grid = grid
        self.handled = {tile: False for row in grid.grid for tile in row}
        self.route = []

    def run_dijkstra(self):
        start = self.grid.start
        end = self.grid.end
        start.dist = 0
        heap = PriorityQueue()
        heap.put((start.dist,start))
        order = []

        while not heap.empty():
            tile = heap.get()[1]
            order.append(tile)
            if self.handled[tile] == True:
                continue
            self.handled[tile] = True
            if end in tile.neighbors:
                self.handled[end] = True
                end.dist = tile.dist+1
                return order, self.handled, end.dist
            for neighbor in tile.neighbors:
                cur = neighbor.dist
                new = tile.dist + 1
                if new < cur:
                    neighbor.dist = new
                    heap.put((new, neighbor))
        return False

    def get_route(self):
        start = self.grid.start
        step = self.grid.end
        while self.handled[step]:
            self.route.append(step)
            if start in step.neighbors:
                break
            step = min([n for n in step.neighbors if self.handled[n]])
        return self.route




if __name__ == "__main__":
    small_grid = Grid(4,3)
    small_grid.change_tile_state(1,1)
    small_grid.change_tile_state(1,2)
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