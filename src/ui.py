import pygame
from grid import Tile,Grid

class Ui:
    def __init__(self, init_screen_width = 800, grid_width = 30, grid_height = 30):
        self.framerate = 60
        self.grid_widht = grid_width       
        self.grid_height = grid_height
        Tile.size = init_screen_width//grid_width
        self.screen_width = grid_width*Tile.size
        self.screen_height = grid_height*Tile.size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.grid = Grid(grid_width, grid_height)

    def start(self):
        print("start")
        testile = Tile(4,5)
        print(testile.x, testile.y, testile.size)
        print(self.screen_width,"x",self.screen_height)
        self.main()

    def get_grid_tile_from_screen_pos(self,pos):
        return pos[0]//Tile.size, pos[1]//Tile.size
    
    def draw_obstacle(self, tile:Tile):
        tile.blocked = True
        tile.draw_tile(self.screen,225)

    
    def main(self):
        running = True
        
        while running:
            self.screen.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.grid.draw_grid(self.screen)
            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                x, y = self.get_grid_tile_from_screen_pos(pos)
                self.grid.block_tile(x, y)
            
            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                x, y = self.get_grid_tile_from_screen_pos(pos)
                self.grid.unblock_tile(x, y)
            
            pygame.time.Clock().tick(self.framerate)

        pygame.quit()
        print(self.grid)


if __name__ == "__main__":
    ui = Ui(400, 10, 15)
    ui.start()