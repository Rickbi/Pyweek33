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
        self.mute = False

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.scene = pygame.Surface((width, height))
        self.clock = pygame.time.Clock()
        self.fps = 30
        font = pygame.font.match_font('consolas')
        self.font_size = min(width*40//1440, height*50//810)
        #print(font_size)
        self.font = pygame.font.Font(font, self.font_size)
        self.load_assets()
        self.load_story()
        try:
            self.load_sounds()
        except Exception as err:
            print('Error loading the sound')
            print(f'Error Name: {err}')
            self.mute = True

        self.t1 = time.time()
        self.block_select = 0
        self.block_type = [0]*9

        self.level = 1
        self.last_level = len(self.story)
        self.save_map_slot = self.last_level + 1
        self.reset()

    def load_sounds(self):
        self.sounds = {'rock':None,
                       'walk':None}

        for name in self.sounds:
            path = os.path.join('assets','sounds', f'{name}.wav')
            self.sounds[name] = pygame.mixer.Sound(path)
            if name == 'rock':
                self.sounds[name].set_volume(0.25)
            elif name == 'walk':
                self.sounds[name].set_volume(0.5)
        
        path = os.path.join('assets','sounds', 'music.wav')
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.25)

    def make_sound(self, sound):
        if not self.mute:
            self.sounds[sound].play()
    
    def play_music(self):
        if not self.mute:
            pygame.mixer.music.play(-1)

    def load_last_level_played(self):
        path = os.path.join('levels', 'save.txt')
        with open(path, 'r') as f:
            lvl = int(f.read())
        return lvl
    
    def save_last_level_played(self):
        path = os.path.join('levels', 'save.txt')
        with open(path, 'w') as f:
            f.write(f'{self.level}')

    def load_assets(self):
        self.images = {'floor' : None,
                       'wall'  : None,
                       'rock'  : None,
                       'player'  : None,
                       'twin'  : None,
                       'player_door'  : None,
                       'twin_door'  : None,
                       'rock_door_p'  : None,
                       'rock_door_t'  : None}
        for name in self.images:
            path = os.path.join('assets', f'{name}.png')
            img = pygame.image.load(path).convert_alpha()
            self.images[name] = pygame.transform.scale(img, (self.nx, self.ny))
        
        bgs = ['bg', 'bg_end', 'bg_menu']
        for name in bgs:
            path = os.path.join('assets', f'{name}.png')
            img = pygame.image.load(path).convert_alpha()
            self.images[name] = pygame.transform.scale(img, (self.width, self.height))

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

    def load_story(self):
        path = os.path.join('levels', 'story.txt')
        self.story = []
        with open(path, 'r') as f:
            text = f.read()
            for line in text.split('\n'):
                self.story.append(line.split('-'))

    def add_sprite(self, value, x, y):
        if value == 2:
            self.player.add(Sprite(self.nx, self.ny, x, y, 2, 0, [0,4,5], self.images['player']))
        elif value == 3:
            self.twin.add(Sprite(self.nx, self.ny, x, y, 3, 0, [0,4,5], self.images['twin']))
        elif value == 6:
            self.rocks.add(Sprite(self.nx, self.ny, x, y, 6, 0, [0,4,5], self.images['rock']))
        elif value == 7:
            self.rocks.add(Sprite(self.nx, self.ny, x, y, 6, 4, [0,4,5], self.images['rock']))
        elif value == 8:
            self.rocks.add(Sprite(self.nx, self.ny, x, y, 6, 5, [0,4,5], self.images['rock']))

    def make_level(self):
        self.player = pygame.sprite.GroupSingle()
        self.twin = pygame.sprite.GroupSingle()
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

    def get_image(self, value):
        if value == 0:
            return self.images['floor']
        elif value == 1:
            return self.images['wall']
        elif value == 2:
            return self.images['player']
        elif value == 3:
            return self.images['twin']
        elif value == 4:
            return self.images['player_door']
        elif value == 5:
            return self.images['twin_door']
        elif value == 7:
            return self.images['rock_door_p']
        elif value == 8:
            return self.images['rock_door_t']
        else:
            return self.images['rock']

    def draw(self):
        self.scene.fill((35,168,28))
        for y, col in enumerate(self.lvl):
            for x, row in enumerate(col):
                img = self.get_image(row)
                rect = img.get_rect(topleft = (x*self.nx, y*self.ny) )
                self.scene.blit(img, rect)
    
    def draw_level(self):
        for y, col in enumerate(self.lvl):
            for x, row in enumerate(col):
                if row == 1:
                    img = self.images['wall']
                elif row == 4:
                    img = self.images['player_door']
                elif row == 7:
                    img = self.images['player_door']
                    self.lvl[y][x] = 6
                elif row == 5:
                    img = self.images['twin_door']
                elif row == 8:
                    img = self.images['twin_door']
                    self.lvl[y][x] = 6
                else:
                    img = self.images['floor']
                
                pos = (x*self.nx, y*self.ny)
                self.scene.blit(img, pos)
    
    def get_pos_grid(self, pos):
        ix = pos[0]//self.nx
        iy = pos[1]//self.ny
        return (ix, iy)

    def draw_square(self):
        m_pos = pygame.mouse.get_pos()
        i_pos = self.get_pos_grid(m_pos)

        color = (0,0,0)
        img = self.get_image(self.block_select)
        rect = img.get_rect(topleft = (self.nx*i_pos[0], self.ny*i_pos[1]) )
        self.scene.blit(img, rect)
        pygame.draw.rect(self.scene, color, rect, 1)

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
        
        if cond_1 and self.lvl[new_pos_y][new_pos_x] in sprite.movable:
            self.lvl[sprite.pos_grid[1]][sprite.pos_grid[0]] = sprite.value_on
            sprite.value_on = self.lvl[new_pos_y][new_pos_x]
            self.lvl[new_pos_y][new_pos_x] = sprite.value
            new_x = new_pos_x*self.nx
            new_y = new_pos_y*self.ny
            sprite.pos_grid = (new_pos_x, new_pos_y)
            sprite.rect.x = new_x
            sprite.rect.y = new_y
            if sprite.value == 2:
                self.make_sound('walk')
            return True
        return False

    def move_sprite(self, sprite, dx = 0, dy = 0):
        new_pos_x = sprite.pos_grid[0] + dx
        new_pos_y = sprite.pos_grid[1] + dy
        cond_1 = 0 <= new_pos_x < len(self.lvl[0]) and 0 <= new_pos_y < len(self.lvl)

        if not self.only_move(sprite, new_pos_x, new_pos_y) and cond_1:
            if self.lvl[new_pos_y][new_pos_x] == 6:
                for rock in self.rocks.sprites():
                    if rock.pos_grid == (new_pos_x, new_pos_y):
                        #self.move_sprite(rock, dx, dy)
                        if self.only_move(rock, new_pos_x + dx, new_pos_y + dy):
                            self.make_sound('rock')
                        self.only_move(sprite, new_pos_x, new_pos_y)

    def reset(self):
        self.lvl = self.load_level(f'lvl_{self.level}')
        self.make_level()
        self.draw_level()

    def select_menu(self):
        run = True
        enter_b = False
        buttons = [Button('Back', self.width*200//1440, self.height*200//810, self.font_size)]
        level = self.load_last_level_played()

        for i in range(level):
            x = 200 + 250*(i//4)
            y = 350 + 100*(i%4)
            buttons.append(Button(f'lvl {1+i}', self.width*x//1440, self.height*y//810, self.font_size))

        while run:
            if pygame.event.get(QUIT):
                run = False
            for event in pygame.event.get(MOUSEBUTTONUP):
                if event.button == 1:
                    for button in buttons:
                        if pygame.Rect.collidepoint(button.rect, event.pos[0], event.pos[1]):
                            self.make_sound('rock')
                            if button.text == 'Back':
                                run = False
                            else:
                                return int(button.text.replace('lvl ', ''))

            self.screen.fill((0,0,10))
            self.screen.blit(self.images['bg_menu'], (0,0))
            pos_m = pygame.mouse.get_pos()
            s = 0
            for button in buttons:
                if pygame.Rect.collidepoint(button.rect, pos_m[0], pos_m[1]):
                    button.draw(self.screen, (255,0,0))
                    s += 1
                else:
                    button.draw(self.screen, (0,0,255))

            if s >= 1 and not enter_b:
                self.make_sound('walk')
                enter_b = True
            elif s == 0:
                enter_b = False

            #self.show_fps()
            pygame.display.flip()
            self.clock.tick(self.fps)

    def main_menu(self):
        run = True
        enter_b = False
        buttons = [Button('Play', self.width//2, self.height*100//810, self.font_size),
                   Button('Reset Level', self.width//2, self.height*250//810, self.font_size),
                   Button('Level Select', self.width//2, self.height*400//810, self.font_size),
                   Button('Make Level', self.width//2, self.height*550//810, self.font_size),
                   Button('Quit Game', self.width//2, self.height*700//810, self.font_size)]
        self.play_music()
        self.end_level_scene()
        while run:
            if pygame.event.get(QUIT):
                run = False
            for event in pygame.event.get(MOUSEBUTTONUP):
                if event.button == 1:
                    for button in buttons:
                        if pygame.Rect.collidepoint(button.rect, event.pos[0], event.pos[1]):
                            self.make_sound('rock')
                            if button.text == 'Play':
                                self.game()
                            elif button.text == 'Make Level':
                                self.level = 0
                                self.reset()
                                self.map_maker()
                                self.level = 1
                                self.reset()
                            elif button.text == 'Reset Level':
                                self.reset()
                                self.game()
                            elif button.text == 'Quit Game':
                                run = False
                            elif button.text == 'Level Select':
                                select = self.select_menu()
                                if select:
                                    self.level = select
                                    self.reset()
                                    self.game()

            self.screen.fill((0,0,10))
            self.screen.blit(self.images['bg_menu'], (0,0))
            pos_m = pygame.mouse.get_pos()
            s = 0
            for button in buttons:
                if pygame.Rect.collidepoint(button.rect, pos_m[0], pos_m[1]):
                    button.draw(self.screen, (255,0,0))
                    s += 1
                else:
                    button.draw(self.screen, (0,0,255))
            
            if s >= 1 and not enter_b:
                self.make_sound('walk')
                enter_b = True
            elif s == 0:
                enter_b = False

            #self.show_fps()

            pygame.display.flip()
            self.clock.tick(self.fps)
        
        pygame.quit()

    def win_scene(self):
        run = True
        while run:
            if pygame.event.get(QUIT):
                run = False
            for event in pygame.event.get(KEYDOWN):
                run = False
            for event in pygame.event.get(MOUSEBUTTONUP):
                if event.button == 1 or event.button == 3:
                    run = False

            self.screen.fill((0,0,50))
            self.screen.blit(self.images['bg_end'], (0,0))
            
            self.write('That does not matter now.', (self.width*100//1440,self.height*100//810))
            self.write('For me, he will always be my brother.', (self.width*100//1440,self.height*150//810))

            self.write('Congratulations, you finish all the levels.', (self.width*100//1440,self.height*300//810))
            self.write('Thanks for Playing', (self.width*100//1440,self.height*350//810))
            
            #self.show_fps()

            pygame.display.flip()
            self.clock.tick(self.fps)
    
    def end_level_scene(self):
        run = True
        while run:
            if pygame.event.get(QUIT):
                run = False
            for event in pygame.event.get(KEYDOWN):
                run = False
            for event in pygame.event.get(MOUSEBUTTONUP):
                if event.button == 1 or event.button == 3:
                    run = False

            self.screen.fill((0,0,50))
            self.screen.blit(self.images['bg'], (0,0))

            for i, line in enumerate(self.story[self.level - 1]):
                self.write(line, (self.width*100//1440, self.height*(100 + i*50)//810 ))
            
            #self.show_fps()

            pygame.display.flip()
            self.clock.tick(self.fps)

    def game(self):
        run = True
        won = False
        #self.draw_level()
        while run:
            if pygame.event.get(QUIT):
                run = False
            for event in pygame.event.get(KEYUP):
                if event.key == K_e or event.key == K_SPACE:
                    if self.check_if_won():
                        if self.level == self.last_level:
                            run = False
                            won = True
                        else:
                            self.level += 1
                            self.end_level_scene()
                            if self.load_last_level_played() < self.level:
                                self.save_last_level_played()
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

            # if self.check_if_won():
            #     if self.level == self.last_level:
            #         run = False
            #         won = True
            #     else:
            #         self.level += 1
            #         self.end_level_scene()
            #     if self.load_last_level_played() < self.level:
            #         self.save_last_level_played()
            #     self.reset()

            self.screen.fill((100,100,100))
            self.screen.blit(self.scene, (0,0))
            
            self.player.draw(self.screen)
            self.twin.draw(self.screen)
            self.rocks.draw(self.screen)

            #self.show_fps()
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
                if event.key == K_ESCAPE:
                    run = False
                elif event.key == K_SPACE:
                    self.save_level(f'lvl_{self.save_map_slot}')
                    self.save_map_slot += 1
                elif event.key == K_r:
                    self.level = self.save_map_slot - 1
                    self.reset()
            for event in pygame.event.get(KEYDOWN):
                lar_p = len(self.player.sprites())
                lar_t = len(self.twin.sprites())
                if event.key == K_d or event.key == K_RIGHT:
                    if lar_p > 0: self.move_sprite(self.player.sprites()[0], dx = 1)
                    if lar_t > 0: self.move_sprite(self.twin.sprites()[0], dx = -1)
                elif event.key == K_a or event.key == K_LEFT:
                    if lar_p > 0: self.move_sprite(self.player.sprites()[0], dx = -1)
                    if lar_t > 0: self.move_sprite(self.twin.sprites()[0], dx = 1)
                elif event.key == K_w or event.key == K_UP:
                    if lar_p > 0: self.move_sprite(self.player.sprites()[0], dy = -1)
                    if lar_t > 0: self.move_sprite(self.twin.sprites()[0], dy = 1)
                elif event.key == K_s or event.key == K_DOWN:
                    if lar_p > 0: self.move_sprite(self.player.sprites()[0], dy = 1)
                    if lar_t > 0: self.move_sprite(self.twin.sprites()[0], dy = -1)

            self.screen.fill((0,0,0))
            self.draw()
            self.draw_square()
            self.screen.blit(self.scene, (0,0))

            #self.show_fps()
            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    map = Map(1440,810, 70, 70)
    map.main_menu()