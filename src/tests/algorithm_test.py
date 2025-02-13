# etsi lyhin reitti Dijkstralla ja vertaa omaa algoritmia niihin
# ota testikeissejä movingai.com:sta
# tee satunnaisgeneroituja karttoja?
# testaa myös satunnaisesti sijoiteuilla alku- ja loppupisteillä
# huom: skenaariotiedostoissa ei pysty skippaamaan kulman yli

import unittest
import astar, dijkstra, jps, grid
from algorithm_tester import Comparison
from map_handler import MapHandler
import random


class TestDijkstra(unittest.TestCase):
    def setUp(self) -> None:
        mh = MapHandler()
        self.test_map = mh.load_map("test_map")

    def test_init_dijkstra(self):
        d = dijkstra.Dijkstra(self.test_map,True)
        self.assertEqual(f'{d.grid.start}', '[(0,0), b:False, n:3, d:inf]')
        self.assertEqual(d.grid.start.dist, float("Inf"))

    def test_run_dijkstra(self):
        d = dijkstra.Dijkstra(self.test_map,True)
        result = d.run_dijkstra()
        self.assertEqual(result,True)
        self.assertEqual(len(d.route),9)

class TestAstar(unittest.TestCase):
    def setUp(self) -> None:
        mh = MapHandler()
        self.test_map = mh.load_map("test_map")

    def test_init_astar(self):
        a = astar.A_star(self.test_map,True)
        self.assertEqual(f'{a.grid.start}', '[(0,0), b:False, n:3]')
        self.assertEqual(a.grid.start.g_score,0)
        self.assertEqual(a.grid.start.f_score,16)

    def test_run_astar(self):
        a = astar.A_star(self.test_map,True)
        result = a.run_a_star()
        self.assertEqual(result,True)
        self.assertEqual(len(a.route),9)

class TestJPS(unittest.TestCase):
    def setUp(self) -> None:
        mh = MapHandler()
        self.test_map = mh.load_map("test_map")

    def test_init_jps(self):
        j = jps.Jump_point_search(self.test_map)
        self.assertEqual(f'{j.grid.start}', '[(0,0), b:False, n:3]')
        self.assertEqual(j.grid.start.g_score,0)
        self.assertEqual(j.grid.start.f_score,118)
        self.assertEqual(j.grid.start.natural_neighbors,[])

    def test_run_jps(self):
        j = jps.Jump_point_search(self.test_map)
        result = j.run_jps()
        self.assertEqual(result,True)
        self.assertEqual(j.get_dist(),9)

class TestAlgorithms(unittest.TestCase):
    """
    First runs Dijkstra on a random Moving AI benchmark map with random start and end locations and compares A* and JPS results to it.
    """
    def setUp(self) -> None: 
        self.path = 'movingai-maps/'
        self.maps = ['Berlin_0_256.map',"Denver_0_256.map",'Sydney_2_512.map','Paris_2_512.map','NewYork_1_256.map','thecrucible.map','divideandconquer.map','battleground.map']
        self.map_handler = MapHandler()
        map_setup = self.setup_map()
        test_map, self.mapfile, self.start, self.end = map_setup
        d = dijkstra.Dijkstra(test_map,True)
        d_res = d.run_dijkstra()
        self.result = d_res
        self.length = len(d.route)

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
    
    def test_astar_result(self):
        test_map = self.reset_map(self.mapfile, self.start, self.end)
        a = astar.A_star(test_map,True)
        a_res = a.run_a_star()
        a_len = len(a.route)
        self.assertEqual(a_res,self.result)
        self.assertEqual(a_len,self.length)

    def test_jps_result(self):
        test_map = self.reset_map(self.mapfile, self.start, self.end)
        j = jps.Jump_point_search(test_map)
        j_res = j.run_jps()
        j_len = j.get_dist()
        self.assertEqual(j_res,self.result)
        self.assertEqual(j_len,self.length)