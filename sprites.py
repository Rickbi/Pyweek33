import pygame

class Button:
    def __init__(self, text, cx, cy, font_size) -> None:
        font = pygame.font.match_font('consolas')
        self.font = pygame.font.Font(font, font_size)
        self.text_surf = self.font.render(text, True, (255,255,255))
        self.rect = self.text_surf.get_rect(center = (cx, cy))
        self.border_rect = pygame.Rect(0,0,self.rect.w + 10, self.rect.h + 10)
        self.border_rect.center = self.rect.center
        self.text = text
    
    def draw(self, screen, color_border):
        pygame.draw.rect(screen, (55,55,55), self.rect, 0)
        screen.blit(self.text_surf, self.rect)
        pygame.draw.rect(screen, color_border, self.border_rect, 5)

class Sprite(pygame.sprite.Sprite):
    def __init__(self, nx, ny, pos_x, pos_y, value, value_on, movable, image) -> None:
        super().__init__()
        self.rect = pygame.Rect(pos_x*nx, pos_y*ny, nx, ny)
        self.image = image
        self.pos_grid = (pos_x, pos_y)
        self.movable = movable
        self.value = value
        self.value_on = value_on
