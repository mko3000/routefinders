import pygame
from grid import Tile,Grid
from dijkstra import Dijkstra
from astar import A_star
from jps import Jump_point_search
from map_handler import MapHandler

class Gui:
    def __init__(self, grid = None, init_screen_width = 800, grid_width = 30, grid_height = 30):
        self.framerate = 20
        self.footer_height = 100
        if grid:
            self.grid = grid
            grid_width = self.grid.w  
            grid_height = self.grid.h
            Tile.size = init_screen_width//grid_width
            self.screen_width = grid_width*Tile.size
            self.screen_height = grid_height*Tile.size + self.footer_height           
        else:
            Tile.size = init_screen_width//grid_width
            self.screen_width = grid_width*Tile.size
            self.screen_height = grid_height*Tile.size + self.footer_height
            self.grid = Grid(grid_width,grid_height)
        self.screen = None

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

    def draw_footer(self):
        Font=pygame.font.SysFont('courier',  int(self.footer_height/3))
        bg_color = (66, 66, 66)
        pygame.draw.rect(self.screen, bg_color,(0, self.screen_height - self.footer_height, self.screen_width, self.footer_height))
        texts = Font.render((f'Dijkstra: "d", A*: "a", JPS: "j"'),False,(225,225,225))
        self.screen.blit(texts,(20, self.screen_height - 0.9*self.footer_height))

    def main(self):
        pygame.init()
        running = True
        routefinding_started = False
        pygame.time.Clock().tick(self.framerate)
        Font=pygame.font.SysFont('courier',  int(Tile.size/2))
        Font2 = pygame.font.SysFont('courier',  int(self.footer_height/3))
        running_text = Font2.render((f'running...'),False,(225,225,225))
        setting_up_text = Font2.render((f'setting up...'),False,(225,225,225))
        
        start_press_delay = self.framerate
        
        while running:
            
            keys = pygame.key.get_pressed()
            self.screen.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    print("\nquitting\n")        

            self.grid.draw_grid(self.screen)
            self.draw_footer()
            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                x, y = self.get_grid_tile_from_screen_pos(pos)
                self.grid.block_tile(x, y)
            
            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                x, y = self.get_grid_tile_from_screen_pos(pos)
                self.grid.unblock_tile(x, y)
            
            reset_key_pressed = keys[pygame.K_r]
            if reset_key_pressed:
                print("reset")
                self.grid.reset_tiles()
                self.grid.draw_grid(self.screen)

            d_start_key_pressed = keys[pygame.K_d]
            a_start_key_pressed = keys[pygame.K_a]
            j_start_key_pressed = keys[pygame.K_j]
            if (d_start_key_pressed or a_start_key_pressed or j_start_key_pressed) and start_press_delay > self.framerate:
                routefinding_started = True
                start_press_delay = 0
                #self.grid.reset_tiles()
                jps_dist = 0
                self.screen.blit(setting_up_text,(20, self.screen_height - 0.5*self.footer_height))
                if d_start_key_pressed:
                    routefinder = Dijkstra(self.grid, allow_diagonal=True)
                    self.screen.blit(running_text,(20, self.screen_height - 0.5*self.footer_height))
                    result = routefinder.run_dijkstra()
                if a_start_key_pressed:
                    routefinder = A_star(self.grid, allow_diagonal=True)
                    self.screen.blit(running_text,(20, self.screen_height - 0.5*self.footer_height))
                    result = routefinder.run_a_star()
                if j_start_key_pressed:
                    routefinder = Jump_point_search(self.grid)
                    self.screen.blit(running_text,(20, self.screen_height - 0.5*self.footer_height))
                    result = routefinder.run_jps()
                    jps_dist = routefinder.get_dist()
                print(f'found route: {result}\ntiles visited: {len(routefinder.order)}\nroute length: {len(routefinder.route)}/{jps_dist}\n')
            if routefinding_started:
                for tile in routefinder.order:
                    tile.draw_tile(self.screen,(225,0,225))
                for tile in routefinder.route:
                    tile.draw_tile(self.screen,(225,225,0)) 
                if len(routefinder.order) < 1000:
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
    berlin = True
    mh = MapHandler()
    if berlin:
        test_map = mh.load_movingai_map('movingai-maps/','Berlin_0_256.map')
        test_map.set_start(198,146)
        test_map.set_end(54,67)
        # test_map.set_random_start()
        # test_map.set_random_end()
        ui = Gui(grid=test_map, init_screen_width=2000)
    else:
        test_map = mh.load_map("s3")
        test_map.set_start(0,test_map.h-1)
        test_map.set_end(test_map.w-1,0)
        ui = Gui(grid=test_map, init_screen_width=800)

    grid = ui.start()
    print(grid)

