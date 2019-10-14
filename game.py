import pygame
import random
pygame.init()

width = 1000
height = 500
screen = pygame.display.set_mode((width,height))

#white = 255,255,255
#red = 255,0,0
#black = 0,0,0
#blue = 0,0,255
#green = 0,255,0
count = 0
n=5
def score(count):

    font = pygame.font.SysFont(None, 30)
    text = font.render("Score : {}".format(count), True, black)
    screen.blit(text, (width-100, 0))
def gameover():
    font = pygame.font.SysFont(None, 100)
    text = font.render("GAME OVER", True, black)
    screen.blit(text, (width/2-200, height/2-50))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50,50))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.center = width/2, height/2
        self.rect.y = height - 60
        self.moveX = 0
        self.playerHealth = 100

    def update(self):
        if self.playerHealth > 0:
            keypressed = pygame.key.get_pressed()
            if keypressed[pygame.K_RIGHT]:
                self.moveX = 4
            elif keypressed[pygame.K_LEFT]:
                self.moveX = -4
            else:
                self.moveX = 0

            self.rect.x += self.moveX

            self.hit = pygame.sprite.groupcollide(playerGroup,enemyGroup,False,True)
            if self.hit:
                self.playerHealth -= 10

            if self.rect.x > width+50:
                self.rect.x = -50
            elif self.rect.x < -50:
                self.rect.x = width
        
                #self.moveX = 0
        else:
            gameover()
            self.moveX = 0
            

    def triggerBullet(self):
        bullet = Bullet(self.rect.x, self.rect.y)
        all_sprites.add(bullet)
        bulletGroup.add(bullet)
        
            


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50,50))
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,width-50)
        self.rect.y = random.randint(-height,0)
        self.moveX = 0
        self.moveY = random.randint(1,4)
        

    def update(self):
        self.rect.y += self.moveY
        health = player.playerHealth
        if self.rect.top > height:
            self.rect.x = random.randint(0, width - 50)
            self.rect.y = random.randint(-height, 0)
            if health >0:
                self.moveY = random.randint(1, 4)
            else:
                self.moveY = 0
                self.rect.y = -height-100
                

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect.x = x + 22
        self.rect.y = y
        self.moveY = 5

    def update(self, *args):
        self.rect.y -= self.moveY
        if self.rect.bottom < 0:
            self.kill()

all_sprites = pygame.sprite.Group()
player = Player()
playerGroup = pygame.sprite.Group()
playerGroup.add(player)
all_sprites.add(player)

bulletGroup = pygame.sprite.Group()
enemyGroup = pygame.sprite.Group()

for i in range(20):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemyGroup.add(enemy)

FPS = 100
clock = pygame.time.Clock()

def playerHealth():
    health = player.playerHealth
    if health < 33:
        color = red

    else:
        color = green
    pygame.draw.rect(screen,color,[10,10,health,30])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        health = player.playerHealth
        if health > 0:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.triggerBullet()

    hit = pygame.sprite.groupcollide(bulletGroup,enemyGroup,True,True)
    if hit:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemyGroup.add(enemy)
        count +=1

    screen.fill(white)
    playerHealth()
    
    all_sprites.draw(screen)
    all_sprites.update()
    score(count)
    
    
    pygame.display.update()
    clock.tick(FPS)
