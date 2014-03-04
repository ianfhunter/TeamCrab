import pygame
import os
from pgu import gui
from time import sleep

this_dir = os.path.dirname(__file__)
root_dir = os.path.join(this_dir, '../..')

class Start_Screen:
    def __init__(self, game_config,screen):
        self.config = game_config
        self.selected_site = None
        self.screen = screen

        #
        self.app = gui.App()
        self.app.connect(gui.QUIT, self.app.quit, None)
        self.contain = gui.Container(width=self.config["screenX"],
                                     height=self.config["screenY"])
        self.font = pygame.font.SysFont("Helvetica", 15)

    def run(self):
        ''' Handles all input events and goes to sleep.'''
        self.draw()
        while True:
            sleep(self.config["sleep_duration"])
            # Handle all events.
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    return

    def refresh_screen(self):
        ''' Updates the screen - but only the updated portion of it so we save
        on refreshing the entire screen.
        '''
        pygame.display.flip()
        self.firstDraw = False

    def draw(self):
        ''' Redraws all of the map screen. '''
        pygame.draw.rect(self.screen, self.config["background_colour"],
                         (0, 285, 200, 175))
        self.refresh_screen()
