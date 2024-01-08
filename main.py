import pygame, sys
from pygame.locals import *
import random

# from PygameShader.shader import dithering # might not be useful # not used for now


# import player
# import enemies
# import projectiles

# syf
debug = True

# init
Hell = ValueError
Gayming = ZeroDivisionError
pygame.init()
FramePerSec = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# Predefined some colors
from src import colors

# Screen information
FPS = 120
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Window stuff
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(colors.RGB.WHITE)
pygame.display.set_caption("Kosmiczne elfy amarena giera")

# test czy dziala
clock = pygame.time.Clock()
dt = clock.tick(FPS)


######## CLASS STUFF #############
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


class Debug_Menu(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sel = int(0)
        self.timeout = 0
        self.tresc = ""
        self.toggle = False
        infinite_HP = self.boolsetting("Toggle infinite HP", False)
        enemy_spawn = self.boolsetting("Toggle enemy spawn", False)
        Debug_hud = self.boolsetting("Toggle debug HUD",False)
        self.pause = False
        
        self.settings = []
        self.settings.append(infinite_HP)
        self.settings.append(enemy_spawn)

        self.Checkbox = []
        self.Checkbox.append("[ ] ")
        self.Checkbox.append("[x] ")
    class boolsetting:
        def __init__(self, name : str, defaultbool : bool):
            self.name = name
            self.toggle = defaultbool
    def Create_String(self):
        cool = ""
        erm = 0
        for setti in self.settings:
            if self.sel == erm:
                cool += '>'
            if setti.toggle:
                cool += self.Checkbox[1]
            else:
                cool += self.Checkbox[0]
            cool += setti.name
            cool += '\n'
            erm +=1
        return cool
    def update(self):
        pressed_keys = pygame.key.get_pressed()
        
        if pressed_keys[K_F8] and self.timeout <= 0:
            self.toggle = not self.toggle
            self.timeout = int(FPS/2)
        
        if self.toggle:
            if pressed_keys[K_UP]and self.timeout <= 0:
                if self.sel > 0:
                    self.sel -= 1
                self.timeout = int(FPS/4)
            if pressed_keys[K_DOWN]and self.timeout <= 0:
                if self.sel < len(self.settings):
                    self.sel += 1
                    self.timeout = int(FPS/4)
            if pressed_keys[K_t] and self.timeout <= 0:
                self.timeout = int(FPS/4)
                self.settings[self.sel].toggle = not self.settings[self.sel].toggle
        if self.timeout > 0:
            self.timeout -= 1
        
    def Spawn_Enemy():
        pass
    def draw(self, surface):
        if self.toggle:
            self.tresc = self.Create_String().split('\n')
            for meow in range(len(self.tresc)):
                img = font.render(self.tresc[meow], True, colors.RGB.BLACK)
                surface.blit(img, (20, 80+(24*meow)))

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
        # Stats
        self.hp = 10
        self.cooldown_var = 0
        self.cooldown_stat = 20
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
        if debug == True:
            self.dbg = font.render(str(vec_sum) + str(p), True, colors.RGB.BLUE)
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

        if self.rect.right > SCREEN_WIDTH:
            self.velocity = ((SCREEN_WIDTH - self.rect.right) * 0.2, self.velocity[1])
        if self.rect.left < 0:
            self.velocity = (self.rect.left * -0.2, self.velocity[1])
        if self.rect.bottom > SCREEN_HEIGHT:
            self.velocity = (self.velocity[0], (SCREEN_HEIGHT - self.rect.bottom) * 0.2)

        if self.rect.top < 0:
            self.velocity = (self.velocity[0], self.rect.top * -0.2)

        if pressed_keys[K_SPACE] and not self.cooldown_var:
            self.shoot()
            self.cooldown_var = self.cooldown_stat
        # print(self.velocity)
        self.rect.move_ip(self.velocity[0] * dt, self.velocity[1] * dt)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.dbg, (20, 20))
######## FUNCTIONS ##############


def update_state():
    P1.update()
    DebugMenu.update()
    for enemy in enemies:
        enemy.move()
    for projectile in projectiles:
        projectile.move()

def signum(x):
    return 0.0 if abs(x) == 0 else x / abs(x)

def redraw_game_window():
    DISPLAYSURF.fill((255, int(P1.hp * 255 / 10), int(P1.hp * 255 / 10)))

    P1.draw(DISPLAYSURF)

    for enemy in enemies:
        enemy.draw(DISPLAYSURF)

    for projectile in projectiles:
        projectile.draw(DISPLAYSURF)
    DebugMenu.draw(DISPLAYSURF)
    pygame.display.update()


######## VARIABLES ###############


P1 = Player()
E1 = Enemy()
SCORE = 0
enemies = pygame.sprite.Group()
enemies.add(E1)
projectiles = pygame.sprite.Group()
DebugMenu = Debug_Menu()

# MAIN LOOP
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

    dt = clock.tick(FPS)
    redraw_game_window()
    FramePerSec.tick(FPS)
