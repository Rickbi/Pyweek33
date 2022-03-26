import pygame
import os

pygame.init()
pygame.display.set_mode((500,500))

name = 'twin'
path = os.path.join('assets', f'{name}.png')
save_path = os.path.join('assets', f'{name}_alpha.png')
img = pygame.image.load(path).convert_alpha()
img.set_colorkey((255,255,255))
new_img = img.copy()
new_img.set_alpha(0)
new_img.blit(img, (0,0))

pygame.image.save(new_img, save_path)

pygame.quit()