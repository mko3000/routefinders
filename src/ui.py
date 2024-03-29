import pygame
from grid import Tile,Grid
import algorithms

class Ui:
    def __init__(self, init_screen_width = 800, grid_width = 30, grid_height = 30):
        self.framerate = 20
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

    def quit_condition(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    
    def main(self):
        pygame.init()
        running = True
        started = False
        pygame.time.Clock().tick(self.framerate)
        Font=pygame.font.SysFont('timesnewroman',  20)
        
        start_press_delay = self.framerate
        d=[[],[],0]
        route = []
        self.grid.set_end(5,7)

        count = 0
        
        while running:
            # count += 1
            # if count >= 100:
            #     print(".")
            #     count = 0
            
            keys = pygame.key.get_pressed()
            self.screen.fill((255, 255, 255))
            

            self.quit_condition()            

            self.grid.draw_grid(self.screen)

            # test_text = Font.render((f'{count}'),False,(225,225,225),(0,0,0))
            # self.screen.blit(test_text,(self.screen_width/2,self.screen_height/2))
            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                x, y = self.get_grid_tile_from_screen_pos(pos)
                self.grid.block_tile(x, y)
            
            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                x, y = self.get_grid_tile_from_screen_pos(pos)
                self.grid.unblock_tile(x, y)
            
            start_key_pressed = keys[pygame.K_SPACE]
            if start_key_pressed and start_press_delay > self.framerate:
                started = True
                start_press_delay = 0
                [[tile.update_neighbors(self.grid)for tile in row] for row in self.grid.grid]
                dijk = algorithms.Dijkstra(self.grid,self.screen,(225,0,225))
                d = dijk.run_dijkstra()
                if d:
                    route = dijk.get_route()
                #d = algorithms.dijkstra(self.grid,self.screen,(225,0,225))
            if start_press_delay <= self.framerate + 1:
                start_press_delay += 1
            if started:
                if d:
                    for tile in d[1]:
                        if d[1][tile]:
                            tile.draw_tile(self.screen,(225,0,225))
                    for tile in route:
                        tile.draw_tile(self.screen,(225,225,0))
                    for tile in d[0]:
                        no = Font.render((f'{d[0].index(tile)}'),False,(225,225,225),(0,0,0))
                        self.screen.blit(no,(tile.x*Tile.size,tile.y*Tile.size))
                    self.grid.draw_end_and_start(self.screen)

            pygame.display.update()
            pygame.time.Clock().tick(self.framerate)

        pygame.quit()
        print(self.grid)


if __name__ == "__main__":
    ui = Ui(400, 10, 15)
    ui.start()