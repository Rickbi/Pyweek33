import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, nx, ny, pos_x, pos_y) -> None:
        super().__init__()
        self.rect = pygame.Rect(pos_x*nx, pos_y*ny, nx, ny)
        self.image = pygame.Surface((nx,ny))
        self.image.fill((100,100,255))
        self.pos_grid = (pos_x, pos_y)


class Player(Sprite):
    def __init__(self, nx, ny, pos_x, pos_y) -> None:
        super().__init__(nx, ny, pos_x, pos_y)
    
    def move(self, dx = 0, dy = 0):
        self.rect.x += dx*self.rect.w
        self.rect.y += dy*self.rect.h