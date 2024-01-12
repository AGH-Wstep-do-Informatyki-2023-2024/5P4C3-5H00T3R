import pygame
from .config import cfg
clock = pygame.time.Clock()
dt = clock.tick(cfg.FPS)

def signum(x):
    return 0.0 if abs(x) == 0 else x / abs(x)
projectiles = pygame.sprite.Group()