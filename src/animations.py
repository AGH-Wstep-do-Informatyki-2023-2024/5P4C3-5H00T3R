import pygame
from src import physics
from src import colors


class SpriteSheet:  # przechowuje sprite sheet
    def __init__(self, spritesheet_image):
        # load spritesheet image from path
        self.sheet = spritesheet_image

    def get_image(self, x, width, height, scale):
        # make empty surface the size of our sprite
        image = pygame.Surface((width, height)).convert_alpha()
        image.fill((0, 0, 0, 0))

        # draw an animation frame onto the surface
        image.blit(self.sheet, (0, 0), ((x * width), 0, width, height))

        # scale the sprite image
        image = pygame.transform.scale(image, (width * scale, height * scale))

        # # keying out the background colour
        # image.set_colorkey(key_col)  # <---- unused
        return image


"""
class Animation:
    def __init__(self, sprite_sheet_img, sprite_width, sprite_height, scale):
        self.sprite_sheet = SpriteSheet(sprite_sheet_img)
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.sprite_scale = scale
        pass

    def update(self):
        pass

    def draw(self):
        pass
"""


# TODO: dziedziczenie wszystkich klas animacji po tej klasie (maybe...)


class GridSheetAnim:  # Animacje na bazie wektora przyspieszenia
    def __init__(self, sprite_sheet_img, sheet_frames_h, sheet_frames_v, sprite_width, sprite_height, scale):

        # sheet parameters
        self.sprite_sheet = SpriteSheet(sprite_sheet_img)
        self.frames_h = sheet_frames_h
        self.frames_v = sheet_frames_v

        # sprite parameters
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.sprite_scale = scale

        # frame container and parameters
        self.frame = ((self.frames_h - 1) // 2, (self.frames_v - 1) // 2)
        self.frames = []

        # extracting frames from sprite sheet
        for y in range(self.frames_h):  # numer rzedu w tabeli frames
            temp_frame_list = []
            for x in range(self.frames_v):  # indeks w rzedzie w tabeli frames
                temp_frame_list.append(
                    self.sprite_sheet.get_image((y * self.frames_h + x), self.sprite_width, self.sprite_height,
                                                self.sprite_scale))
            self.frames.append(temp_frame_list)
        pass

    def frame_xy_from_accel_vect(self, accel_vector, transition_threshold: float,
                                 standing_threshold: float):
        # wybiera ktore klatki wyswietlac na podstawie wektora przyspieszenia

        x, y = (self.frames_h - 1) // 2, (self.frames_v - 1) // 2

        # mapping x component of acceleration vector to frame coordinates (horizontal movement)
        if accel_vector.x > transition_threshold:
            x += 2
        elif accel_vector.x > standing_threshold:
            x += 1
        elif accel_vector.x > -1 * standing_threshold:
            pass
        elif accel_vector.x > transition_threshold * -1:
            x -= 1
        else:
            x -= 2

        # mapping y component of acceleration vector to frame coordinates (vertical movement)
        if accel_vector.y > transition_threshold:
            y += 2
        elif accel_vector.y > standing_threshold:
            y += 1
        elif accel_vector.y > -1 * standing_threshold:
            pass
        elif accel_vector.y > transition_threshold * -1:
            y -= 1
        else:
            y -= 2

        return x, y

    def update(self, accel_vector, transition_threshold: float, standing_threshold: float):
        self.frame = self.frame_xy_from_accel_vect(accel_vector, transition_threshold, standing_threshold)
        pass

    def draw(self, screen: pygame.Surface, coords: tuple[float, float]):
        screen.blit(self.frames[self.frame[1]][self.frame[0]], coords)


class CyclicAnim:  # Animacje zapetlane - idle, plomenie, wydechy etc. moga miec po kilka wariantow np. zwykly wydech i boost
    def __init__(self, sprite_sheet_img, frame_counts, frame_time, width, height, scale):
        # sprite sheet parameters
        self.sprite_sheet = SpriteSheet(sprite_sheet_img)

        # sprite parameters
        self.sprite_width = width
        self.sprite_height = height
        self.sprite_scale = scale

        # animation parameters
        self.animation_list = []
        self.animation_steps = frame_counts  # list of frame counts for every animation in the sprite sheet
        self.action = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = frame_time
        self.frame = 0

        step_counter = 0
        for animation in self.animation_steps:
            temp_img_list = []
            for _ in range(animation):
                temp_img_list.append(
                    self.sprite_sheet.get_image(step_counter, self.sprite_width, self.sprite_height,
                                                self.sprite_scale))
                step_counter += 1
            self.animation_list.append(temp_img_list)

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = current_time
            if self.frame >= len(self.animation_list[self.action]):
                self.frame = 0

    def draw(self, screen: pygame.Surface, coords: tuple):
        screen.blit(self.animation_list[self.action][self.frame], coords)
