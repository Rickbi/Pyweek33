import pygame
from pygame.locals import *
import time, os

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

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.fps = 60
        font = pygame.font.match_font('consolas')
        self.font = pygame.font.Font(font, 50)
        self.scene = pygame.Surface((width, height))
        self.draw()

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
    
    def draw_square(self):
        m_pos = pygame.mouse.get_pos()
        ix = m_pos[0]//self.nx
        iy = m_pos[1]//self.ny
        x = self.nx*ix
        y = self.ny*iy
        rect = ((x, y),(self.nx,self.ny))
        pygame.draw.rect(self.screen, self.block_type[self.block_select], rect, 5)
        self.write(f'{ix, iy}', (0,200))

    def show_fps(self):
        dt = time.time() - self.t1
        self.t1 = time.time()
        if dt != 0: self.write(f'{int(1/dt)}', (0,0))

    def main(self):
        run = True
        while run:
            if pygame.event.get(QUIT):
                run = False
            for event in pygame.event.get(MOUSEWHEEL):
                self.block_select = (self.block_select + event.y)%len(self.block_type)
                #print(self.block_select)
            self.screen.fill((100,100,100))
            self.screen.blit(self.scene, (0,0))
            self.draw_square()
            self.show_fps()
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()


if __name__ == '__main__':
    map = Map(1000,500, 50, 50)
    map.main()