# Taken from http://inventwithpython.com/

import pygame, sys
from pygame.locals import *
from global_config import config as gc

def zero_velocity_test():
    # set up pygame
    pygame.init()

    # set up the window
    windowSurface = pygame.display.set_mode((gc["screenX"], gc["screenY"]), 0, 32)
    pygame.display.set_caption('Crab SWENG Simulator')  #Title of screen

    # set up the colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # set up fonts
    titleFont = pygame.font.SysFont(None, 48)

    # draw the white background onto the surface
    windowSurface.fill(WHITE)

    text = titleFont.render("Config values:", True, BLACK)
    windowSurface.blit(text, (20, 20))

    pygame.display.update()
    bodyFont = pygame.font.SysFont(None, 24)
    y = 70

    for (key, val) in gc.items():
        # set up the text
        text = bodyFont.render(key + " : " + str(val), True, BLACK)

        # draw the text onto the surface
        windowSurface.blit(text, (40, y))
        y += 30

    # draw the window onto the screen
    pygame.display.update()

    # run the game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
