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
        self.complete = False
        self.draw()
        while True:
            sleep(self.config["sleep_duration"])
            # Handle all events.
            for event in pygame.event.get():
                self.app.event(event)
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    os._exit(1)
            if self.complete:
                return
            else:
                self.draw()

    def refresh_screen(self):
        ''' Updates the screen - but only the updated portion of it so we save
        on refreshing the entire screen.
        '''
        pygame.display.flip()

    def update_scenario_choice(self,selection):
        ''' Callback for changing scenarios with PGU select element'''
        print selection.value

    def complete_setup(self):
        self.complete = True
        return

    def draw_choices(self):
        ''' Takes different scenarios and puts them in the selection gui element '''
        choices = ["Eastern European Teams", "Asia-Based Development", "Worldwide Development"]

        if self.contain.widgets == []:
            #selection
            sel = gui.Select()
            for itr,label in enumerate(choices):
                sel.add(label,str(itr))
            sel.connect(gui.CHANGE,self.update_scenario_choice ,sel)
            #button
            button = gui.Button("Submit")
            button.connect(gui.CLICK, self.complete_setup)

            self.contain.add(button, 500, 180)
            self.contain.add(sel, 200, 180)
            self.app.init(self.contain)


        font = pygame.font.SysFont("Veranda", 40)
        label = font.render("Scenario Choice", 1, (0, 0, 0))
        self.screen.blit(label, (300, 0))


        self.app.paint(self.screen)

        #select APP

    def draw(self):
        ''' Redraws all of the map screen. '''
        pygame.draw.rect(self.screen, self.config["background_colour"],
                         (0, 0, self.config["screenX"],self.config["screenY"]))
        self.draw_choices()
        self.refresh_screen()
