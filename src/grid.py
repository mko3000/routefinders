from pygame import draw, display



class Tile:
    size = 20

    def __init__(self, x, y, blocked = False):
        self.x = x
        self.y = y
        self.blocked = blocked
        self.neighbors = []
        self.visited = False
        
    def draw_tile(self,screen,c):
        if type(c) == int and c<=225 and c>=0:
            color = (c,c,c)
        elif type(c) == tuple:
            color = c
        else:
            color = (0,0,0)
        draw.rect(screen,color,(self.x*self.size, self.y*self.size, self.size, self.size))

    def update_neighbors(self, neighbors):
        if self.blocked:
            self.neighbors = []
        else:
            self.neighbors = neighbors
        
    def reset_tile(self):
        return Tile(self.x, self.y, self.blocked)
    
    def __str__(self) -> str:
        return f'[({self.x},{self.y}), b:{self.blocked}, n:{len(self.neighbors)}]'
    
    
class Dijkstra_tile(Tile):
    def __init__(self, x=None, y=None, blocked=None):
        super().__init__(x, y, blocked)
        self.dist = float("Inf")

    @classmethod
    def from_Tile(cls, tile: Tile):
        d_tile_obj = cls()
        for key, value in tile.__dict__.items():
            d_tile_obj.__dict__[key] = value
        return d_tile_obj    
    
    def __gt__(self,other):
        return self.dist > other.dist
    
    def __str__(self) -> str:
        return f'[({self.x},{self.y}), b:{self.blocked}, n:{len(self.neighbors)}, d:{self.dist}]'

class Astar_tile(Tile):
    def __init__(self, x=None, y=None, blocked=False):
        super().__init__(x, y, blocked)
        self.g_score = float("Inf")
        self.f_score = float("Inf")
    
    @classmethod
    def from_Tile(cls, tile: Tile):
        a_tile_obj = cls()
        for key, value in tile.__dict__.items():
            a_tile_obj.__dict__[key] = value
        return a_tile_obj  

    def __gt__(self,other):
        return self.f_score > other.f_score 


class JPS_tile(Tile):
    def __init__(self, x, y, blocked=False):
        super().__init__(x, y, blocked)
        self.natural_neighbors = []
    
    @classmethod
    def from_Tile(cls, tile: Tile):
        d_tile_obj = cls()
        for key, value in tile.__dict__.items():
            d_tile_obj.__dict__[key] = value
        return d_tile_obj   


class Grid:
    def __init__(self,width,height):
        """Grid
        
        Args:
            width (int): width in grid tiles
            height (int): height in grid tiles
        """
        self.w = width
        self.h = height        
        self.grid = [[Tile(x,y) for x in range(width)] for y in range(height)]
        self.start = self.get_tile(0,0)
        self.end = self.get_tile(width-1,height-1)
    
    def valid_coordinates(self,x,y):
        if x >= 0 and x < self.w and y >= 0 and y < self.h:
            return True
        return False
    
    def get_tile(self,x,y):
        if self.valid_coordinates(x,y): 
            return self.grid[y][x]
        return None
    
    def get_free_tile(self,x,y):
        if self.valid_coordinates(x,y) and not self.grid[y][x].blocked: 
            return self.grid[y][x]
        return None
    
    def set_tile(self,x,y,blocked = False):
        if self.valid_coordinates(x,y): 
            tile = Tile(x,y,blocked)
            self.grid[y][x] = tile
            return tile
        return None
    
    def change_tile_state(self,x,y):
        if self.valid_coordinates(x,y):
            self.grid[y][x].blocked = not self.grid[y][x].blocked

    def block_tile(self,x,y):
        if self.valid_coordinates(x,y):
            self.grid[y][x].blocked = True

    def unblock_tile(self,x,y):
        if self.valid_coordinates(x,y):
            self.grid[y][x].blocked = False

    def set_start(self,x,y):
        if self.valid_coordinates(x,y):
            self.start = self.get_tile(x,y)
    
    def set_end(self,x,y):
        if self.valid_coordinates(x,y):
            self.end = self.get_tile(x,y)

    def reset_tiles(self):
        [[tile.reset_tile() for tile in row] for row in self.grid]

    def update_all_neighbors(self, diagonal = False):
        for y in range(self.h):
            for x in range(self.w):
                tile = self.grid[y][x]
                if not tile.blocked:
                    neighbors = self.calculate_neighbors(x, y, diagonal)
                    tile.update_neighbors(neighbors)

    def calculate_neighbors(self, x, y, diagonal = False):
        neighbors = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        if not diagonal:
            directions = directions[:4]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.valid_coordinates(nx, ny) and not self.grid[ny][nx].blocked:
                neighbors.append(self.grid[ny][nx])
        return neighbors
    
    def draw_grid(self,screen):
        for y in range(self.h):
            for x in range(self.w):
                if self.grid[y][x].blocked:
                    self.grid[y][x].draw_tile(screen,0)
                else:
                    self.grid[y][x].draw_tile(screen,225)
        self.draw_end_and_start(screen)

    def draw_end_and_start(self,screen):
        self.start.draw_tile(screen,(0,225,0))
        self.end.draw_tile(screen,(225,0,0))

    def __str__(self) -> str:
        output = ""
        for i in range(self.h):
            row = ""
            for j in range(len(self.grid[i])):
                if self.grid[i][j].blocked:
                    row += "#"
                else:
                    row += "."
            output += f'{row}\n'
        return output
    
if __name__ == "__main__":
    pass