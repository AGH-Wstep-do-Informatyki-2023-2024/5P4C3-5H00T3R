import pygame


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


class GridSheetAnim:  # Animacje na bazie wektora przyspieszenia
    def __init__(self, sprite_sheet_img: pygame.image, sheet_frames_h: int, sheet_frames_v: int, sprite_width: int,
                 sprite_height: int, scale: int):

        """

        :param sprite_sheet_img: pygame.image representinhg spritesheet to be animated
        :param sheet_frames_h: number of frames that will make up an animation grid row
        :param sheet_frames_v: number of rows in the animation grid
        :param sprite_width: sprite image width (px)
        :param sprite_height: sprite image height (px)
        :param scale: scale for displaying sprite on screen
        """

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
    def __init__(self, sprite_sheet_img: pygame.image, frame_counts: list[int], frame_time: int, width: int,
                 height: int, scale: int):

        """

        :param sprite_sheet_img: pygame.image object storing spritesheet
        :param frame_counts: list of frame counts for every animation in the sprite sheet, in order
        :param frame_time: time between frame swaps
        :param width: sprite frame width (px)
        :param height: sprite frame height (px)
        :param scale: scale for displaying sprite on screen
        """
        # sprite sheet parameters
        self.sprite_sheet = SpriteSheet(sprite_sheet_img)

        # sprite parameters
        self.sprite_width = width
        self.sprite_height = height
        self.sprite_scale = scale

        # animation parameters
        self.animation_list = []
        self.animation_steps = frame_counts
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


class ScrollingAnim:  # Scrollowanie obrazka w pętli
    def __init__(self, img_path: str, screen_size_v: int, frames_per_pixel_scroll: int):
        self.image = pygame.image.load(img_path)
        self.frame = pygame.Surface(self.image.get_size()).convert_alpha()
        self.frame.fill((0, 0, 0, 0))  # make surface transparent, otherwise base surface is (0, 0, 0, 1)
        self.scroll = 0
        self.scroll_max = screen_size_v  # self.image.get_height()
        self.fpp = frames_per_pixel_scroll
        pass

    def update(self):
        self.frame.fill((0, 0, 0, 0))
        self.frame.blit(self.image, (0, self.scroll))
        self.frame.blit(self.image, (0, self.scroll - self.scroll_max - 1))
        self.scroll = (self.scroll + (1 / self.fpp)) % self.scroll_max
        pass

    def draw(self, screen: pygame.Surface, coords: tuple):
        screen.blit(self.frame, coords)
        pass


class BgAnim:
    def __init__(self, screen_height: int, top_path: str, mid_path: str, bot_path: str, top_fpp: int, mid_fpp: int,
                 bot_fpp: int):
        """

        :param screen_height: used to initialize background layers
        :param top_path:
        :param mid_path:
        :param bot_path:
        :param top_fpp: Frames needed to scroll top layer by 1 pixel
        :param mid_fpp:
        :param bot_fpp:
        """
        self.top = ScrollingAnim(top_path, screen_height, top_fpp)
        self.mid = ScrollingAnim(mid_path, screen_height, mid_fpp)
        self.bot = ScrollingAnim(bot_path, screen_height, bot_fpp)
        pass

    def update(self):
        self.top.update()
        self.mid.update()
        self.bot.update()
        pass

    def draw(self, screen: pygame.Surface):
        self.bot.draw(screen, (0, 0))
        self.mid.draw(screen, (0, 0))
        self.top.draw(screen, (0, 0))
        pass
