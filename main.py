import pygame
from pygame.sprite import * 

class Tile:
    def __init__(self, isWall: bool):
        self.isWall = isWall
class Map:
    def __init__(self, tileSize: int, data: str):
        self.data = [[Tile(c == '#') for c in row] for row in data.split('\n')]
        self.height = len(self.data)
        self.width = len(self.data[0])
        self.tileSize = tileSize
        self.playerStartPos = next(((x, y) for y, row in enumerate(data.split('\n')) for x, c in enumerate(row) if c == 'C'), (0, 0))
    
    def isWall(self, x: int, y: int) -> bool:
        return not (0 <= x < self.width and 0 <= y < self.height) or self.data[y][x].isWall
    
    def generateImage(self) -> pygame.Surface:
        surface = pygame.Surface((self.width * self.tileSize, self.height * self.tileSize))
        surface.fill('black')
        for y in range(self.height):
            for x in range(self.width):
                if self.isWall(x, y):
                    pygame.draw.rect(surface, 'white', (x * self.tileSize, y * self.tileSize, self.tileSize, self.tileSize))
        return surface
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen = pygame.display.set_mode((490, 510))
clock = pygame.time.Clock()
running = True
dt = 0 

with open("mapData.txt", 'r') as file:
    mapData = file.read()

gameMap = Map(16, mapData)
background = gameMap.generateImage()
 
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black") 
    screen.blit(background, (0, 0))
 
    # flip() the display to put your work on screen
    pygame.display.flip()
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    clock.tick(60) 
 
pygame.quit()