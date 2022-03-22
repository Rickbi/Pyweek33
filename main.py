import pygame
from pygame.locals import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((500,500))

    run = True
    while run:
        for event in pygame.event.get(QUIT):
            run = False
        
        screen.fill((0,0,0))
        
    pygame.quit()

if __name__ == '__main__':
    main()