from dijkstra import Dijkstra
from astar import A_star
from jps import Jump_point_search
from time import time
from map_handler import MapHandler
import random
import cProfile
import re


class Comparison:
    def __init__(self) -> None:
        self.path = 'movingai-maps/'
        self.maps = ['Berlin_0_256.map',"Denver_0_256.map",'Sydney_2_512.map','Paris_2_512.map','NewYork_1_256.map','thecrucible.map','divideandconquer.map','battleground.map']
        self.map_handler = MapHandler()

    def setup_map(self):
        mapfile = self.maps[random.randint(0,len(self.maps)-1)]
        m = self.map_handler.load_movingai_map(self.path,mapfile)
        m.set_random_start()
        m.set_random_end()
        return (m, mapfile, m.start, m.end)
    
    def reset_map(self, mapfile, start, end):
        m = self.map_handler.load_movingai_map(self.path,mapfile)
        m.set_start(start.x,start.y)
        m.set_end(end.x,end.y)
        return m

    def run_algorithms(self):        
        map_setup = self.setup_map()
        test_map, mapfile, start, end = map_setup
        print(test_map)
        print(mapfile)
        print(f'start: ({start.x},{start.y}), end: ({end.x},{end.y})\n')

        jps = Jump_point_search(test_map)
        s = time()
        jps_result = jps.run_jps()
        e = time()
        print(f'JPS: {jps_result}, visited: {len(jps.order)}, length: {jps.get_dist()}, time: {round(e-s,6)}')

        test_map = self.reset_map(mapfile, start, end)
        astar = A_star(test_map, allow_diagonal=True)
        s = time()
        astar_result = astar.run_a_star()
        e = time()
        print(f'ASTAR: {astar_result}, visited: {len(astar.order)}, length: {len(astar.route)}, time: {round(e-s,6)}')

        test_map = self.reset_map(mapfile, start, end)
        test_map.set_start(start.x,start.y)
        test_map.set_end(end.x,end.y)
        dijksta = Dijkstra(test_map, allow_diagonal=True)
        s = time()
        dijksta_result = dijksta.run_dijkstra()
        e = time()
        print(f'DIJKSTRA: {dijksta_result}, visited: {len(dijksta.order)}, length: {len(dijksta.route)}, time: {round(e-s,6)}')



if __name__ == "__main__":
    comp = Comparison()
    comp.run_algorithms()


