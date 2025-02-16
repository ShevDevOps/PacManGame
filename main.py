import pygame
from pygame.sprite import * 
from typing import Tuple, List

class Tile:
    def __init__(self, s: str):
        self.isWall = False
        self.hasDot = False
        self.hasPill = False
        if(s == '#'):
            self.isWall = True
            self.isRetPass = False
        elif(s == 'R' or s == 'G'):
            self.isWall = True
        elif(s == 'D'):
            self.hasDot = True
        elif(s == 'P'):
            self.hasPill = True
        
class AlighnedSprite(Sprite):
    def __init__(self, map : "Map", image : pygame.Surface, x : int, y : int, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = (x * map.tileSize, y * map.tileSize, map.tileSize, map.tileSize)

class Map:
    def __init__(self, tileSize: int, data: str):
        self.data = [[Tile(c) for c in row] for row in data.split('\n')]
        self.height = len(self.data)
        self.width = len(self.data[0])
        self.tileSize = tileSize
        self.dots : Group = Group()
        self.powerPills : Group = Group()
        self.playerStartPos = next(((x, y) for y, row in enumerate(data.split('\n')) for x, c in enumerate(row) if c == 'C'), (0, 0))
    
    def isWall(self, x: int, y: int) -> bool:
        return not (0 <= x < self.width and 0 <= y < self.height) or self.data[y][x].isWall
    
    def blitTile(self, surface : pygame.Surface, tile : pygame.Surface, x : int, y : int, angle : float = 0):
        surface.blit(pygame.transform.rotate(tile, angle), (x * self.tileSize + self.tileSize/2, y * self.tileSize + self.tileSize/2))

    def generateImage(self) -> pygame.Surface: 
        result = pygame.Surface((self.tileSize*len(self.data[0]) + self.tileSize/2, self.tileSize*len(self.data) + self.tileSize/2))
        result.fill('black')
        cornerTile = pygame.transform.scale(pygame.image.load(f"tiles/cornerTile.png").convert(), (self.tileSize, self.tileSize))
        straightTile = pygame.transform.scale(pygame.image.load(f"tiles/straightTile.png").convert(), (self.tileSize, self.tileSize))
        passageTile = pygame.transform.scale(pygame.image.load(f"tiles/passageTile.png").convert(), (self.tileSize, self.tileSize))

        for y in range(1, len(self.data) - 1):
            for x in range(1, len(self.data[y]) -1):
                if(self.isWall(x, y) and
                self.isWall(x + 1, y) and
                self.isWall(x, y + 1) and
                self.isWall(x + 1, y + 1)):
                    self.blitTile(result, passageTile, x, y)
                elif(not self.isWall(x, y) and
                not self.isWall(x + 1, y) and
                not self.isWall(x, y + 1) and
                not self.isWall(x + 1, y + 1)):
                    self.blitTile(result, passageTile, x, y)
                elif(not self.isWall(x, y) and
                not self.isWall(x + 1, y) and
                not self.isWall(x, y + 1) and
                self.isWall(x + 1, y + 1)):
                    self.blitTile(result, cornerTile, x, y)
                elif(self.isWall(x, y) and
                self.isWall(x + 1, y) and
                self.isWall(x, y + 1) and
                not self.isWall(x + 1, y + 1)):
                    self.blitTile(result, cornerTile, x, y)
                elif(self.isWall(x, y) and
                not self.isWall(x + 1, y) and
                self.isWall(x, y + 1) and
                self.isWall(x + 1, y + 1)):
                    self.blitTile(result, cornerTile, x, y, 90)
                elif(not self.isWall(x, y) and
                self.isWall(x + 1, y) and
                not self.isWall(x, y + 1) and
                not self.isWall(x + 1, y + 1)):
                    self.blitTile(result, cornerTile, x, y, 90)
                elif(not self.isWall(x, y) and
                self.isWall(x + 1, y) and
                self.isWall(x, y + 1) and
                self.isWall(x + 1, y + 1)):
                    self.blitTile(result, cornerTile, x, y, 180)
                elif(self.isWall(x, y) and
                not self.isWall(x + 1, y) and
                not self.isWall(x, y + 1) and
                not self.isWall(x + 1, y + 1)):
                    self.blitTile(result, cornerTile, x, y, 180)
                elif(self.isWall(x, y) and
                self.isWall(x + 1, y) and
                not self.isWall(x, y + 1) and
                self.isWall(x + 1, y + 1)):
                    self.blitTile(result, cornerTile, x, y, 270)
                elif(not self.isWall(x, y) and
                not self.isWall(x + 1, y) and
                self.isWall(x, y + 1) and
                not self.isWall(x + 1, y + 1)):
                    self.blitTile(result, cornerTile, x, y, 270)
                elif(self.isWall(x, y) and
                not self.isWall(x + 1, y) and
                self.isWall(x, y + 1) and
                not self.isWall(x + 1, y + 1)):
                    self.blitTile(result, straightTile, x, y)
                elif(not self.isWall(x, y) and
                self.isWall(x + 1, y) and
                not self.isWall(x, y + 1) and
                self.isWall(x + 1, y + 1)):
                    self.blitTile(result, straightTile, x, y)
                elif(not self.isWall(x, y) and
                not self.isWall(x + 1, y) and
                self.isWall(x, y + 1) and
                self.isWall(x + 1, y + 1)):
                    self.blitTile(result, straightTile, x, y, 90)
                elif(self.isWall(x, y) and
                self.isWall(x + 1, y) and
                not self.isWall(x, y + 1) and
                not self.isWall(x + 1, y + 1)):
                    self.blitTile(result, straightTile, x, y, 90)
        return result

    def isIntersect(self, x : int, y: int) -> bool:
        tileX = x // self.tileSize
        tileY = y // self.tileSize
        if(tileX < 0 or 
        tileY < 0 or 
        tileX >= self.width or 
        tileY >= self.height or 
        self.data[tileY][tileX].isWall):
            #print(f"X{x} Y{y} Xtile{tileX} Ytile{tileY}")
            return True
        return False
    
    def killSprites(self, group : Group):
        spritesList : List[Sprite] = group.sprites()
        group.empty()
        for sprite in spritesList:
            sprite.kill()

    def updateDots(self):
        
        self.killSprites(self.dots)
        self.killSprites(self.powerPills)

        dotImage = pygame.transform.scale(pygame.image.load("dots/dot.png").convert(), (self.tileSize, self.tileSize))
        dotImage.set_colorkey(pygame.Color(0,0,0))
        pillImage = pygame.transform.scale(pygame.image.load("dots/pill.png").convert(), (self.tileSize, self.tileSize))
        pillImage.set_colorkey(pygame.Color(0,0,0))
        for y in range(self.height):
            for x in range(self.width):
                if(self.data[y][x].hasDot):
                    AlighnedSprite(self, dotImage, x, y, self.dots)
                if(self.data[y][x].hasPill):
                    AlighnedSprite(self, pillImage, x, y, self.powerPills)

class Pacman(Sprite):
    def __init__(self, map : Map, *groups):
        super().__init__(*groups)
        self.frames = [pygame.transform.scale(pygame.image.load(f"frames/frame_{i}.png").convert(), (map.tileSize,map.tileSize)) for i in range(5)]
        self.currentFrame = 0
        self.frameCounter = 3
        self.image = self.frames[0]
        self.angle = 0 
        self.rect = pygame.Rect(map.playerStartPos[0]*map.tileSize , map.playerStartPos[1]*map.tileSize, map.tileSize - 1, map.tileSize - 1)
        self.map = map

    def __updateImage(self):
        self.image = pygame.transform.rotate(self.frames[self.currentFrame], self.angle)

    def update(self, *args, **kwargs):
        
        if(self.frameCounter != 0):
            self.frameCounter -= 1
            return super().update(*args, **kwargs)
        
        if(self.currentFrame == 4):
            self.currentFrame = 0
        else:
            self.currentFrame += 1
        self.__updateImage()
        self.frameCounter = 3
        return super().update(*args, **kwargs)

    

    def moveUp(self, step):
        #print(self.rect.topleft)
        if(self.map.isIntersect(*(self.rect.move(0, -step).topleft)) or 
        self.map.isIntersect(*(self.rect.move(0, -step).topright))):
            return
        self.angle = 90
        self.__updateImage()
        self.rect = self.rect.move(0, -step)

    def moveDown(self, step):
        #print(self.rect.topleft)
        if(self.map.isIntersect(*(self.rect.move(0, step).bottomleft)) or 
        self.map.isIntersect(*(self.rect.move(0, step).bottomright))):
            return
        self.angle = 270
        self.__updateImage()
        self.rect = self.rect.move(0, step)

    def moveLeft(self, step):
        #print(self.rect.topleft)
        if(self.map.isIntersect(*(self.rect.move(-step, 0).topleft)) or 
        self.map.isIntersect(*(self.rect.move(-step, 0).bottomleft))):
            return
        self.angle = 180
        self.__updateImage()
        self.rect = self.rect.move(-step, 0)

    def moveRight(self, step):
        #print(self.rect.topleft)
        if(self.map.isIntersect(*(self.rect.move(step, 0).topright)) or 
        self.map.isIntersect(*(self.rect.move(step, 0).bottomright))):
            return
        self.angle = 0
        self.__updateImage()
        self.rect = self.rect.move(step, 0)

    def getTile(self) -> Tuple[int, int]:
        return (self.rect.topleft[0] // self.map.tileSize, self.rect.topleft[0] // self.map.tileSize)




# pygame setup
pygame.init()
screen = pygame.display.set_mode((470, 510))
clock = pygame.time.Clock()
running = True
dt = 0 
score = 0

with open("map/mapData.txt", 'r') as file:
    mapData = file.read()

gameMap = Map(16, mapData)
background = gameMap.generateImage()
gameMap.updateDots()

renderGroup = RenderPlain()
player = Pacman(gameMap, renderGroup)
renderGroup.add(*gameMap.dots.sprites(), *gameMap.powerPills.sprites())

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
        player.moveUp(4)
    if keys[pygame.K_s]:
        player.moveDown(4)
    if keys[pygame.K_a]:
        player.moveLeft(4)
    if keys[pygame.K_d]:
        player.moveRight(4)
    score += len(spritecollide(player, gameMap.dots, True))
    pillsColide = len(spritecollide(player, gameMap.powerPills, True))
    renderGroup.draw(screen)
    player.update()


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    clock.tick(60)

pygame.quit()