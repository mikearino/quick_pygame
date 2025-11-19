# Import the pygame module
import pygame

#import random for rando numbers
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("jet.png")
        self.surf = pygame.transform.scale(self.surf, (60, 30))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
    
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (30, 20))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )          
        self.speed = random.randint(5, 20)

#Move sprite base on speed
#Remove sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

#def cloud object
#use an image
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        #Start position is random
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    #Move cloud basedd on a constant speed
    #remove cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

#set up for sound
pygame.mixer.init()

# Load and play background music
# Sound source: youtube.com
# License: 8-Bit March by Twin Musicom is 
# licensed under a Creative Commons Attribution 4.0 license. 
# https://creativecommons.org/licenses/by/4.0/
#Artist: http://www.twinmusicom.org/
pygame.mixer.music.load("8-Bit March - Twin Musicom.mp3")
pygame.mixer.music.play(loops=-1)

# Load all sound files
# Sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound("one.wav")
move_down_sound = pygame.mixer.Sound("two.wav")
collision_sound = pygame.mixer.Sound("Collision.ogg")

# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Custom event for adding new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Instantiate player. Right now, this is just a rectangle.
player = Player()

#Create groups to hold enemy sprites and all sprites
# enemenies is used for collision detectiona and position update
#all sprites used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Variable to keep the main loop running
running = True

#setup clock for decent framerate
clock = pygame.time.Clock()

# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        #Get the set of keys pressed and check for user input
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            if event.key == K_UP:
                move_up_sound.play()
            if event.key == K_DOWN:
                move_down_sound.play()
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False

        #Add a new enemy
        elif event.type == ADDENEMY:
            #Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        #Add a cloud
        elif event.type == ADDCLOUD:
            # Create the new cloud and add it to sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    #Update player sprite based on keypress
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    #Update enemy position
    enemies.update()
    clouds.update()

    # Fill the screen with blue
    screen.fill((135, 206, 250))

        #Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    #Check if any enemies have collided with player
    if pygame.sprite.spritecollideany(player, enemies):
        #if so remove player
        player.kill()

        # Stop any moving sounds and play the collision sound
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()
        pygame.time.delay(500)   # play for 1 second (adjust as needed)
        #stop the loop
        running = False

    # Draw the player on the screen
    screen.blit(player.surf, player.rect)

    # Update the display
    pygame.display.flip()

    #force program to maintian 30 fps
    clock.tick(25)

# All done! Stop and quit the mixer.
pygame.mixer.music.stop()
pygame.mixer.quit()