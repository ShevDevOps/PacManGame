import pygame
import pygame_menu
from pygame_menu import themes
from pygame_menu.widgets import Label, TextInput
import random
from pygame.sprite import * 
from typing import Tuple, List, Callable, Dict
from enum import Enum

class Tile:
    def __init__(self, s: str):
        self.isWall = False
        self.hasDot = False
        self.hasPill = False
        self.isRetPass = True
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

class GhostState(Enum):
    NORMAL = 0
    SCARED = 1
    EATEN = 2
    AFTER_EATEN = 3

class Map:
    def __init__(self, tileSize: int, data: str):
        lst = data.split('\n')
        it = iter(lst)
        the_len = len(next(it))
        if not all(len(l) == the_len for l in it):
            self.data = [[]]
        else:
            self.data = [[Tile(c) for c in s] for s in lst]
        self.height = len(self.data)
        self.width = len(self.data[0])
        self.tileSize = tileSize
        self.ghostReturnGoal = (0,0)
        self.ghostAfterReturnGoal = (0,0)
        self.dots : Group = Group()
        self.powerPills : Group = Group()
        for y in range(self.height):
            for x in range(self.width):
                if(lst[y][x] == 'C'):
                    self.playerStartPos = (x,y)
                if(lst[y][x] == 'G'):
                    self.ghostReturnGoal = (x,y)
                if(lst[y][x] == 'g'):
                    self.ghostAfterReturnGoal = (x,y)
    def isWall(self, x : int, y :int, state : GhostState = GhostState.NORMAL) ->bool:
        if(x < 0 or y < 0 or x >= self.width or y >= self.height or ( self.data[y][x].isWall if (state == GhostState.NORMAL or state == GhostState.SCARED) else not self.data[y][x].isRetPass)):
            return True
        return False
    
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
    def __init__(self, map : Map, frames : List[List[pygame.Surface]], frameDuration : int, *groups):
        super().__init__(*groups)
        self.frames = frames
        self.currentAnimation = 0
        self.currentFrame = 0
        self.frameDuration = frameDuration
        self.frameCounter = frameDuration
        for i in range(len(frames)):
            for j in range(len(frames[i])):
                frames[i][j] = pygame.transform.scale(frames[i][j], (map.tileSize, map.tileSize))
        self.angle = 0 
        self.__updateImage()
        self.rect = pygame.Rect(map.playerStartPos[0] * map.tileSize, map.playerStartPos[1] * map.tileSize, map.tileSize - 1, map.tileSize - 1)
        self.map = map
        self.animationEnded = False

        self.direction = None 
        self.nextDirection = None 
        self.isMoving = True
        self.directionDelay = 10
        self.directionCounter = 0

    def checkPortals(self):
        if self.getTile()[0] == 0:
            self.rect = self.rect.move((self.map.width - 3) * self.map.tileSize, 0)
            return
        
        if self.getTile()[0] == self.map.width - 2:
            self.rect = self.rect.move(-(self.map.width - 3) * self.map.tileSize, 0)
            return

    def __updateImage(self):
        self.image = pygame.transform.rotate(self.frames[self.currentAnimation][self.currentFrame], self.angle)

    def update(self, *args, **kwargs):
        if self.directionCounter > 0:
            self.directionCounter -= 1
        
        if self.nextDirection and self.canMove(self.nextDirection):
            self.direction = self.nextDirection
            self.nextDirection = None
        
        if self.isMoving:
            if self.direction == "up":
                self.moveUp(2)
            elif self.direction == "down":
                self.moveDown(2)
            elif self.direction == "left":
                self.moveLeft(2)
            elif self.direction == "right":
                self.moveRight(2)
        
        if self.frameCounter != 0:
            self.animationEnded = False
            self.frameCounter -= 1
            return super().update(*args, **kwargs)
        
        if self.currentFrame == len(self.frames[self.currentAnimation]) - 1:
            self.currentFrame = 0
            self.animationEnded = True
        else:
            self.currentFrame += 1
        self.__updateImage()
        self.frameCounter = self.frameDuration
        return super().update(*args, **kwargs)

    def reset(self):
        self.currentAnimation = 0
        self.currentFrame = 0
        self.frameCounter = self.frameDuration
        self.angle = 0 
        self.__updateImage()
        self.rect = pygame.Rect(self.map.playerStartPos[0]*self.map.tileSize , self.map.playerStartPos[1]*self.map.tileSize, self.map.tileSize - 1, self.map.tileSize - 1)
        self.animationEnded = False
        self.direction = None

    def moveUp(self, step):
        if not self.canMove("up"):
            return
        self.angle = 90
        self.__updateImage()
        self.checkPortals()
        self.rect = self.rect.move(0, -step)

    def moveDown(self, step):
        if not self.canMove("down"):
            return
        self.angle = 270
        self.__updateImage()
        self.checkPortals()
        self.rect = self.rect.move(0, step)

    def moveLeft(self, step):
        if not self.canMove("left"):
            return
        self.angle = 180
        self.__updateImage()
        self.checkPortals()
        self.rect = self.rect.move(-step, 0)

    def moveRight(self, step):
        if not self.canMove("right"):
            return
        self.angle = 0
        self.__updateImage()
        self.checkPortals()
        self.rect = self.rect.move(step, 0)

    def setDirection(self, new_direction): 
        if self.nextDirection != new_direction and self.directionCounter == 0:
            self.nextDirection = new_direction
            self.directionCounter = self.directionDelay

    def canMove(self, direction):
        if direction == "up":
            return not (self.map.isIntersect(*(self.rect.move(0, -2).topleft)) or 
                        self.map.isIntersect(*(self.rect.move(0, -2).topright)))
        elif direction == "down":
            return not (self.map.isIntersect(*(self.rect.move(0, 2).bottomleft)) or 
                        self.map.isIntersect(*(self.rect.move(0, 2).bottomright)))
        elif direction == "left":
            return not (self.map.isIntersect(*(self.rect.move(-2, 0).topleft)) or 
                        self.map.isIntersect(*(self.rect.move(-2, 0).bottomleft)))
        elif direction == "right":
            return not (self.map.isIntersect(*(self.rect.move(2, 0).topright)) or 
                        self.map.isIntersect(*(self.rect.move(2, 0).bottomright)))
        return False

    def getTile(self) -> Tuple[int, int]:
        return (self.rect.topleft[0] // self.map.tileSize, self.rect.topleft[1] // self.map.tileSize)

class GameState(Enum):
    PLAY = 0
    DEFEAT = 1
    OVER = 2
    MENU = 3

class Game:
    def __init__(self, screen : pygame.Surface ,map : Map, pacman : Pacman, ghosts : Dict[ str,"Ghost"], startLives : int, levels : List[List[int]],  bonusImage : pygame.Surface):
        self.screen = screen
        self.map = map
        self.bonusImage = pygame.transform.scale(bonusImage, (self.map.tileSize, self.map.tileSize))
        self.background = self.map.generateImage()
        self.pacman = pacman
        self.ghosts = ghosts 
        self.ghostsGroup = Group(*ghosts.values())
        self.renderGroup = Group(*ghosts.values(), self.pacman)
        self.bonusGroup = Group()
        self.startLives = startLives
        self.lives = self.startLives
        self.levels = levels
        self.currentLevel = 0
        self.score = 0
        self.state = GameState.MENU

    def startNewGame(self):
        self.currentLevel = 0
        self.score = 0
        self.startLevel()

    def reset(self):
        self.pacman.reset()
        for ghost in self.ghosts.values():
            ghost.reset()
        self.state = GameState.PLAY
    
    def startLevel(self):
        self.lives = self.startLives
        for g in self.ghosts.values():
            g.modes = self.levels[self.currentLevel]
        self.map.updateDots()
        self.reset()

    def nextLevel(self):
        self.currentLevel += 1
        if(self.currentLevel >= len(self.levels)):
            self.state = GameState.OVER
            return
        self.startLevel()
                
    def update(self):
        if(self.state != GameState.PLAY and self.state != GameState.DEFEAT):
            return

        self.screen.fill("black")
        self.screen.blit(self.background, (0, 0))

        if(self.state == GameState.PLAY):

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.pacman.setDirection("up")
            elif keys[pygame.K_s]:
                self.pacman.setDirection("down")
            elif keys[pygame.K_a]:
                self.pacman.setDirection("left")
            elif keys[pygame.K_d]:
                self.pacman.setDirection("right")

            
            self.pacman.update()
            self.ghostsGroup.update(game=gameObj)
            bonusColide = len(spritecollide(self.pacman, self.bonusGroup, True))
            self.score += bonusColide*200
            self.score += len(spritecollide(self.pacman, gameMap.dots, True))
            pillsColide = len(spritecollide(self.pacman, gameMap.powerPills, True))
            if(pillsColide > 0):
                self.score += pillsColide*10
                for g in self.ghosts.values():
                    g.scare()
                        
            if(len(self.map.dots.sprites()) == 0 and len(self.map.powerPills.sprites()) == 0):
                self.nextLevel()
                    
            colidedGhosts : List[Ghost] = spritecollide(self.pacman, self.ghostsGroup, False)
            for g in colidedGhosts:
                    if(g.state == GhostState.SCARED):
                        g.eat()
                        self.score += 100
                    elif(g.state == GhostState.NORMAL):
                        self.lives -= 1
                        self.state = GameState.DEFEAT
                        self.pacman.currentAnimation = 1
                        self.pacman.currentFrame = 0
                        break

            if(random.randrange(1200) == 1):
                bonusX = 0
                bonusY = 0
                while self.map.isWall(bonusX, bonusY):
                    bonusX = random.randrange(self.map.width)
                    bonusY = random.randrange(self.map.height)
                AlighnedSprite(self.map, self.bonusImage, bonusX, bonusY, self.renderGroup, self.bonusGroup)

        else:
            self.pacman.update()
            if(self.pacman.animationEnded):
                if(self.lives == 0):
                    self.state = GameState.OVER
                else:
                    self.reset() 
        self.map.dots.draw(self.screen)
        self.map.powerPills.draw(self.screen)
        self.renderGroup.draw(self.screen)       


class LeaderBoard:
    def __init__(self, menuWidth : int, menuHeight: int):
        self.board = []
        self.message = ""
        self.menu = pygame_menu.Menu("Leader Board", menuWidth, menuHeight, theme=themes.THEME_DARK)
        self.menu.add.button("Quit", pygame_menu.events.BACK)

    def add(self, name : str, score : int):
        if(self.check(name)):
            self.board.append((name, score))
            self.menu.add.label(f"{name} - {score}")
            return True
        return False

    def check(self, name : str) -> bool:
        for record in self.board:
            if(record[0] == name):
                self.message = f"\"{name}\" is already taken"
                return False
        self.message = ""
        return True

def calcDistanceSqr(a : Tuple[int, int], b : Tuple[int, int]) -> int:
        return pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2)
        
        
