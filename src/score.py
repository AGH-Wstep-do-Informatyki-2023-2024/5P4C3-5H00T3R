import pygame
from src import colors
from src import ui


class Score:
    def __init__(self, score=0):
        self.value = score

    def increase(self, enemy):
        self.value += enemy.score_val

    def draw(self, surface: pygame.surface):
        score_text = ui.Fonts.default.render("Score: " + str(self.value), True, colors.RGB.BLACK)
        surface.blit(score_text, (160, 50))
