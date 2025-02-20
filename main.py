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

    def checkPortals(self):
        if(self.getTile()[0] == 0):
            self.rect = self.rect.move((self.map.width - 3) * self.map.tileSize, 0)
            return
        
        if(self.getTile()[0] == self.map.width - 2):
            self.rect = self.rect.move(-(self.map.width - 3) * self.map.tileSize, 0)
            return

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

    def reset(self):
        self.currentAnimation = 0
        self.currentFrame = 0
        self.frameCounter = 3
        self.angle = 0 
        self.__updateImage()
        self.rect = pygame.Rect(self.map.playerStartPos[0]*self.map.tileSize , self.map.playerStartPos[1]*self.map.tileSize, self.map.tileSize - 1, self.map.tileSize - 1)
        self.animationEnded = False

    def moveUp(self, step):
        #print(self.rect.topleft)
        if(self.map.isIntersect(*(self.rect.move(0, -step).topleft)) or 
        self.map.isIntersect(*(self.rect.move(0, -step).topright))):
            return
        self.angle = 90
        self.__updateImage()
        self.checkPortals()
        self.rect = self.rect.move(0, -step)

    def moveDown(self, step):
        #print(self.rect.topleft)
        if(self.map.isIntersect(*(self.rect.move(0, step).bottomleft)) or 
        self.map.isIntersect(*(self.rect.move(0, step).bottomright))):
            return
        self.angle = 270
        self.__updateImage()
        self.checkPortals()
        self.rect = self.rect.move(0, step)

    def moveLeft(self, step):
        #print(self.rect.topleft)
        if(self.map.isIntersect(*(self.rect.move(-step, 0).topleft)) or 
        self.map.isIntersect(*(self.rect.move(-step, 0).bottomleft))):
            return
        self.angle = 180
        self.__updateImage()
        self.checkPortals()
        self.rect = self.rect.move(-step, 0)

    def moveRight(self, step):
        #print(self.rect.topleft)
        if(self.map.isIntersect(*(self.rect.move(step, 0).topright)) or 
        self.map.isIntersect(*(self.rect.move(step, 0).bottomright))):
            return
        self.angle = 0
        self.__updateImage()
        self.checkPortals()
        self.rect = self.rect.move(step, 0)

    def getTile(self) -> Tuple[int, int]:
        return (self.rect.topleft[0] // self.map.tileSize, self.rect.topleft[0] // self.map.tileSize)


class Game:
    def __init__(self, screen : pygame.Surface ,map : Map, pacman : Pacman):
        self.screen = screen
        self.map = map
        self.map.updateDots()
        self.background = self.map.generateImage()
        self.pacman = pacman
        self.renderGroup = Group(self.pacman)
        self.currentLevel = 0
        self.score = 0

    def reset(self):
        self.pacman.reset()

    def startLevel(self):
            self.map.updateDots()
            self.reset()

    def nextLevel(self):
            self.currentLevel += 1
            self.startLevel()
                
    def update(self):
        self.screen.fill("black")
        self.screen.blit(self.background, (0, 0))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.pacman.moveUp(4)
        if keys[pygame.K_s]:
            self.pacman.moveDown(4)
        if keys[pygame.K_a]:
            self.pacman.moveLeft(4)
        if keys[pygame.K_d]:
            self.pacman.moveRight(4)

        self.map.dots.draw(self.screen)
        self.map.powerPills.draw(self.screen)
        self.renderGroup.draw(self.screen)
        self.pacman.update()

        self.score += len(spritecollide(self.pacman, gameMap.dots, True))
        pillsColide = len(spritecollide(self.pacman, gameMap.powerPills, True))
        if(pillsColide > 0):
            self.score += pillsColide*10
        if(len(self.map.dots.sprites()) == 0 and len(self.map.powerPills.sprites()) == 0):
                self.nextLevel()

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
player = Pacman(gameMap)
gameObj = Game(screen, gameMap, player)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    gameObj.update()
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    clock.tick(60)

pygame.quit()