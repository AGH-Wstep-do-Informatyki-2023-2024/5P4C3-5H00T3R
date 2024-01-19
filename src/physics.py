import pygame
from pygame.locals import *


class AccelerationVector:
    def __init__(self):
        self.x = 0
        self.y = 0
        pass

    def update(self):
        self.x = 0
        self.y = 0
        # get user input and adjust vector accordingly:
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.y = -1
        if pressed_keys[K_DOWN]:
            self.y = 1
        if pressed_keys[K_LEFT]:
            self.x = -1
        if pressed_keys[K_RIGHT]:
            self.x = 1

        # dividing by sqrt(2) when moving on diagonal:
        if self.y != 0 and self.x != 0:
            self.x = self.x / 1.4142135623747
            self.y = self.y / 1.4142135623747
        pass


class VelocityVector:
    def __init__(self, drag_coeff: float, max_vel: float):
        """

        :param drag_coeff: Should be < 1. defines to what degree drag will affect the velocity represented by
        a VelocityVector object. In conjunction with AccelerationVector it caps velocity at an equilibrium point.
        In practice drag is used when calculating velocity by multiplying x and y components of the velocity vector by
        the drag value: (vel * drag)
        :param max_vel: added just in case for now, might get used soon.
        """

        self.x = 0
        self.y = 0

        if 0 > drag_coeff > 1:
            raise ValueError(f"Drag value components must be between 1 and 0; Current value: {drag_coeff}")
        self.drag_coeff = drag_coeff
        self.drag_vect = (0, 0)

        self.max = max_vel
        self.bounce_slowdown = 1.2

    def update(self, acc_vect: AccelerationVector, update_acc_vector: bool = False):
        self.drag_vect = (self.x * (1 - self.drag_coeff), self.y * (1 - self.drag_coeff))
        self.x -= self.drag_vect[0]  # <=> self.x = self.x * self.drag_coeff
        self.y -= self.drag_vect[1]  # the order matters here - drag should not affect acceleration vector
        if update_acc_vector:
            acc_vect.update()
        self.x += acc_vect.x  # <=> x * acc_factor, acc_factor > 1
        self.y += acc_vect.y

        # zeroing vector when infinitesimally close to being stationary and thresholding if velocity too high
        if -0.01 < self.x < 0.01:
            self.x = 0
        elif self.max < self.x:
            self.x = self.max
        elif -1 * self.max > self.x:
            self.x = -1 * self.max

        if -0.01 < self.y < 0.01:
            self.y = 0
        elif self.max < self.y:
            self.y = self.max
        elif -1 * self.max > self.y:
            self.y = -1 * self.max

        # TODO: add bouncing off walls
