import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 50)
BLUE = (50, 50, 255)
GREY = (200, 200, 200)
LIGHTGREY = (100, 100, 100)
ORANGE = (200, 100, 50)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
TRANS = (1, 1, 1)

pygame.font.init()
sys_font = pygame.font.SysFont('lucidasanstypewriterfett', 12)

class Slider():
    def __init__(self, name, val,  mini, maxi,pos_x, pos_y):
        self.val = val  # start value
        self.mini = mini  # minimum at slider position left
        self.maxi = maxi  # maximum at slider position right
        self.xpos = pos_x  # x-location on screen
        self.ypos = pos_y
        self.surf = pygame.surface.Surface((100, 50))
        self.hit = False  # the hit attribute indicates slider movement due to mouse interaction

        self.txt_surf = sys_font.render(name, 1, BLACK)
        self.txt_rect = self.txt_surf.get_rect(center=(50, 15))

        # Static graphics - slider background #
        self.surf.fill((250, 250, 250))
        #pygame.draw.rect(self.surf, LIGHTGREY, [0, 0, 100, 50], 3)            #Border
        #pygame.draw.rect(self.surf, ORANGE, [10, 10, 80, 10], 0)        #Name
        pygame.draw.rect(self.surf, LIGHTGREY, [10, 30, 80, 3], 0)      #Slide

        self.surf.blit(self.txt_surf, self.txt_rect)  # this surface never changes

        # dynamic graphics - button surface #
        self.button_surf = pygame.surface.Surface((20, 20))
        self.button_surf.fill(TRANS)
        self.button_surf.set_colorkey(TRANS)
        pygame.draw.circle(self.button_surf, BLACK, (10, 8), 5, 0)
        pygame.draw.circle(self.button_surf, LIGHTGREY, (10, 8), 4, 0)

    def draw(self, window):
        """ Combination of static and dynamic graphics in a copy of
    the basic slide surface
    """
        # static
        surf = self.surf.copy()

        # dynamic
        pos_x = (10+int((self.val-self.mini)/(self.maxi-self.mini)*80), 33)
        self.button_rect = self.button_surf.get_rect(center=pos_x)
        surf.blit(self.button_surf, self.button_rect)
        self.button_rect.move_ip(self.xpos, self.ypos)  # move of button box to correct screen position

        # screen
        window.blit(surf, (self.xpos, self.ypos))

    def move(self):
        """
    The dynamic part; reacts to movement of the slider button.
    """
        self.val = (pygame.mouse.get_pos()[0] - self.xpos - 10) / 80 * (self.maxi - self.mini) + self.mini
        if self.val < self.mini:
            self.val = self.mini
        if self.val > self.maxi:
            self.val = self.maxi

