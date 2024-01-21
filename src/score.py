import pygame
from src import config
from src import colors
from src import ui


class Score:
    def __init__(self, score=0):
        self.value = score

    def increase(self, enemy):
        self.value += enemy.score_val

    def draw(self, surface: pygame.surface):
        score_text = ui.Fonts.default.render("Score: " + str(self.value), True, colors.RGB.WHITE)
        surface.blit(score_text, ((config.cfg.SCREEN_WIDTH - score_text.get_width()) / 2, 50))
