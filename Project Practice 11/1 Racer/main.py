import pygame, sys
from pygame.locals import *
import random, time

# Initialzing 
pygame.init()

# Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Other Variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COIN_SCORE = 0
N_COINS_FOR_SPEEDUP = 5  # Increase speed every N coins

# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")

DISPLAYSURF = pygame.display.set_mode((400,600))
pygame.display.set_caption("Game")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.bottom > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self, enemy):
        super().__init__() 
        self.enemy = enemy
        self.weight = 1
        self.image = pygame.image.load("Coin.png") 
        self.rect = self.image.get_rect()
        self.reset()

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.bottom > 600):
            self.reset()

    def reset(self):
        self.rect.top = 0
        # Randomize weight: 80% chance for weight 1, 20% for weight 3
        self.weight = random.choices([1, 3], weights=[80, 20])[0]
        
        # Visually differentiate weights (scaling the image)
        size = 20 if self.weight == 1 else 35
        self.image = pygame.transform.scale(pygame.image.load("Coin.png"), (size, size))
        
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
        
        # Ensure coin doesn't spawn exactly on top of enemy
        while abs(self.rect.center[0] - self.enemy.rect.center[0]) < 30:   
            self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

# Setup Sprites
P1 = Player()
E1 = Enemy()
C1 = Coin(E1)
C2 = Coin(E1)

enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
coins.add(C2)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1, C2)

# Speed timer 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.2 # Slight passive increase      
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(f"Enemies: {SCORE}", True, BLACK)
    coin_score = font_small.render(f"Coins: {COIN_SCORE}", True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    DISPLAYSURF.blit(coin_score, (SCREEN_WIDTH - 120, 10))

    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)
        
    # Enemy Collision
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()        
    
    # Coin Collision
    collided_coin = pygame.sprite.spritecollideany(P1, coins)
    if collided_coin:
        pygame.mixer.Sound('coin_pickup.wav').play()
        
        # Add weight value to total score
        COIN_SCORE += collided_coin.weight
        
        # Increase enemy speed every N coins earned
        if COIN_SCORE % N_COINS_FOR_SPEEDUP == 0:
            SPEED += 1 
            
        collided_coin.reset()

    pygame.display.update()
    FramePerSec.tick(FPS)
