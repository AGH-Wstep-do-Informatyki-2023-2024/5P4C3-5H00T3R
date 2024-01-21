import pygame
import random
from .animations import GridSheetAnim
from .config import cfg
class Enemy(pygame.sprite.Sprite):
    def __init__(self, hp, damage, score_val):
        super().__init__()

        self.rect = pygame.Rect(0, 0, 64, 64)
        self.anim_handler = GridSheetAnim(pygame.image.load("img/spritesheets/Enemy_Basic.png"), 5, 5,
                                                     self.rect.width, self.rect.height, 1)
        self.rect.center = (random.randint(40, cfg.SCREEN_WIDTH - 40), 0)
        self.hp = hp
        self.damage = damage
        self.score_val = score_val

    def move(self, vel=2):
        self.rect.move_ip(0, vel)
        if self.rect.bottom > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)

    def draw(self, surface):
        self.anim_handler.draw(surface, self.rect.topleft)