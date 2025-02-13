from dijkstra import Dijkstra
from astar import A_star
from jps import Jump_point_search
from time import time
from map_handler import MapHandler
import random
import cProfile
import re
from rich import print
from rich.table import Table


class Comparison:
    def __init__(self) -> None:
        self.path = 'movingai-maps/'
        self.maps = ['Berlin_0_256.map',"Denver_0_256.map",'Sydney_2_512.map','Paris_2_512.map','NewYork_1_256.map','thecrucible.map','divideandconquer.map','battleground.map']
        self.map_handler = MapHandler()

    def setup_map(self):
        """
        Selects a random map with random start and end locations.
        """
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
        print()
        print(f"[bold]Map:[/bold] [bold yellow]{mapfile}[/bold yellow]")
        print(f"[bold]Start:[/bold] ({start.x},{start.y}), [bold]End:[/bold] ({end.x},{end.y})")

        jps = Jump_point_search(test_map)
        s = time()
        jps_result = jps.run_jps()
        e = time()
        jps_time = round(e-s,6)
        jps_visited = len(jps.order)
        jps_len = jps.get_dist()

        test_map = self.reset_map(mapfile, start, end)
        astar = A_star(test_map, allow_diagonal=True)
        s = time()
        astar_result = astar.run_a_star()
        e = time()
        astar_time = round(e-s,6)
        astar_visited = len(astar.order)
        astar_len = len(astar.route)

        test_map = self.reset_map(mapfile, start, end)
        dijkstra = Dijkstra(test_map, allow_diagonal=True)
        s = time()
        dijkstra_result = dijkstra.run_dijkstra()
        e = time()
        dijkstra_time = round(e-s,6)
        dijkstra_visited = len(dijkstra.order)
        dijkstra_len = len(dijkstra.route)


        # ChatGPT 4o was used to help with the table formating
        table = Table(show_header=True, header_style="bold magenta")

        table.add_column("Algorithm", style="bold cyan")
        table.add_column("Found", justify="center")
        table.add_column("Tiles Visited", justify="right")
        table.add_column("Route Length", justify="right")
        table.add_column("Time (s)", justify="right")

        table.add_row("JPS", str(jps_result), str(jps_visited), str(jps_len), str(jps_time))
        table.add_row("ASTAR", str(astar_result), str(astar_visited), str(astar_len), str(astar_time))
        table.add_row("DIJKSTRA", str(dijkstra_result), str(dijkstra_visited), str(dijkstra_len), str(dijkstra_time))

        print(table)


if __name__ == "__main__":
    comp = Comparison()
    comp.run_algorithms()


