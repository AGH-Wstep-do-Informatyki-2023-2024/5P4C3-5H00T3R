from enum import Enum

Hell = ValueError


def hex_color_to_tuple(erm: str):
    if erm[0] == '#':
        if len(erm) == 7:
            return int(erm[1]) * 16 + int(erm[2]), int(erm[3]) * 16 + int(erm[4]), int(erm[5]) * 16 + int(erm[6])
    else:
        raise Hell("pass #xxyyzz or #xxyyzzaa(not implemented >_<) here")


class RGB(Enum):
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)
    ORANGE = hex_color_to_tuple("#ffa000")
    KEY = hex_color_to_tuple("#00b140")
