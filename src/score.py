import pygame
from src import colors
from src import ui
class Score:
    def __init__(self, score=0):
        self.score = score

    def increase(self, enemy):
        self.score += enemy.score_val

    def draw(self, surface:pygame.surface):
        score_text = ui.font.render("Score: " + str(self.score), True, colors.RGB.BLACK)
        surface.blit(score_text, (160, 50))
