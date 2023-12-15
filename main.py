import pygame, sys
from pygame.locals import *
import random
# import player
# import enemies
# import projectiles

Hell = ValueError

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Predefined some colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen information
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Kosmiczne elfy amarena giera")


class Projectile(pygame.sprite.Sprite):
    def __init__(self, coord):
        super().__init__()
        self.image = pygame.image.load("img/Bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = coord
        self.velocity = 1
        self.damage = 1

    def move(self):
        self.rect.move_ip(0, self.velocity * -1)
        if self.rect.centery < 1:
            self.kill()

    def hit(self):
        self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("img/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        self.hp = 2
        self.damage = 1

    def move(self, na_gore=False):
        self.rect.move_ip(0, 5)
        if (self.rect.bottom > 600) or na_gore:
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("img/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        self.hp = 10
        self.cooldown = 0

    def shoot(self):
        global projectiles
        proj = Projectile((self.rect.center[0], self.rect.center[1] - round(self.rect.height/2)))
        projectiles.add(proj)

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        # if pressed_keys[K_UP]:
        # self.rect.move_ip(0, -5)
        # if pressed_keys[K_DOWN]:
        # self.rect.move_ip(0,5)
        if self.cooldown > 0:
            self.cooldown -= 1

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

        if pressed_keys[K_SPACE] and not self.cooldown:
            self.shoot()
            self.cooldown = 20

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def update_state():
    P1.update()
    for enemy in enemies:
        enemy.move()
    for projectile in projectiles:
        projectile.move()


def redraw_game_window():
    DISPLAYSURF.fill((255, int(P1.hp * 255 / 10), int(P1.hp * 255 / 10)))

    P1.draw(DISPLAYSURF)

    for enemy in enemies:
        enemy.draw(DISPLAYSURF)

    for projectile in projectiles:
        projectile.draw(DISPLAYSURF)

    pygame.display.update()


P1 = Player()
E1 = Enemy()
# proj1 = Projectile(P1)
SCORE = 0
enemies = pygame.sprite.Group()
enemies.add(E1)
projectiles = pygame.sprite.Group()
# projectiles.add(proj1)  TODO: Zeby projectile nie wyjebywaly gry
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    update_state()

    if pygame.sprite.spritecollideany(P1, enemies):
        E1.move(True)
        P1.hp -= E1.damage

        if P1.hp == 0:
            pygame.quit()
            sys.exit()

    coll = pygame.sprite.groupcollide(enemies, projectiles, False, True)
    if coll:
        print(coll)
        for enemy in coll.keys():
            enemy.hp -= 1
            print(enemy, enemy.hp)
            if enemy.hp == 0:
                enemy.kill()


    redraw_game_window()
    FramePerSec.tick(FPS)
