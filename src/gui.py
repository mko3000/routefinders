import pygame
from grid import Tile,Grid
import algorithms
from map_handler import MapHandler

class Gui:
    def __init__(self, grid = None, init_screen_width = 800, grid_width = 30, grid_height = 30):
        self.framerate = 20
        if grid:
            self.grid = grid
            grid_width = self.grid.w  
            grid_height = self.grid.h
            Tile.size = init_screen_width//grid_width
            self.screen_width = grid_width*Tile.size
            self.screen_height = grid_height*Tile.size            
        else:
            Tile.size = init_screen_width//grid_width
            self.screen_width = grid_width*Tile.size
            self.screen_height = grid_height*Tile.size
            self.grid = Grid(grid_width,grid_height)
        self.grid.set_start(0,self.grid.h-1)
        self.grid.set_end(self.grid.w-1,0)
        self.screen = None

        # self.grid.set_start(1,grid_height-2)
        # self.grid.set_end(grid_width-2,1)
        # self.grid.set_start(5,2)
        # self.grid.set_end(25,15)

    def start(self):
        print("start")
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.main()
        return self.grid

    def get_grid_tile_from_screen_pos(self,pos):
        return pos[0]//Tile.size, pos[1]//Tile.size
    
    def draw_obstacle(self, tile:Tile):
        tile.blocked = True
        tile.draw_tile(self.screen,225)


    def main(self):
        pygame.init()
        running = True
        routefinding_started = False
        pygame.time.Clock().tick(self.framerate)
        Font=pygame.font.SysFont('timesnewroman',  int(Tile.size/2))
        
        start_press_delay = self.framerate
        
        while running:
            
            keys = pygame.key.get_pressed()
            self.screen.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    print("\nquitting\n")        

            self.grid.draw_grid(self.screen)
            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                x, y = self.get_grid_tile_from_screen_pos(pos)
                self.grid.block_tile(x, y)
            
            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                x, y = self.get_grid_tile_from_screen_pos(pos)
                self.grid.unblock_tile(x, y)
            

            d_start_key_pressed = keys[pygame.K_SPACE]
            a_start_key_pressed = keys[pygame.K_a]
            if (d_start_key_pressed or a_start_key_pressed) and start_press_delay > self.framerate:
                routefinding_started = True
                start_press_delay = 0
                self.grid.reset_tiles()
                self.grid.update_all_neighbors()
                if d_start_key_pressed:
                    routefinder = algorithms.Dijkstra(self.grid)
                    routefinder.run_dijkstra()
                if a_start_key_pressed:
                    routefinder = algorithms.A_star(self.grid)
                    routefinder.run_a_star()
            if routefinding_started:
                for tile in routefinder.order:
                    tile.draw_tile(self.screen,(225,0,225))
                for tile in routefinder.route:
                    tile.draw_tile(self.screen,(225,225,0)) 
                for tile in routefinder.order:                                           
                    no = Font.render((f'{routefinder.order.index(tile)}'),False,(225,225,225),(0,0,0))
                    self.screen.blit(no,(tile.x*Tile.size,tile.y*Tile.size))
                self.grid.draw_end_and_start(self.screen)

            if start_press_delay <= self.framerate + 1:
                start_press_delay += 1
            
            pygame.display.update()
            pygame.time.Clock().tick(self.framerate)

        pygame.quit()
        #print(self.grid)


if __name__ == "__main__":
    # ui = Gui(init_screen_width=800, grid_height=30, grid_width=30)
    # grid = ui.start()
    # print(grid)

    mh = MapHandler()
    dog_map = mh.load_map("dog")
    ui = Gui(grid=dog_map)
    grid = ui.start()
    print(grid)

