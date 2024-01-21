import pygame, sys
from pygame.locals import *
from .gameinit import *
from .colors import *
from .fun import *

class Fonts:
    default = pygame.font.SysFont(None, 24)
    consolas = pygame.font.SysFont("consolas", 36)


class MainMenu(pygame.sprite.Sprite): # # Powinni mnie za to spalić na stosie
    def __init__(self):
        super().__init__()
        self.sel = int(0) # selction
        self.menu_state = "main"
        self.difficulty = None
        self.isOn = None
        self.Fun.__init__(self)
        self.menu_main_arr = [
            [self.Option("5T4RT", self.Fun.start_M, None, self)], # Debilizm
            [self.Option("0PT10N5", self.Fun.opt_M, None, self)], # nawet gorzej a to to samo
            [self.Option("Qv1T", self.Fun.quit)]
        ]
        self.menu_start_arr = [
            [self.Option("EASY", self.Fun.set_difficulty, 0, self)],
            [self.Option("NORMAL", self.Fun.set_difficulty, 1, self)],
            [self.Option("HARD", self.Fun.set_difficulty, 2, self)],
            [self.Option("RETURN", self.Fun.main_M, None, self)]
        ]
        self.menu_option_arr = [
            [self.Option("FPS : ",self.Fun.null)],
            [self.Option("Dithering : ", self.Fun.null)],
            [self.Option("RETURN", self.Fun.main_M, None, self)]
        ]
        self.active_arr = self.menu_main_arr
        self.tresc = ""
        #menu_generator(self.menu_arr)
    
    class Option: # poco ja robie te pod klasy to niewiem ale fajnie to wygląda... jak spagetti... chyba zgłodniałam
        def __init__(self, name : str, func, val = None, m = None):
            self.name = name
            self.function = func
            self.pass_val = val
            if self.pass_val != None:
                self.pass_val = int(self.pass_val)
            self.old_keys = 0
            if type(m) == type(None):
                self.me = None
            else:
                self.me = m
        def do(self):
            #
            # try:
            #     self.function()
            # except kałszpula:
            #     #if type(self.pass_val) == type(int):
            #     try:
            #         self.function(self.pass_val)
            #     except kałszpula:
            #         try:
            #             if type(self).me != type(None): 
            #                 self.function(self.pass_val, self.me)
            #         except kałszpula:
            #             print("aha to ja już nie wiem")
            # ERM ciekawe
            print(type(self.pass_val), type(int),)
            if type(self.pass_val) == type(int):
                self.function(pass_val)
            elif (self.pass_val != None and self.pass_val >=0 and type(self.me) != type(None) ):
                self.function(self.me, self.pass_val)
            else:
                try:
                    self.function(self.me)
                except Hell: # tu powinno być cokolwiek a nie tylko ValueError
                    print("erm")
    class Fun:
        def __init__(self):
            self.xd = True
        def null():
            pass
        def quit(self):
            pygame.quit()
            sys.exit()
        def set_difficulty(self, dif): # kałszpula
            self.difficulty = dif
            self.xd = False
        def main_M(self):
            self.menu_state = "main"
        def opt_M(self):
            self.menu_state = "options"
        def start_M(self):
            self.menu_state = "start"
        def get_menuOn(self):
            return bool(self.xd)
    def draw(self, surface):
        for arrI in range(len(self.active_arr)):
            if arrI == self.sel:
                img = Fonts.consolas.render("> " + self.active_arr[arrI][0].name, True, RGB.WHITE)
            else:
                img = Fonts.consolas.render("  " + self.active_arr[arrI][0].name, false, RGB.GREEN)
            surface.blit(img, (20, 80 + (40 * arrI)))
    
    def update(self):
        meow = 0 
        if self.menu_state == "main":
            self.active_arr = self.menu_main_arr
        if self.menu_state == "start":
            self.active_arr = self.menu_start_arr
        if self.menu_state == "options":
            self.active_arr = self.menu_option_arr # ale padaka
        meow = len(self.active_arr)
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_UP] and self.sel > 0 and pressed_keys[K_UP] != self.old_keys[K_UP] :
            self.sel -= 1
        if pressed_keys[K_DOWN] and self.sel < (meow - 1) and pressed_keys[K_DOWN] != self.old_keys[K_DOWN]:
            self.sel += 1
        if pressed_keys[K_SPACE] and pressed_keys[K_SPACE] != self.old_keys[K_SPACE]:
            # if self.menu_state == "main":
            #     if self.sel == 0:
            #         self.menu_state == "start"
            #     if self.sel == 1:
            #         self.menu_state == "option"
            self.active_arr[self.sel][0].do()
            self.sel = 0
        
        self.isOn = self.Fun.get_menuOn(self) # Wyższa łopatologia
        # zapisz stare klawisze żeby wiedzieć kiedy przycisk jest przytrzymany
        self.old_keys = pressed_keys
        
class PauseMenu:
    def __init__(self):
        pass