import json
from grid import Grid

class MapHandler:
    def __init__(self, filepath='maps.json'):
        self.filepath = filepath

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
        return map_names

    def find_map(self, name):
        with open(self.filepath, "r") as f:
            map_data = json.load(f)
        for m in map_data["maps"]:
            if m["name"] == name:
                return m["layout"]
        return False

    def load_map(self, name):
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
        return grid

    def delete_map(self, name):
        #this method was generated with chat GTP
        with open(self.filepath, 'r') as f:
            map_data = json.load(f)
        map_data['maps'] = [map_ for map_ in map_data['maps'] if map_['name'] != name]
        with open(self.filepath, 'w') as f:
            json.dump(map_data, f, indent=4)

