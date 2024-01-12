import pygame


# from .config import cfg
# from .gameinit import * # Na później

class Projectile(pygame.sprite.Sprite):
    def __init__(self, coord):
        super().__init__()
        self.image = pygame.image.load("img/Bullet.png")
        self.rect = self.image.get_rect()
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
        surface.blit(self.image, self.rect)