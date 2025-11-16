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
screen = pygame.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


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