class Ghost(Sprite):
    def __init__(self, map : Map,
    images : List[List[pygame.Surface]],
    frameDuration : int,
    modes : List[int],
    speed : int,
    returnSpeed : int,
    scaredTime : int,
    targetFuction : Callable[[Game], Tuple[int, int]],
    startX : int,
    startY : int,
    scatterGoalX : int, 
    scatterGoalY : int,
    returnGoalX : int, 
    returnGoalY : int,
    afterReturnX : int,
    afterReturnY : int, 
    *groups):
        super().__init__(*groups)
        self.map = map
        self.speed = speed
        self.returnSpeed = returnSpeed
        self.currentSpeed = self.speed
        self.targetFuction = targetFuction
        self.images = images
        for i in range(len(images)):
            for j in range(len(images[i])):
                images[i][j] =  pygame.transform.scale(images[i][j], (map.tileSize, map.tileSize))
        self.currentAnimation = 0
        self.currentFrame = 0
        self.updateImage()
        self.frameDuration = frameDuration
        self.currentFrameDuration = frameDuration
        self.rect = pygame.Rect(startX * map.tileSize, startY * map.tileSize, map.tileSize, map.tileSize)
        self.startX = startX
        self.startY = startY
        self.curX = startX
        self.curY = startY
        self.scatterGoalX = scatterGoalX
        self.scatterGoalY = scatterGoalY
        self.dX = 0
        self.dY = 0 
        self.modes = modes
        self.currentMode = 0
        self.returnGoalX = returnGoalX
        self.returnGoalY = returnGoalY
        self.afterReturnX = afterReturnX
        self.afterReturnY = afterReturnY
        self.modeDuartion = self.modes[0]
        self.state : GhostState = GhostState.NORMAL
        self.scaredTime = scaredTime
        self.scaredTimer = 0

    def updateImage(self):
        self.image = self.images[self.currentAnimation][self.currentFrame]

    def reset(self):
        self.curX = self.startX
        self.curY = self.startY
        self.state : GhostState = GhostState.NORMAL
        self.currentMode = 0
        self.modeDuartion = self.modes[0]
        self.currentAnimation = 0
        self.currentFrame = 0
        self.updateImage()
        self.currentFrameDuration = self.frameDuration
        self.state : GhostState = GhostState.NORMAL
        self.scaredTimer = 0
        self.rect = pygame.Rect(self.startX * self.map.tileSize, self.startY * self.map.tileSize, self.map.tileSize, self.map.tileSize)
        
    def updateAnimation(self):
        self.currentFrameDuration -= 1
        if(self.currentFrameDuration == 0):
            self.currentFrameDuration = self.frameDuration
            self.currentFrame += 1
            if(self.currentFrame >= len(self.images[self.currentAnimation])):
                self.currentFrame = 0
            self.updateImage()

    def updateMode(self):
        self.modeDuartion -= 1
        if(self.modeDuartion <= 0):
            self.currentMode += 1
            if(self.currentMode >= len(self.modes)):
                self.currentMode = 0
            self.modeDuartion = self.modes[self.currentMode]

    def scare(self):
        if(self.state == GhostState.NORMAL):
            self.state = GhostState.SCARED
            self.currentAnimation = 4
            self.scaredTimer = self.scaredTime
            
    def eat(self):
        if(self.state == GhostState.SCARED):
            self.state = GhostState.EATEN
            self.currentAnimation = 5
            self.currentFrame = 0
            self.currentSpeed = self.returnSpeed
    
    def update(self, *args, **kwargs):

        self.updateAnimation()

        if(not(self.rect.topleft[0] % self.map.tileSize == 0 and
           self.rect.topleft[1] % self.map.tileSize == 0)):
            self.rect = self.rect.move(self.dX, self.dY)
            return
            
        self.updateMode()

        newX : int = int(self.rect.topleft[0] / self.map.tileSize)
        newY : int = int(self.rect.topleft[1] / self.map.tileSize)

        if(newX == 0):
            self.rect = self.rect.move(self.map.width * self.map.tileSize + self.dX - self.map.tileSize, 0)
            return
        
        if(newX == self.map.width - 1):
            self.rect = self.rect.move(-self.map.width * self.map.tileSize + self.dX + self.map.tileSize, 0)
            return

        if(self.state == GhostState.EATEN and
        newX == self.returnGoalX and
        newY == self.returnGoalY):
            self.state = GhostState.AFTER_EATEN
            self.currentSpeed = self.speed
            
        if(self.state == GhostState.AFTER_EATEN and
        newX == self.afterReturnX and
        newY == self.afterReturnY):
            self.state = GhostState.NORMAL
            
        if(self.state == GhostState.SCARED):
            self.scaredTimer -= 1
            if(self.scaredTimer == 0):
                self.state = GhostState.NORMAL

        targetCoords = (0,0)
        if(self.state == GhostState.NORMAL):
            if(self.currentMode % 2 == 0):
                game : Game = kwargs["game"]
                targetCoords = self.targetFuction(game)
            else:
                targetCoords = (self.scatterGoalX, self.scatterGoalY)
        elif(self.state == GhostState.EATEN):
            targetCoords = (self.returnGoalX, self.returnGoalY)
        elif(self.state == GhostState.AFTER_EATEN):
            targetCoords = (self.afterReturnX, self.afterReturnY)
        
        topDistance = calcDistanceSqr((newX, newY - 1), targetCoords)
        leftDistance = calcDistanceSqr((newX - 1, newY), targetCoords)
        bottomDistance = calcDistanceSqr((newX, newY + 1), targetCoords)
        rightDistance = calcDistanceSqr((newX + 1, newY), targetCoords)
        
        directions = [(topDistance, newX, newY - 1, 0, -self.currentSpeed, 3), 
                      (leftDistance, newX - 1, newY, -self.currentSpeed, 0, 0),
                      (bottomDistance, newX, newY + 1, 0, self.currentSpeed, 2),
                      (rightDistance, newX + 1, newY, self.currentSpeed, 0, 1)]
        validDirections = [d for d in directions if(not (d[1] == self.curX and d[2] == self.curY) and not self.map.isWall(d[1], d[2], self.state))]
        
        if(self.state != GhostState.SCARED):
            finalDirection = min(validDirections, key=lambda item:item[0])
        else:
            finalDirection = random.choice(validDirections)
        
        self.dX = finalDirection[3]
        self.dY = finalDirection[4]
        self.curX = newX
        self.curY = newY
        if(self.state == GhostState.NORMAL):
            self.currentAnimation = finalDirection[5]
            self.updateImage()
        self.rect = self.rect.move(self.dX, self.dY)
        return super().update(*args, **kwargs)




