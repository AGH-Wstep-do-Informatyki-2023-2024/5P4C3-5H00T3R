import pygame,sys
from pygame.locals import *
from .config import cfg
from .colors import RGB
from .ui import fonts
from .player import Player

class Debug_Menu(pygame.sprite.Sprite):
    def __init__(self,_Player: Player):
        super().__init__()
        self.sel = int(0)
        self.timeout = 0
        self.tresc = ""
        self.toggle = False

        self.plr = _Player
        self.plr_old_HP = int(_Player.hp)

        infinite_HP = self.boolsetting("Toggle infinite HP", False, self.Make_player_invincible)
        enemy_spawn = self.boolsetting("Toggle enemy spawn", False, print())
        Debug_hud = self.boolsetting("Toggle debug HUD", False, print())
        self.pause = False
        
        self.settings = []
        self.settings.append(infinite_HP)
        self.settings.append(enemy_spawn)
        self.settings.append(Debug_hud)

        

        self.Checkbox = []
        self.Checkbox.append("[ ] ")
        self.Checkbox.append("[x] ")
    class boolsetting:
        def __init__(self, name : str, defaultbool : bool,func):
            self.name = name
            self.toggle = defaultbool
            self.fun = func
        def do(self):
            self.fun(self.toggle)
    def Make_player_invincible(self, toggle : bool ):
        if toggle:
            self.plr.hp = int("0111111111111111111111111111111111111111111111111111111111111111",base=2)
        else:
            self.plr.hp = self.plr_old_HP
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
            self.timeout = int(cfg.FPS/2)
        
        if self.toggle:
            if pressed_keys[K_UP]and self.timeout <= 0:
                if self.sel > 0:
                    self.sel -= 1
                self.timeout = int(cfg.FPS/4)
            if pressed_keys[K_DOWN]and self.timeout <= 0:
                if self.sel < len(self.settings)-1:
                    self.sel += 1
                    self.timeout = int(cfg.FPS/4)
            if pressed_keys[K_t] and self.timeout <= 0:
                self.timeout = int(cfg.FPS/4)
                self.settings[self.sel].toggle = not self.settings[self.sel].toggle
                self.settings[self.sel].do()
        if self.timeout > 0:
            self.timeout -= 1
        
    def Spawn_Enemy():
        pass
    def draw(self, surface):
        if self.toggle:
            self.tresc = self.Create_String().split('\n')
            for meow in range(len(self.tresc)):
                img = fonts.Default.render(self.tresc[meow], True, RGB.BLACK)
                surface.blit(img, (20, 80+(24*meow)))
