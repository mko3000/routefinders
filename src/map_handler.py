from grid import Tile, Grid
import json

def save_map(grid:Grid, name:str):    
    dict_grid = []
    for row in grid.grid:
        dict_row = []
        for tile in row:
            tile_dict = tile.__dict__           
            dict_row.append(tile_dict)
        dict_grid.append(dict_row)
    result_dict = {"name":name,"layout":dict_grid}
    with open("maps.json","r+") as f:
        file_data = json.load(f)
        file_data["maps"].append(result_dict)
        f.seek(0)
        json.dump(file_data, f, indent=4)

def list_maps():
    with open("maps.json","r") as f:
        map_data = json.load(f)
    for grid_map in map_data["maps"]:
        print(grid_map["name"])

def load_map(name):
    with open("maps.json","r") as f:
        map_data = json.load(f)
    for grid_map in map_data["maps"]:
        if grid_map["name"] == name:
            layout = grid_map["layout"]

    print(f'rows: {len(layout)}, columns: {len(layout[0])}')
    #grid = Grid()

    return layout

def delete_map():
    pass

if __name__ == "__main__":
    grid = Grid(10,8)
    grid.change_tile_state(2,2)
    grid.change_tile_state(2,3)
    for i in range(0,8):
        grid.change_tile_state(6,i)
    for i in range(0,5):
        grid.change_tile_state(i,7)
    grid.change_tile_state(6,4)
    print(grid)

    # save_map(grid,"testi_jee")

    # load_map("moi")

    list_maps()

    #l_map = load_map("testi_jee")
