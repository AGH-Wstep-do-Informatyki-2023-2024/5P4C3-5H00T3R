from src import animations
from .gameinit import *
from .projectiles import Projectile
from .score import *
from .physics import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Sprite
        self.rect = pygame.Rect(0, 0, 64, 64)
        self.anim_handler = animations.GridSheetAnim(pygame.image.load("img/spritesheets/Spritesheet_Default.png"), 5,
                                                     5,
                                                     self.rect.width, self.rect.height, 1)
        self.rect.center = (160, 520)
        # Stats
        self.hp = 10
        self.cooldown_var = 0
        self.cooldown_stat = 20
        self.score = Score()
        # Physics
        self.acceleration = AccelerationVector()
        self.velocity = VelocityVector(0.95, 0.5)
        self.dbg: pygame.Surface

    def shoot(self):
        global projectiles
        proj = Projectile((self.rect.center[0], self.rect.center[1] - round(self.rect.height / 2)))
        projectiles.add(proj)

    def update(self):
        pressed_keys = pygame.key.get_pressed()

        # movement
        self.velocity.update(self.acceleration, True)  # auto updates acceleration vector

        # wall bouncing
        if self.rect.right > cfg.SCREEN_WIDTH:
            self.velocity.x = (cfg.SCREEN_WIDTH - self.rect.right) * 0.2
        if self.rect.left < 0:
            self.velocity.x = self.rect.left * -0.2
        if self.rect.bottom > cfg.SCREEN_HEIGHT:
            self.velocity.y = (cfg.SCREEN_HEIGHT - self.rect.bottom) * 0.2
        if self.rect.top < 0:
            self.velocity.y = self.rect.top * -0.2

        self.rect.move_ip(self.velocity.x * dt, self.velocity.y * dt)

        # shooting
        if self.cooldown_var > 0:
            self.cooldown_var -= 1
        if pressed_keys[K_SPACE] and not self.cooldown_var:
            self.shoot()
            self.cooldown_var = self.cooldown_stat

        # Animation
        self.anim_handler.update(self.velocity, 0.48, 0.2)

        # TODO: Change hitbox to fit with alpha clipped sprite - pygame mask

    def draw(self, surface: pygame.Surface):
        self.anim_handler.draw(surface, self.rect.topleft)
        # Tu sterowanie przejmuje klasa GridSheetAnim