# pygame setup
pygame.init()
screen = pygame.display.set_mode((470, 510))
clock = pygame.time.Clock()
running = True
dt = 0 

with open("map/mapData.txt", 'r') as file:
    mapData = file.read()

gameMap = Map(16, mapData)
player = Pacman(gameMap, [[ pygame.image.load(f"pacman/frame_{i}.png").convert()  for i in range(8)],[pygame.image.load(f"pacman/gameOver/frame_{i}.png").convert()  for i in range(42)]], 3)

blinky = Ghost(gameMap, 
                [[pygame.image.load(f"blinky/frame_{i}_{j}.png").convert() for j in range(2)] for i in range(4)] + 
                [[pygame.image.load(f"scared/scared_{i}.png").convert() for i in range(2)]] +
                [[pygame.image.load(f"eaten/eaten.png").convert()]],
                10,
                [30, 30],
                2,
                4,
                30,
               lambda g : g.pacman.getTile(),
               gameMap.ghostAfterReturnGoal[0],
               gameMap.ghostAfterReturnGoal[1],
               -1,
               -1,
               gameMap.ghostReturnGoal[0],
               gameMap.ghostReturnGoal[1],
               gameMap.ghostAfterReturnGoal[0],
               gameMap.ghostAfterReturnGoal[1]
               )

