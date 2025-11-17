#import module
import pygame

#importing pygame.locals for easy access to key coords
#flake8 and blk standards

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

#init game
pygame.init()

#def constants for screen width and height
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600

#Create screen obj
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


#keep main loop running
running = True

#Main loop 
while running:
    #check all events in queue
    for event in pygame.event.get():
        #keypress?
        if event.type == KEYDOWN:
            #ESC key? Stop loop
            if event.key == K_ESCAPE:
                running = False

        #Did the user click the close window button? STOP
        elif event.type == QUIT:
            running = False

    #fill screen with white
    screen.fill((255, 255, 255))

    #Surface with a tuple containing LxW
    surf = pygame.Surface((50, 50))

    # #give surface color to separate it from BG
    surf.fill((0, 0, 0))
    rect = surf.get_rect()

    # #blitting surface onto another surface for visability 
    screen.blit(surf, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    pygame.display.flip()