from pygame import draw, display



class Tile:
    size = 20

    def __init__(self, x, y, blocked = False):
        self.x = x
        self.y = y
        self.blocked = blocked
        
    def draw_tile(self,screen,c):
        if type(c) == int and c<=225 and c>=0:
            color = (c,c,c)
        elif type(c) == tuple:
            color = c
        else:
            color = (0,0,0)
        draw.rect(screen,color,(self.x*self.size, self.y*self.size, self.size, self.size))
        
    def __str__(self) -> str:
        return f'({self.x},{self.y},{self.blocked})'

class Grid:
    def __init__(self,width,height):
        """Grid
        
        Args:
            width (int): width in grid tiles
            height (int): height in grid tiles
        """
        self.w = width
        self.h = height        
        self.grid = [[Tile(i,j) for j in range(height)] for i in range(width)]


    
    def change_tile_state(self,x,y):
        self.grid[x][y].blocked = not self.grid[x][y].blocked

    def block_tile(self,x,y):
        self.grid[x][y].blocked = True

    def unblock_tile(self,x,y):
        self.grid[x][y].blocked = False

    def draw_grid(self,screen):
        for i in range(self.w):
            for j in range(self.h):
                if self.grid[i][j].blocked:
                    self.grid[i][j].draw_tile(screen,0)
                else:
                    self.grid[i][j].draw_tile(screen,225)
        display.update()
    
    def draw_test_gradient_grid(self,screen):
        shade = 0
        for i in range(self.w):
            for j in range(self.h):
                self.grid[i][j] = Tile(i,j)
                self.grid[i][j].draw_tile(screen,shade)
                shade += 1
                if shade >= 225:
                    shade = 0
        display.update()

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