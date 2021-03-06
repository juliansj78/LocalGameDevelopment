import pygame
import random
import math
from pygame import mixer


# Initialize the pygame
pygame.init()

#create the screen

screen = pygame.display.set_mode((800,600))

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('./images/ufo.png')
pygame.display.set_icon(icon)

#Background
background = pygame.image.load('./images/background2.png')

#Background music
mixer.music.load('./sounds/background.wav')
mixer.music.play(-1)

#Player
playerImg = pygame.image.load('./images/space-invaders-64.png')
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemyImg = []
enemyExplosion = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 8
remaining_enemies = num_of_enemies
enemyExplosion =pygame.image.load('./images/explosion64.png')

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('./images/space-invader-icon-64.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(16)
    enemyY_change.append(40)

# Bullet 
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('./images/bunny16.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 20
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score = font.render("Score :" + str(score_value),True, (255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER",True, (255,255,255))
    screen.blit(over_text,(200,250))

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x + 16, y + 10))

def isCollision(enemyX,enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance <27:
       # screen.blit(enemyExplosion,(enemyX,enemyY))
        return True
    else: 
        return False

# Game Loop
running = True
while running:

   #RGB - Red, Green, Blue (values 0-255)
    screen.fill((0, 0, 0))
    #Background image
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            running = False
     #if keystroke is pressed check whether its right or left
        if event.type ==pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('./sounds/laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key ==pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change   
 # Player boundaries according to display settings               
    
    if playerX <= 0:
        playerX =0
    elif playerX >= 736:
        playerX = 736

# Enemy movement
    for i in range(num_of_enemies):
        # Game Over
        
       # if remaining_enemies<1:
        #    game_over_text()
        if enemyY[i] > 400:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break

        enemyX[i] += enemyX_change[i]       
        if enemyX[i] <= 0:
            enemyX_change[i] = 10
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -10
            enemyY[i] += enemyY_change[i]

# Collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_Sound = mixer.Sound('./sounds/explosion.wav')
            explosion_Sound.play()
            screen.blit(enemyExplosion,(enemyX[i],enemyY[i]))
            bulletY=480
            bullet_state="ready"
            score_value += 1
            #uncomment next two lines to respawn enemies at random coordinates
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)

            #enemyY[i] = -2000
            remaining_enemies +=-1 

            
        enemy(enemyX[i],enemyY[i], i)

# Bullet movement
 
    if bulletY <=0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change 

    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()





