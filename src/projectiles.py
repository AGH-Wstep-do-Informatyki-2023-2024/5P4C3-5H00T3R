import pygame
from .animations import CyclicAnim

class Projectile(pygame.sprite.Sprite):
    def __init__(self, coord):
        super().__init__()
        self.anim_handler = CyclicAnim(pygame.image.load("img/spritesheets/projectile.png"), [5], 10, 15, 30, 1)
        self.rect = pygame.Rect(0, 0, 15, 30)
        self.rect.center = coord
        self.velocity = 8
        self.damage = 1

    def move(self):
        self.rect.move_ip(0, self.velocity * -1)
        if self.rect.centery < 1:
            self.kill()

    def hit(self):
        self.kill()

    def draw(self, surface):
        self.anim_handler.draw(surface, self.rect.topleft)
