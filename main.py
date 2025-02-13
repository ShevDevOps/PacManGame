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

class Pacman(pygame.sprite.Sprite):
    def __init__(self, map, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((map.tileSize, map.tileSize))
        self.image.fill('yellow')
        self.rect = pygame.Rect(map.playerStartPos[0] * map.tileSize, 
                                 map.playerStartPos[1] * map.tileSize, 
                                 map.tileSize, map.tileSize)
        self.map = map
    
    def canMove(self, dx, dy):
        new_x = self.rect.centerx + dx
        new_y = self.rect.centery + dy
        tile_x = new_x // self.map.tileSize
        tile_y = new_y // self.map.tileSize
        return not self.map.isWall(tile_x, tile_y)
    
    def move(self, dx, dy):
        if dx != 0 and self.canMove(dx, 0):
            self.rect.x += dx
        elif dy != 0 and self.canMove(0, dy):
            self.rect.y += dy




# pygame setup
pygame.init()
screen = pygame.display.set_mode((470, 510))
clock = pygame.time.Clock()
running = True
dt = 0 

with open("mapData.txt", 'r') as file:
    mapData = file.read()

gameMap = Map(16, mapData)
background = gameMap.generateImage()

renderGroup = RenderPlain()
player = Pacman(gameMap, renderGroup)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    screen.blit(background, (0, 0))
    

    #pygame.draw.circle(screen, "red", player_pos, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.move(0, -4)
    elif keys[pygame.K_s]:
        player.move(0, 4)
    elif keys[pygame.K_a]:
        player.move(-4, 0)
    elif keys[pygame.K_d]:
        player.move(4, 0)

    renderGroup.draw(screen)
    player.update()


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    clock.tick(60)

pygame.quit()