pinky = Ghost(gameMap, 
                [[pygame.image.load(f"pinky/frame_{i}_{j}.png").convert() for j in range(2)] for i in range(4)] + 
                [[pygame.image.load(f"scared/scared_{i}.png").convert() for i in range(2)]] +
                [[pygame.image.load(f"eaten/eaten.png").convert()]],
                10,
                [30, 30],
                2,
                4,
                30,
               lambda g : (g.pacman.getTile()[0] + (4 if g.pacman.angle == 0 else (-4 if g.pacman.angle == 180 else 0)),
                           g.pacman.getTile()[1] + (4 if g.pacman.angle == 270 else (-4 if g.pacman.angle == 90 else 0))),
               gameMap.ghostAfterReturnGoal[0] - 1,
               gameMap.ghostAfterReturnGoal[1],
               gameMap.width,
               -1,
               gameMap.ghostReturnGoal[0],
               gameMap.ghostReturnGoal[1],
               gameMap.ghostAfterReturnGoal[0],
               gameMap.ghostAfterReturnGoal[1]
               )

inky = Ghost(gameMap, 
                [[pygame.image.load(f"inky/frame_{i}_{j}.png").convert() for j in range(2)] for i in range(4)] + 
                [[pygame.image.load(f"scared/scared_{i}.png").convert() for i in range(2)]] +
                [[pygame.image.load(f"eaten/eaten.png").convert()]],
                10,
                [30, 30],
                2,
                4,
                30,
               lambda g : (g.pacman.getTile()[0] + (g.pacman.getTile()[0] - g.ghosts["blinky"].curX),
                           g.pacman.getTile()[1] + (g.pacman.getTile()[1] - g.ghosts["blinky"].curY)),
               gameMap.ghostAfterReturnGoal[0] + 1,
               gameMap.ghostAfterReturnGoal[1],
               gameMap.width,
               gameMap.height,
               gameMap.ghostReturnGoal[0],
               gameMap.ghostReturnGoal[1],
               gameMap.ghostAfterReturnGoal[0],
               gameMap.ghostAfterReturnGoal[1]
               )

