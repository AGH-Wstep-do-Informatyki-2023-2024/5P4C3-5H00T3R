Hell = ValueError

class RGB:
    def __init__(self):
        orange = self.hex_color_to_tuple("#ffa000")
        pass    
    BLACK = (0,0,0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)

    def hex_color_to_tuple(self,erm : str):
        if(erm[0]=='#'):
            if(len(erm) == 7):
                return (hex(erm[1]+erm[2]), hex(erm[3]+erm[4]), hex(erm[5] + erm[6]))
        else:
            raise Hell("pass #xxyyzz or #xxyyzzaa(not implemented >_<) here")




