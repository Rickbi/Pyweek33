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

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.scene = pygame.Surface((width, height))
        self.clock = pygame.time.Clock()
        self.fps = 60
        font = pygame.font.match_font('consolas')
        self.font = pygame.font.Font(font, 50)

        self.t1 = time.time()
        self.block_select = 0
        self.block_type = [(0,0,0), (255,0,0), (0,255,0), (0,0,255), (255,255,255), (255,0,255), (255,255,0)]

        self.level = 1
        self.last_level = 1
        self.reset()

        self.save_map_slot = 0
              
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

    def add_sprite(self, value, x, y):
        if value == 2:
            self.player.add(Sprite(self.nx, self.ny, x, y, 2, 0, movable = [0,4,5], color = (255,0,0)))
        elif value == 3:
            self.twin.add(Sprite(self.nx, self.ny, x, y, 3, 0, movable = [0,4,5], color = (100,255,100)))
        elif value == 4:
            self.player_door.add(Sprite(self.nx, self.ny, x, y, 4, 0, color = (255,255,255)))
        elif value == 5:
            self.twin_door.add(Sprite(self.nx, self.ny, x, y, 5, 0, color = (255,0,255)))
        elif value == 6:
            self.rocks.add(Sprite(self.nx, self.ny, x, y, 6, 0, movable = [0,4,5], color = (255,255,0)))

    def make_level(self):
        self.player = pygame.sprite.GroupSingle()
        self.twin = pygame.sprite.GroupSingle()
        self.player_door = pygame.sprite.GroupSingle()
        self.twin_door = pygame.sprite.GroupSingle()
        self.rocks = pygame.sprite.Group()
        for y, line in enumerate(self.lvl):
            for x, value in enumerate(line):
                self.add_sprite(value, x, y)

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
    
    def draw_level(self):
        for y, col in enumerate(self.lvl):
            for x, row in enumerate(col):
                if row == 1:
                    color = (255,0,0)
                else:
                    color = (0,0,0)
                rect = ((x*self.nx, y*self.ny),(self.nx, self.ny))
                pygame.draw.rect(self.scene, color, rect, 0)
    
    def get_pos_grid(self, pos):
        ix = pos[0]//self.nx
        iy = pos[1]//self.ny
        return (ix, iy)

    def draw_square(self):
        m_pos = pygame.mouse.get_pos()
        i_pos = self.get_pos_grid(m_pos)
        rect = ((self.nx*i_pos[0], self.ny*i_pos[1]),(self.nx,self.ny))
        pygame.draw.rect(self.screen, self.block_type[self.block_select], rect, 5)

    def show_fps(self):
        dt = time.time() - self.t1
        self.t1 = time.time()
        if dt != 0: self.write(f'{int(1/dt)}', (0,0))
    
    def check_if_won(self):
        cond_1 = self.player.sprites()[0].value_on == 4
        cond_2 = self.twin.sprites()[0].value_on == 5
        return cond_1 and cond_2

    def only_move(self, sprite, new_pos_x, new_pos_y):
        cond_1 = 0 <= new_pos_x < len(self.lvl[0]) and 0 <= new_pos_y < len(self.lvl)
        cond_2 = self.lvl[new_pos_y][new_pos_x] in sprite.movable
        
        if cond_1 and cond_2:
            self.lvl[sprite.pos_grid[1]][sprite.pos_grid[0]] = sprite.value_on
            sprite.value_on = self.lvl[new_pos_y][new_pos_x]
            self.lvl[new_pos_y][new_pos_x] = sprite.value
            new_x = new_pos_x*self.nx
            new_y = new_pos_y*self.ny
            sprite.pos_grid = (new_pos_x, new_pos_y)
            sprite.rect.x = new_x
            sprite.rect.y = new_y
            return True
        return False

    def move_sprite(self, sprite, dx = 0, dy = 0):
        new_pos_x = sprite.pos_grid[0] + dx
        new_pos_y = sprite.pos_grid[1] + dy

        if not self.only_move(sprite, new_pos_x, new_pos_y):            
            if self.lvl[new_pos_y][new_pos_x] == 6:
                for rock in self.rocks.sprites():
                    if rock.pos_grid == (new_pos_x, new_pos_y):
                        #self.move_sprite(rock, dx, dy)
                        self.only_move(rock, new_pos_x + dx, new_pos_y + dy)
                        self.only_move(sprite, new_pos_x, new_pos_y)

    def reset(self):
        self.lvl = self.load_level(f'lvl_{self.level}')
        self.make_level()
        self.draw_level()

    def main_menu(self):
        run = True
        buttons = [Button('Play', self.width//2, 100),
                   Button('Reset Level', self.width//2, 250),
                   Button('Make Level', self.width//2, 400),
                   Button('Quit Game', self.width//2, 550)]

        while run:
            if pygame.event.get(QUIT):
                run = False
            for event in pygame.event.get(MOUSEBUTTONUP):
                if event.button == 1:
                    for button in buttons:
                        if pygame.Rect.collidepoint(button.rect, event.pos[0], event.pos[1]):
                            if button.text == 'Play':
                                self.game()
                            elif button.text == 'Make Level':
                                self.level = 0
                                self.reset()
                                self.map_maker()
                                #self.save_level('lvl_10')
                                self.level = 10
                            elif button.text == 'Reset Level':
                                self.reset()
                                self.game()
                            elif button.text == 'Quit Game':
                                run = False

            self.screen.fill((0,0,10))
            pos_m = pygame.mouse.get_pos()
            for button in buttons:
                if pygame.Rect.collidepoint(button.rect, pos_m[0], pos_m[1]):
                    button.draw(self.screen, (255,0,0))
                else:
                    button.draw(self.screen, (0,0,255))

            self.show_fps()

            pygame.display.flip()
            self.clock.tick(self.fps)
        
        pygame.quit()

    def win_scene(self):
        run = True
        while run:
            if pygame.event.get(QUIT):
                run = False
            for event in pygame.event.get(KEYUP):
                run = False
            for event in pygame.event.get(MOUSEBUTTONUP):
                if event.button == 1 or event.button == 3:
                    run = False

            self.screen.fill((0,0,50))
            self.write('Congratulations, you finish all the levels.', (100,100))
            self.write('Thanks for Playing', (100,300))
            self.show_fps()

            pygame.display.flip()
            self.clock.tick(self.fps)

    def game(self):
        run = True
        won = False
        self.draw_level()
        while run:
            if pygame.event.get(QUIT):
                run = False
            for event in pygame.event.get(KEYUP):
                if event.key == K_e:
                    if self.check_if_won():
                        if self.level == self.last_level:
                            run = False
                            won = True
                        else:
                            self.level += 1
                            self.reset()
                elif event.key == K_ESCAPE:
                    run = False
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
            
            self.player_door.draw(self.screen)
            self.twin_door.draw(self.screen)
            self.player.draw(self.screen)
            self.twin.draw(self.screen)
            self.rocks.draw(self.screen)

            self.show_fps()
            pygame.display.flip()
            self.clock.tick(self.fps)
        
        if won:
            self.win_scene()

    def map_maker(self):
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
                        if event.button == 1:
                            self.add_sprite(self.block_select, i_pos[0], i_pos[1])
                elif event.button == 4:
                    self.block_select = (self.block_select + 1)%len(self.block_type)
                elif event.button == 5:
                    self.block_select = (self.block_select - 1)%len(self.block_type)
            for event in pygame.event.get(KEYUP):
                if event.key == K_e:
                    if self.check_if_won():
                        run = False
                elif event.key == K_ESCAPE:
                    run = False
                elif event.key == K_SPACE:
                    self.save_level(f'lvl_{10 + self.save_map_slot}')
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
            self.draw()
            self.screen.blit(self.scene, (0,0))
            self.draw_square()

            #self.player_door.draw(self.screen)
            #self.twin_door.draw(self.screen)
            #self.player.draw(self.screen)
            #self.twin.draw(self.screen)
            #self.rocks.draw(self.screen)
            self.show_fps()
            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    map = Map(1440,810, 45, 45)
    map.main_menu()