clyde = Ghost(gameMap, 
                [[pygame.image.load(f"clyde/frame_{i}_{j}.png").convert() for j in range(2)] for i in range(4)] + 
                [[pygame.image.load(f"scared/scared_{i}.png").convert() for i in range(2)]] +
                [[pygame.image.load(f"eaten/eaten.png").convert()]],
                10,
                [30, 30],
                2,
                4,
                30,
               lambda g : (-1, gameMap.height) if calcDistanceSqr(g.pacman.getTile(), (g.ghosts["clyde"].curX,g.ghosts["clyde"].curY)) < 64 else g.pacman.getTile(),
               gameMap.ghostAfterReturnGoal[0] - 2,
               gameMap.ghostAfterReturnGoal[1],
               -1,
               gameMap.height,
               gameMap.ghostReturnGoal[0],
               gameMap.ghostReturnGoal[1],
               gameMap.ghostAfterReturnGoal[0],
               gameMap.ghostAfterReturnGoal[1]
               )

gameObj = Game(screen, gameMap, player, {"blinky" : blinky, "pinky" : pinky, "inky" : inky, "clyde" : clyde}, 3, [[30, 40], [30, 40]], pygame.image.load("cherry.png").convert_alpha(screen))

def startGame():
    global gameObj
    gameObj.startNewGame()

