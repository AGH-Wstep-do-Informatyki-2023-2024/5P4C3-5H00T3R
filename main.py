import pygame
import sys
from pygame.locals import *

# initialize engine
pygame.init()
FramePerSec = pygame.time.Clock()

# continue imports that need pygame engine
from src import animations
from src import debugmenu as DbgM
from src.player import Player
from src.enemies import Enemy
from src.gameinit import *
from src.config import cfg
from src.score import *
from src import colors

# from src.fun import *
# from PygameShader.shader import dithering # might not be useful # not used for now
# from src.ui import fonts


# display settings
DISPLAYSURF = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
DISPLAYSURF.fill(colors.RGB.BLACK)
pygame.display.set_caption("Kosmiczne statki amarena giera ALPHA")


def update_state():
    P1.update()
    DebugMenu.update()
    for enemy in enemies:
        enemy.move()
    for projectile in projectiles:
        projectile.move()


def spawn_enemy(hp=2, damage=1, score_val=10):
    global enemies
    enemies.add(Enemy(hp, damage, score_val))
    print("Spawned new enemy!")


def redraw_game_window():
    # Background
    DISPLAYSURF.fill(colors.RGB.BLACK)
    BG.update()
    BG.draw(DISPLAYSURF)

    # Players
    P1.draw(DISPLAYSURF)

    for enemy in enemies:
        enemy.draw(DISPLAYSURF)

    for projectile in projectiles:
        projectile.draw(DISPLAYSURF)

    # Scores
    P1.score.draw(DISPLAYSURF)

    DebugMenu.draw(DISPLAYSURF)

    pygame.display.update()


# defining game objects
P1 = Player()
E1 = Enemy(2, 1, 10)
SCORE = 0
enemies = pygame.sprite.Group()
enemies.add(E1)
DebugMenu = DbgM.DebugMenu(P1)
BG = animations.BgAnim(DISPLAYSURF.get_height(), "img/bckg/Default/Moon.png", "img/bckg/Default/Galaxy.png",
                       "img/bckg/Default/Stars.png", 10, 20,
                       30)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    update_state()

    coll_enemy = pygame.sprite.spritecollideany(P1, enemies)
    if coll_enemy:
        # print(coll_enemy)
        P1.hp -= coll_enemy.damage
        coll_enemy.kill()
        spawn_enemy()
        if P1.hp == 0:
            pygame.quit()
            sys.exit()

    coll = pygame.sprite.groupcollide(enemies, projectiles, False, True)
    if coll:
        # print(coll)
        for enemy in coll.keys():
            enemy.hp -= 1
            # print(enemy, enemy.hp)
            if enemy.hp == 0:
                P1.score.increase(enemy)
                enemy.kill()
                spawn_enemy(2, 1, 10)

    dt = clock.tick(cfg.FPS)
    redraw_game_window()
    FramePerSec.tick(cfg.FPS)
