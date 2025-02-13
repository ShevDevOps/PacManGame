import pygame
from pygame.sprite import * 


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen = pygame.display.set_mode((490, 510))
clock = pygame.time.Clock()
running = True


 
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black") 
    
 
    # flip() the display to put your work on screen
    pygame.display.flip()
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    clock.tick(60) 

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
pygame.quit()