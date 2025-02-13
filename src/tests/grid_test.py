import unittest
from grid import Grid, Tile

class TestTile(unittest.TestCase):
    def setUp(self):
        pass

    def test_creating_tile(self):
        tile = Tile(2,3)

        self.assertEqual(str(tile), "[(2,3), b:False, n:0]")

    def test_reset_tile(self):
        tile = Tile(2,4)
        tile.visited = True
        print(tile.__dict__)
        tile = tile.reset_tile()
        print(tile.__dict__)
        
        self.assertEqual(tile.neighbors,[])
        self.assertEqual(tile.visited, False)

class TestGrid():    
    def test_grid_initialization(self):
        grid = Grid(10, 10)
        assert grid.w == 10 and grid.h == 10
        assert isinstance(grid.get_tile(0, 0), Tile)

    def test_valid_coordinates(self):
        grid = Grid(5, 5)
        assert grid.valid_coordinates(0, 0)
        assert not grid.valid_coordinates(-1, 0)
        assert not grid.valid_coordinates(5, 5)

    def test_tile_blocked(self):
        grid = Grid(3, 3)
        grid.set_tile(1, 1, True)
        assert grid.get_tile(1, 1).blocked
        grid.unblock_tile(1,1)
        assert not grid.get_tile(1, 1).blocked
        grid.block_tile(1,1)
        assert grid.get_tile(1, 1).blocked

    def test_update_all_neighbors(self):
        grid = Grid(3, 3)
        grid.set_tile(1, 0, True)  # Block the tile at (1, 0)
        grid.update_all_neighbors()

        exp_neighbors = [grid.get_tile(0, 1), grid.get_tile(2, 1), grid.get_tile(1, 2)] 
        for n in exp_neighbors:
            assert n in grid.get_tile(1,1).neighbors
        assert grid.get_tile(1,0).neighbors == []


