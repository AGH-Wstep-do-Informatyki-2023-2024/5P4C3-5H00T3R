import pygame, sys
from pygame.locals import *
from src import animations
from .config import cfg
from .colors import RGB
from .fun import *
from .ui import Fonts
from .gameinit import *
from .projectiles import Projectile
from .score import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Sprite
        self.rect = pygame.Rect(0, 0, 64, 64)
        self.anim_handler = animations.GridSheetAnim(pygame.image.load("img/Player_spritesheet.png"), 5, 5,
                                                     self.rect.width, self.rect.height, 1)
        self.rect.center = (160, 520)
        # Stats
        self.hp = 10
        self.cooldown_var = 0
        self.cooldown_stat = 20
        self.score = Score()
        # Physics
        self.speed = 0.08  # deprecated I guess # jednak nie
        self.drag = 0.07
        self.base_acceleration = 0.75
        self.velocity = (0, 0)  # Speed of spaceship
        self.is_thruster_running = False
        self.thrust_vector = (0, 0)  # Direction of acceleration
        self.vel_vector = (0, 0)  # Velocity
        self.accel_low_border = 0.4  # lower values will make acceleration unpredictable
        self.dbg = 0

    # class Physics:
    #     def __init__(self):
    #         super().__init__()
    def normalize_thrust_and_velocity_vector(self):
        # THRS_VEC
        dlg = ((self.thrust_vector[0] ** 2 + self.thrust_vector[1] ** 2) ** (1 / 2))  # length of thrust vector
        x, y = self.thrust_vector
        try:
            x = x / dlg
        except Gayming:
            x = 0
        try:
            y = y / dlg
        except Gayming:
            y = 0
        self.thrust_vector = (x, y)
        ## VEL_VEC
        dlg = ((self.velocity[0] ** 2 + self.velocity[1] ** 2) ** (1 / 2))
        x, y = self.velocity
        try:
            x = x / dlg
        except Gayming:
            x = 0
        try:
            y = y / dlg
        except Gayming:
            y = 0
        self.vel_vector = (x, y)

    def calculate_drag(self):
        erm = 1.0 - self.drag
        self.velocity = (erm * self.velocity[0], erm * self.velocity[1])

    def update_phys(self):
        # self.thrust_vector = (self.thrust_vector[0], self.thrust_vector[1])
        # limited acceleratoion
        x, y = self.thrust_vector
        z, q = self.vel_vector
        l = z + x
        k = y + q
        vec_sum = (l, k)
        # vec_sum = tuple( x + y for x, y in zip(self.vel_vector, self.thrust_vector))
        PITAGORAS = (vec_sum[0] ** 2 + vec_sum[1] ** 2) ** (1 / 2)
        p, o = vec_sum
        try:
            p = (vec_sum[0] / PITAGORAS)
        except:
            p = 0
        try:
            o = (vec_sum[1] / PITAGORAS)
        except Gayming:
            p = 0
        vec_sum = (p, o)  # Normalized
        if cfg.debug:
            self.dbg = Fonts.default.render(str(vec_sum) + str(p), True, RGB.BLUE)
        accel = (0, 0)  # IS THAT A SERIAL EXPERIMENTS LAIN REFERENCE O_O??!
        b, n = accel
        b = self.base_acceleration * (1 / (abs(vec_sum[0]) + self.accel_low_border))
        n = self.base_acceleration * (1 / (abs(vec_sum[1]) + self.accel_low_border))
        accel = (b, n)
        if self.is_thruster_running:
            g, h = self.velocity
            g += signum(x) * (accel[0] * self.speed)
            h += signum(y) * (accel[1] * self.speed)
            self.velocity = (g, h)
        self.calculate_drag()

    def shoot(self):
        global projectiles
        proj = Projectile((self.rect.center[0], self.rect.center[1] - round(self.rect.height / 2)))
        projectiles.add(proj)

    def update(self):
        self.is_thruster_running = False
        pressed_keys = pygame.key.get_pressed()
        if self.cooldown_var > 0:
            self.cooldown_var -= 1

        j, k = self.thrust_vector  # j = horizontal; k = vertical
        j = 0
        k = 0
        if pressed_keys[K_UP]:
            k = -1
            self.is_thruster_running = True
        if pressed_keys[K_DOWN]:
            k = 1 + k
            self.is_thruster_running = True
        if pressed_keys[K_RIGHT]:
            j = 1
            self.is_thruster_running = True
        if pressed_keys[K_LEFT]:
            j = -1 + j
            self.is_thruster_running = True
        if not self.is_thruster_running:
            self.thrust_vector = (0, 0)
        # APPLY TO THRUST_VEC
        self.thrust_vector = (j, k)
        # AFTER INPUT
        self.normalize_thrust_and_velocity_vector()  # Normalizes input and velocity vector :3 ## trochę chaos :c
        self.update_phys()

        if self.rect.right > cfg.SCREEN_WIDTH:
            self.velocity = ((cfg.SCREEN_WIDTH - self.rect.right) * 0.2, self.velocity[1])
        if self.rect.left < 0:
            self.velocity = (self.rect.left * -0.2, self.velocity[1])
        if self.rect.bottom > cfg.SCREEN_HEIGHT:
            self.velocity = (self.velocity[0], (cfg.SCREEN_HEIGHT - self.rect.bottom) * 0.2)

        if self.rect.top < 0:
            self.velocity = (self.velocity[0], self.rect.top * -0.2)

        if pressed_keys[K_SPACE] and not self.cooldown_var:
            self.shoot()
            self.cooldown_var = self.cooldown_stat
        # print(self.velocity)
        self.rect.move_ip(self.velocity[0] * dt, self.velocity[1] * dt)

        # Animation
        self.anim_handler.update(self.thrust_vector, 0.7)
        # TODO: Ease in and out of acceleration - implement anim vector

    def draw(self, surface):
        self.anim_handler.draw(surface, self.rect.topleft)
        # surface.blit(self.image, self.rect)
        # surface.blit(self.dbg, (20, 20))
        # TODO: tu sterowanie przejmuje klasa GridSheetAnim
