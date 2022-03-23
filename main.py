import pygame
from pygame.locals import *

from map import Map

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
    #main()
    map = Map(500,500, 50, 50)
    map.main()