mainMenu = pygame_menu.Menu("Pac-Man", screen.get_width(), screen.get_height(), theme=themes.THEME_DARK)


board = LeaderBoard(screen.get_width(), screen.get_height())
gameOverMenu = pygame_menu.Menu("Game Over", screen.get_width(), screen.get_height(), theme=themes.THEME_DARK)

def checkName(name : str, widget : TextInput):
    global board
    board.check(name)

def addName(name : str, widget : TextInput):
    global gameObj
    global board
    if(board.add(name, gameObj.score)):
        gameObj.state = GameState.MENU
        widget.set_value("")

def openBoard():
    global board
    global mainMenu
    mainMenu._open(board.menu)

mainMenu.add.button("Play", startGame)
mainMenu.add.button("Leader Board", openBoard)
mainMenu.add.button("Quit", pygame_menu.events.EXIT)

scoreLabel : Label  =  gameOverMenu.add.label("Your Score is 0")
warningLabel : Label = gameOverMenu.add.label("")
nameInput : TextInput = gameOverMenu.add.text_input("Enter Your name:  ", onchange=checkName, onreturn=addName)
nameInput.add_self_to_kwargs()

while running:

    if(gameObj.state == GameState.MENU):
        mainMenu.enable()
    else:
        mainMenu.disable()

    if(gameObj.state == GameState.OVER):
        gameOverMenu.enable()
        warningLabel.set_title(board.message)
    else:
        gameOverMenu.disable()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
 
    if(mainMenu.is_enabled()):
        mainMenu.update(events)
        mainMenu.draw(screen)

    if(gameOverMenu.is_enabled()):
        gameOverMenu.update(events)
        gameOverMenu.draw(screen)

    
    gameObj.update()
    if(gameObj.state == GameState.OVER):
        scoreLabel.set_title(f"Your Score is {gameObj.score}")    

    pygame.display.flip()
    clock.tick(60)

pygame.quit()