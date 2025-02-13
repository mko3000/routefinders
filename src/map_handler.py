import json
import random
from grid import Grid

class MapHandler:
    """
    A class for saving and loading maps using a json file for storage.
    """
    def __init__(self, filepath='maps.json'):
        self.filepath = filepath
        self.loaded_map = None
        self.movingaimaps = ['Berlin_0_256.map',"Denver_0_256.map",'Sydney_2_512.map','Paris_2_512.map','NewYork_1_256.map','thecrucible.map','divideandconquer.map','battleground.map']

    def save_map(self, grid: Grid, name: str):
        if name in self.list_maps():
            print(f'map named {name} already exists')
            return False
        dict_grid = []
        for row in grid.grid:
            dict_row = []
            for tile in row:
                tile_obj = {"x":tile.x, "y":tile.y, "blocked":tile.blocked}
                dict_row.append(tile_obj)
            dict_grid.append(dict_row)
        result_dict = {"name": name, "layout": dict_grid}
        with open(self.filepath, "r+") as f:
            file_data = json.load(f)
            file_data["maps"].append(result_dict)
            f.seek(0)
            json.dump(file_data, f, indent=4)
            return True

    def list_maps(self):
        with open(self.filepath, "r") as f:
            map_data = json.load(f)
        map_names = []
        for m in map_data["maps"]:
            map_names.append(m["name"])
        map_names += self.movingaimaps
        return map_names

    def find_map(self, name):
        with open(self.filepath, "r") as f:
            map_data = json.load(f)
        for m in map_data["maps"]:
            if m["name"] == name:
                return m["layout"]
        return False

    def load_map(self, name):
        if name in self.movingaimaps:
            grid = self.load_movingai_map('movingai-maps/',name)
            grid.set_random_start()
            grid.set_random_end()
            return grid
        layout = self.find_map(name)
        if not layout:
            print(f'map with the name {name} not found')
            return False
        print(f'rows: {len(layout)}, columns: {len(layout[0])}')
        grid = Grid(len(layout[0]), len(layout))
        for row in layout:
            for tile in row:
                if tile.get("blocked", False):
                    grid.block_tile(tile["x"], tile["y"])
        self.loaded_map = name
        return grid
    
    def reload_map(self):
        layout = self.find_map(self.loaded_map)
        grid = Grid(len(layout[0]), len(layout))
        for row in layout:
            for tile in row:
                if tile.get("blocked", False):
                    grid.block_tile(tile["x"], tile["y"])
        return grid

    def delete_map(self, name):
        #this method was generated with chat GTP
        with open(self.filepath, 'r') as f:
            map_data = json.load(f)
        map_data['maps'] = [map_ for map_ in map_data['maps'] if map_['name'] != name]
        with open(self.filepath, 'w') as f:
            json.dump(map_data, f, indent=4)

    def load_movingai_map(self, path, name):
        mapfile = f'{path}{name}'
        layout = open(mapfile,'r') #movingai-maps/street-map/Berlin_0_256.map
        ln = 0
        passable = ['.','G','S']
        grid = None
        while True:
            ln += 1
            line = layout.readline()
            if not line:
                return grid
            if ln == 2:
                h = int(line.split(" ")[1])
            if ln == 3:
                w = int(line.split(" ")[1])
            if ln == 4:
                grid = Grid(w,h)
            if ln > 4:
                y = ln - 5
                for x in range(w):
                    if line[x] not in passable:
                        grid.block_tile(x,y)





if __name__ == "__main__":
    mh = MapHandler()
    lmap = mh.load_movingai_map('movingai-maps/street-map/','Berlin_0_256.map')
    lmap.set_random_start()
    lmap.set_random_end()
    print(lmap)