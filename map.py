import pygame
from pygame.locals import *
import time, os
from sprites import *

class Map:
    def __init__(self, width, height, nx, ny) -> None:
        self.width = width
        self.height = height
        self.nx = nx
        self.ny = ny

        self.t1 = time.time()
        self.block_select = 0
        self.block_type = [(0,0,0), (255,0,0), (0,255,0), (0,0,255), (255,255,255)]

        self.lvl = self.load_level('test')
        self.save_map_slot = 0

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.fps = 60
        font = pygame.font.match_font('consolas')
        self.font = pygame.font.Font(font, 50)
        self.scene = pygame.Surface((width, height))
        self.draw()

        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player(nx, ny, 1,1))
        self.twin = pygame.sprite.GroupSingle()
        self.twin.add(Player(nx, ny, 30,16))
        

    def load_level(self, name):
        path = os.path.join('levels', f'{name}.csv')
        with open(path, 'r') as f:
            data = f.read()
            lines = data.split('\n')
            lvl = []
            for line in lines:
                lvl.append([int(v) for v in line.split(',') if v != ''])
            lvl.remove([])
        return lvl

    def save_level(self, name):
        path = os.path.join('levels', f'{name}.csv')
        with open(path, 'w') as f:
            for line in self.lvl:
                f.write(','.join([str(v) for v in line]))
                f.write('\n')
        print(f'File saved: {name}.csv')

    def write(self, text, pos):
        text_surf = self.font.render(text, True, (255,255,255))
        self.screen.blit(text_surf, pos)

    def draw(self):
        self.scene.fill((100,100,100))
        for y, col in enumerate(self.lvl):
            for x, row in enumerate(col):
                color = self.block_type[self.lvl[y][x]]
                rect = ((x*self.nx, y*self.ny),(self.nx, self.ny))
                pygame.draw.rect(self.scene, color, rect, 5)
    
    def get_pos_grid(self, pos):
        ix = pos[0]//self.nx
        iy = pos[1]//self.ny
        return (ix, iy)

    def draw_square(self):
        m_pos = pygame.mouse.get_pos()
        i_pos = self.get_pos_grid(m_pos)
        rect = ((self.nx*i_pos[0], self.ny*i_pos[1]),(self.nx,self.ny))
        pygame.draw.rect(self.screen, self.block_type[self.block_select], rect, 5)
        #self.write(f'{i_pos}', (0,200))

    def show_fps(self):
        dt = time.time() - self.t1
        self.t1 = time.time()
        if dt != 0: self.write(f'{int(1/dt)}', (0,0))

    def move_sprite(self, sprite, dx = 0, dy = 0):
        new_pos_x = sprite.pos_grid[0] + dx
        new_pos_y = sprite.pos_grid[1] + dy

        cond_1 = 0 <= new_pos_x < len(self.lvl[0]) and 0 <= new_pos_y < len(self.lvl)
        cond_2 = self.lvl[new_pos_y][new_pos_x] == 0
        
        if cond_1 and cond_2:
            self.lvl[new_pos_y][new_pos_x] = 2
            self.lvl[sprite.pos_grid[1]][sprite.pos_grid[0]] = 0
            new_x = new_pos_x*self.nx
            new_y = new_pos_y*self.ny
            sprite.pos_grid = (new_pos_x, new_pos_y)
            sprite.rect.x = new_x
            sprite.rect.y = new_y

    def main(self):
        run = True
        while run:
            if pygame.event.get(QUIT):
                run = False
            for event in pygame.event.get(MOUSEBUTTONUP):
                if event.button == 1 or event.button == 3:
                    pos = pygame.mouse.get_pos()
                    i_pos = self.get_pos_grid(pos)
                    if i_pos[0] < len(self.lvl[0]) and i_pos[1] < len(self.lvl):
                        self.lvl[i_pos[1]][i_pos[0]] = self.block_select if event.button == 1 else 0
                        self.draw()
                elif event.button == 4:
                    self.block_select = (self.block_select + 1)%len(self.block_type)
                elif event.button == 5:
                    self.block_select = (self.block_select - 1)%len(self.block_type)
            for event in pygame.event.get(KEYUP):
                if event.key == K_m:
                    self.save_level(f'Test_level_{self.save_map_slot}')
                    self.save_map_slot += 1
            for event in pygame.event.get(KEYDOWN):
                if event.key == K_d or event.key == K_RIGHT:
                    self.move_sprite(self.player.sprites()[0], dx = 1)
                    self.move_sprite(self.twin.sprites()[0], dx = -1)
                elif event.key == K_a or event.key == K_LEFT:
                    self.move_sprite(self.player.sprites()[0], dx = -1)
                    self.move_sprite(self.twin.sprites()[0], dx = 1)
                elif event.key == K_w or event.key == K_UP:
                    self.move_sprite(self.player.sprites()[0], dy = -1)
                    self.move_sprite(self.twin.sprites()[0], dy = 1)
                elif event.key == K_s or event.key == K_DOWN:
                    self.move_sprite(self.player.sprites()[0], dy = 1)
                    self.move_sprite(self.twin.sprites()[0], dy = -1)

            self.screen.fill((100,100,100))
            self.screen.blit(self.scene, (0,0))
            self.draw_square()
            self.player.draw(self.screen)
            self.twin.draw(self.screen)
            #self.show_fps()
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()


if __name__ == '__main__':
    map = Map(1440,810, 45, 45)
    map.main()