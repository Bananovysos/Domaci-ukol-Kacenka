import pygame
import os
from sys import exit
import random
pygame.init()

canvasW = 1024
canvasH = 512
gameActive = True
dead = False
FPS = 60
floorPos = canvasH - 152

score = 0
highScore = 0
runTime = pygame.time.get_ticks() / 1000
scoreMinus = 0

duckX = 250
duckY = floorPos
eggX = 500
eggY = floorPos
spaceCount = 0

crocX = 1024
crocY = floorPos
crocSpeed = 5

canvas = pygame.display.set_mode((canvasW, canvasH))
pygame.display.set_caption("Skakajici kacenka")
clock = pygame.time.Clock()

skySurface = pygame.image.load("sunandskyfull.png")

mountainsSurface = pygame.image.load("pozadifull.png").convert_alpha()
mountainsRect = mountainsSurface.get_rect(topleft = (0, 0))
mountainsRect2 = mountainsSurface.get_rect(topleft = (2048, 0))

duck = pygame.image.load("kacenkafull.png").convert_alpha()
duckRect = duck.get_rect(bottomleft = (duckX, duckY))
duckGrav = 0
croc = pygame.image.load("krokodylfull.png").convert_alpha()
crocRect = croc.get_rect(bottomleft = (crocX, crocY))


music = pygame.mixer.music.load("hlavni znelka.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
deathMusic = pygame.mixer.Sound("zvuksmrt.mp3")
deathMusic.set_volume(0.2)
skok = pygame.mixer.Sound("skok.mp3")
skok.set_volume(1)

scoreFont = pygame.font.Font(None, 75)
scoreText = scoreFont.render(f"TIME: {score}", False, "black")
scoreRect = scoreText.get_rect(topleft = (10, 10))

highScoreFont = pygame.font.Font(None, 75)
highScoreText = scoreFont.render(f"HIGHSCORE: {highScore}", False, "black")
highScoreRect = scoreText.get_rect(topright = (800, 10))

deathFont = pygame.font.Font(None, 75)
deathText = deathFont.render("GAME OVER", False, "Red")
deathRect = deathText.get_rect(center = (canvasW/2, canvasH/2 - 140))
continueFont = pygame.font.Font(None, 40)
continueText = continueFont.render("""Press "space" to continue""", False, "white")
continueRect = continueText.get_rect(center = (canvasW/2, canvasH/2 - 60))
DeadHighScoreFont = pygame.font.Font(None, 40)
DeadHighScoreText = DeadHighScoreFont.render(f"HIGHSCORE: {highScore}", False, "white")
DeadHighScoreRect = DeadHighScoreText.get_rect(center = (canvasW/2, canvasH/2 - 20))


def reset():
    global score
    global scoreMinus
    global mountainsRect
    global mountainsRect2
    crocRect.x = 1024
    duckRect.bottom = floorPos
    scoreMinus = 0
    scoreMinus += runTime
    score -= scoreMinus
    mountainsRect.x = 0
    mountainsRect2.x = 2048
    pygame.mixer.music.play(-1)



def NPCmovement():
    global crocSpeed
    if score < 60: 
        crocRect.left -= crocSpeed 
    elif score > 60:
        crocRect.left -= crocSpeed + 2
    elif score > 120: 
        crocRect.left -= crocSpeed + 4
    elif score > 180: 
        crocRect.left -= crocSpeed + score/15

    if crocRect.right < -100:
        crocRect.left = canvasW
        crocSpeed = random.randrange(6, 12, 1)

def movement():
    global duckGrav
    global spaceCount
    global duckRect
    global gameActive
    if event.type == pygame.KEYDOWN and gameActive == True:
        if event.key == pygame.K_SPACE and spaceCount < 2:
            duckGrav -= 15
            spaceCount += 1
            skok.play()
    else:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                reset()
                gameActive = True
    
def death():
    global gameActive
    if crocRect.colliderect(duckRect):
        gameActive = False
        pygame.mixer.music.stop()
        deathMusic.play()

    
def draw():
    global mountainsRect
    global mountainsRect2
    global scoreText
    global highScoreText
    global runTime
    global score
    canvas.blit(skySurface, (0,0))
    canvas.blit(mountainsSurface, (mountainsRect))
    canvas.blit(mountainsSurface, (mountainsRect2))
    if mountainsRect.right < 0: mountainsRect.left = mountainsRect2.right
    if mountainsRect2.right < 0: mountainsRect2.left = mountainsRect.right

    canvas.blit(duck, (duckRect))
    canvas.blit(croc, (crocRect))
    canvas.blit(scoreText, (scoreRect))
    canvas.blit(highScoreText, (highScoreRect))
    
    highScoreText = scoreFont.render(f"HIGHSCORE: {highScore}", False, "black")
    score = int(runTime - scoreMinus)
    scoreText = scoreFont.render(f"TIME: {score}", False, "black")
    mountainsRect.x -= 1
    mountainsRect2.x -= 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        movement() 
    runTime = pygame.time.get_ticks() / 1000
    if gameActive:
        dead = False
        deathMusic.stop()
        NPCmovement() 
        draw() 
        death() 
        duckGrav += 0.4
        duckRect.y += duckGrav
        if duckRect.bottom > floorPos: 
            duckRect.bottom = floorPos
            duckGrav = 0
            spaceCount = 0
        if duckRect.top < 0:
            duckRect.top = 0
            duckGrav = 0
        if score > highScore:
            highScore = score
        
    else:
        dead = True
        canvas.fill("black")
        canvas.blit(deathText, (deathRect))
        canvas.blit(continueText, (continueRect))
        DeadHighScoreText = DeadHighScoreFont.render(f"HIGHSCORE: {highScore}", False, "white")
        canvas.blit(DeadHighScoreText, (DeadHighScoreRect))
        reset()



    pygame.display.update()
    clock.tick(FPS)
