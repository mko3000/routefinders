from gui import Gui
from grid import Grid
from map_handler import MapHandler
import sys
import random
from dijkstra import Dijkstra
from astar import A_star
from jps import Jump_point_search
from time import time
from algorithm_tester import Comparison


class Ui:
    def __init__(self) -> None:
        pass

    def start(self):
        self.menu()

    def menu(self):
        while True:
            print("""
Select how you want to run your search algorithms:
1 draw custom map
2 load saved map
3 run algorithm comparison
q quit
                  """)
            user_input = input(">> ")
            match user_input:
                case "1":
                    self.start_gui()
                case "2":
                    self.load_map()
                case "3":
                    self.run_comparison()
                case "q":
                    self.quit_program()
                case _:
                    print("Unrecognized input - please try again.")
            

    def quit_program(self):
        print("quitting")
        sys.exit()

    def start_gui(self,m = None):
        if m == None:
            gui = Gui()
            grid = gui.start()
        else:
            gui = Gui(grid=m)
            grid = gui.start()
        self.run_ended(grid)

    def run_ended(self,grid):
        print("Run ended.")
        print("Map:")
        print(grid)
        print("do you want to save the map? (y/n)")
        user_input = input(">> ")
        match user_input:
            case "y":
                self.save_map(grid)
            case "n":
                return
            case _:
                print("Unrecognized input - please try again.")

    def save_map(self,grid):
        map_handler = MapHandler()
        saved = False
        while not saved:
            print("name your map. (cancel saving by pressing 'c')")
            map_name = input(">> ")
            if map_name == "c":
                break
            saved = map_handler.save_map(grid, map_name)

    def load_map(self):
        map_handler = MapHandler()
        loaded = False
        while not loaded:
            print("Available maps:")
            map_list = map_handler.list_maps()
            for m in map_list:
                print(m)
            print("Which map do you want to load? (cancel loading by pressing 'c')")
            map_name = input(">> ")
            if map_name == "c":
                break
            loaded = map_handler.load_map(map_name)
        if loaded:
            self.start_gui(loaded)

    def run_comparison(self):
        comp = Comparison()
        comp.run_algorithms()
        

if __name__ == "__main__":
    ui = Ui()
    ui.start()