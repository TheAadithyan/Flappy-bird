import pygame
import random

screenWidth = 800
screenHeight = 600
obstacleSpeed = 8
distanceBetweenObstacles = 115
#clock = pygame.time.Clock()
score = 0
gravityStrength = 8
jumpStrength = 6
gamestate = 1
allowScoreCheck = 0
background = pygame.image.load("sky.png")
background = pygame.transform.scale(background, (800, 600))
isJumping = False

class mainCharacter(object):
    
    def __init__(self, x, y, width, height):
        self.name = "mainCharacter"
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 8
        self.left = False
        self.right = False
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.jumping = False
        self.jumpCount = jumpStrength
        self.characterImage = pygame.image.load("flappy.png")
        self.characterImage = pygame.transform.scale(self.characterImage, (64, 64))
    
    def draw(self, win):
        # pygame.draw.rect(win, (255,0,0), (self.x, self.y, self.width, self.height))
        self.hitbox = (self.x, self.y, self.width, self.height)
        # pygame.draw.rect(win, (200, 170, 200), self.hitbox, 2)        
        win.blit(self.characterImage, self.hitbox)



    def gravity(self, boolean):

        if boolean == True:
            self.y += gravityStrength
        elif boolean == False:
            self.y = self.y
    
class obstacle(object):

    def __init__(self):
        self.x = screenWidth
        self.width = 100
        self.gapSize = 250
        self.botHeight = 0
        self.topHeight = 0
        randomHeight = random.randint(10, screenHeight/2 - 20)
        self.botHeight = randomHeight
        self.topHeight = (self.botHeight + self.gapSize)
    
    def draw(self, win):
        pygame.draw.rect(win, (0,255,0), (self.x, 0, self.width, self.botHeight))
        pygame.draw.rect(win, (0,255,0), (self.x, self.topHeight, self.width, screenHeight))

    def resize(self):
        randomHeight = random.randint(10, screenHeight/2 - 20)
        self.botHeight = randomHeight
        self.topHeight = (self.botHeight + self.gapSize)
    
    def xCheck(self):
        if self.x <= 0:
            return False
        if self.x >= 0:
            return True

def collisionCheck(char, obstacle):

    global allowScoreCheck

    def collision():
        global gamestate
        gamestate = 0
    
    #TODO
    #adjust conditions for collision
    #check x co-ordinates
    if char.x + char.width >= obstacle.x and char.x <= obstacle.x + obstacle.width:
        if char.y <= obstacle.botHeight or char.y + char.height >= obstacle.topHeight:
            collision()
    if char.y + char.height >= screenHeight:
        collision()
   
def scoreCheck(char, obstacle):
    global score
    if char.x >= obstacle.x and char.x + char.width <= obstacle.x + char.width + 3:
        score += 1

def updateScore(win):
    pygame.font.init()
    myFont = pygame.font.SysFont("Comic Sans MS", 24)
    scoreBoard = myFont.render("Your Score: " + str(score), False, (255, 255, 0))
    scoreX = screenWidth - (screenWidth/3)
    scoreY = 40
    win.blit(scoreBoard, (scoreX, scoreY))

def redrawGameWindow(win, player, pipeList):
    win.blit(background, (0,0))
    #collisionCheck(player, item)
    player.draw(win)
    for pipe in pipeList:
        if pipe.xCheck == False:
           pipeList.remove(pipe)
        scoreCheck(player, pipe)
        pipe.draw(win)
        collisionCheck(player, pipe)
    #item.draw(win)
    updateScore(win)
    #print(pipeList)  
    pygame.display.update()

def redrawGameOver(win):
    win.fill((0,0,0))
    pygame.font.init()
    myFont = pygame.font.SysFont("Comic Sans MS", 24)
    gameOverText = myFont.render("Game Over - Press ESC to exit.", False, (255, 255, 0))
    continueText = myFont.render("Press ENTER to continue.", False, (255, 255, 0))
    gameOverX = (screenWidth/4)
    gameOverY = screenHeight/2
    win.blit(gameOverText, (gameOverX, gameOverY))
    win.blit(continueText, (gameOverX, gameOverY + 30))
    pygame.display.update()
    
def game():

    clock = pygame.time.Clock()
    win = pygame.display.set_mode((screenWidth,screenHeight))
    pygame.display.set_caption("First Game")
    player = mainCharacter(screenWidth/3, screenHeight - (screenHeight/10 * 7), 64, 64)
    pipeList = []
    pipe = obstacle()
    pipeList.append(pipe)

    tickCount = 0
    global gamestate
    global isJumping
    while gamestate == 1:
        clock.tick(30)
        tickCount += 1
        pipe.x -= obstacleSpeed

        if tickCount % distanceBetweenObstacles == 0:
            pipe = obstacle()
            pipeList.append(pipe)
            tickCount = 0
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        keys = pygame.key.get_pressed()

        if isJumping == False:      
            if keys[pygame.K_SPACE]:
                isJumping = True
                player.gravity(False)  
                while player.jumpCount >= 0:
                    player.y -= (player.jumpCount * abs(player.jumpCount)) * 0.5
                    player.jumpCount -= 1
                player.jumpCount = jumpStrength
                #player.gravity(True)

        if keys[pygame.K_ESCAPE]:
            pygame.QUIT
            pygame.quit()

        isJumping = False  
        player.gravity(True)
        
        redrawGameWindow(win, player, pipeList)


    while gamestate == 0:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamestate == "exit"
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            pygame.QUIT
            pygame.quit()
        
        if keys[pygame.K_RETURN]:
            global score
            score = 0
            gamestate = 1


        redrawGameOver(win)
    
    if gamestate == 1:
        game()

game()