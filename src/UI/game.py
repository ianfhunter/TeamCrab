import pygame, os
from pgu import gui
from time import sleep
import endgame

glob_game = None

this_dir = os.path.dirname(__file__)
root_dir = os.path.join(this_dir, '../..')


class Game:
    def __init__(self, project_data, game_config):
        glob_game = self
        self.project_data = project_data
        self.config = game_config
        self.firstDraw = True
        self.endscreen = None

        self.selected_site = None

        # Screen setup.
        # TODO: This should be passed in the constructor rather than
        # being created in here.
        self.screen = pygame.display.set_mode((self.config["screenX"],
            self.config["screenY"]))
        self.app = gui.App()
        self.app.connect(gui.QUIT,self.app.quit,None)
        self.contain = gui.Container(width = self.config["screenX"],
            height = self.config["screenY"])

    def locationClick(self):
        if(not self.endscreen):
            print("Site Clicked!")
            self.selected_site = self.project_data.locations[0]


    def pauseClick(self):
        ''' Menu button to bring up new dialog, changes variables for next update().'''

        print("Pause Clicked!")
        if not self.endscreen:
            self.endscreen = endgame.EndGame(self.screen,self.config)
        else:
            self.endscreen = None
            self.firstDraw = True #redraw main screen fully once we exit.

    
    def run(self):
        ''' Handles all input events and goes to sleep.'''
        self.draw()
        while True:
            sleep(self.config["sleep_duration"])
            # Handle all events.
            for event in pygame.event.get():
                # Tell PGU about all events.
                self.app.event(event)
                # Handle quitting.
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    os._exit(1)

    def update(self,project):
        """ Retrieves updated information from the backend and redraws the screen. """
        self.project_data = project
        if self.endscreen:
            self.endscreen.draw()        #draw the endgame screen when pause pressed
        else:
            self.draw()

    def draw_world_map(self):
        """ Draws the world map onscreen."""
        worldMap = pygame.image.load(self.config["map_path"])
        self.screen.blit(worldMap, (0, 0))

    def draw_bottom_bar(self, font):
        """Draws bottom bar, taking screen geometry from global config file.
        Draws statistics about progress, balance, etc on the bottom bar.
        """
        # TODO: Info to be retrieved from backend, currently dummy data.
        bar_height = self.config["bottom_bar_height"]
        x = self.config["screenX"]
        y = self.config["screenY"]

        # Draw empty bottom bar.
        pygame.draw.rect(self.screen, self.config["bar_colour"],
                (0, y - bar_height, 850, bar_height))

        # Overlay balance & statistics on bottom bar.
        label_pos = y - bar_height
        label = font.render("-$500", 1, (255, 0, 0))
        self.screen.blit(label, (20, label_pos))
        label = font.render("Jul 21st 14:00 GMT", 1, (0, 0, 0))
        self.screen.blit(label, (200, label_pos))
        label = font.render("10 Items Needing Review", 1, (238, 255, 53))
        self.screen.blit(label, (400, label_pos))


    def draw_sites(self):
        ''' Draws dots showing sites around the world map.
        '''        # TODO: Info to be retrieved from backend, currently dummy data.
        for x in self.project_data.locations:
            button = gui.Button(" ")
            #Note: Styling buttons via images requires that a _surface_ be passed in. 
            button.style.background = pygame.image.load(self.config["green_button_path"])

            failing = False
            for t in x.teams:
                if not failing:
                    #locations with issues causing a time delay
                    if t.task.progress < t.task.expected_progress:
                        button.style.background = pygame.image.load(self.config["yellow_button_path"])
                    #location that needs an intervention before it can progress any further
                    if t.task.stalled:
                        button.style.background = pygame.image.load(self.config["red_button_path"])
                        failing = True

            button.connect(gui.CLICK, self.locationClick)
            self.contain.add(button, x.coordinates[0], x.coordinates[1])
            self.app.init(self.contain)
            self.app.paint(self.screen)

    def draw_detailed_site_info(self, font):
        ''' Draws detailed info about the currently selected site.
        '''        # TODO: Info to b retrieved from backend, currently dummy data.

        y = 320

        # Draw plain background.
        pygame.draw.rect(self.screen, self.config["background_colour"],(0, y, 200, 140))

        if self.selected_site is not None:

            # Draw icons and accompanying text.
            workerIcon = pygame.image.load(self.config["man_icon_path"])
            self.screen.blit(workerIcon, (1, 325))
            label = font.render(str(len(self.selected_site.teams)) + " Team(s)", 1, (0, 0, 0))
            self.screen.blit(label, (40, y + 15))

            cogIcon = pygame.image.load(self.config["cog_icon_path"])
            self.screen.blit(cogIcon, (1, 360))
            label = font.render("75% Efficiency", 1, (0, 0, 0))
            self.screen.blit(label, (40, y + 50))

            clockIcon = pygame.image.load(self.config["clock_icon_path"])
            self.screen.blit(clockIcon, (1, 395))
            label = font.render(str(int(self.project_data.locations[0].teams[0].task.progress)) +" Hours", 1, (0, 0, 0))
            self.screen.blit(label, (40, y + 85))

            targetIcon = pygame.image.load(self.config["target_icon_path"])
            self.screen.blit(targetIcon, (1, 430))
            label = font.render("On Schedule", 1, (0,0,0))
            self.screen.blit(label, (40, y + 115))

    
    def draw_pause_button(self):
        ''' Draws the "menu" pause button over the bottom bar.
        '''
        # TODO: Real implementation for button action, currently dummy action.
        button = gui.Button("Menu")
        button.connect(gui.CLICK, self.pauseClick)

        self.contain.add(button, self.config["menuX"], self.config["menuY"])
        self.app.init(self.contain)
        self.app.paint(self.screen)

    
    def refresh_screen(self):
        ''' Updates the screen - but only the updated portion of it so we save on
        refreshing the entire screen.
        '''
        if self.firstDraw:
            pygame.display.flip()
            self.firstDraw = False
        else:
            pygame.display.update((0, 460, 850, 20))    #bottom bar
            pygame.display.update((0, 320, 200, 140))    #grey box


            for x in self.project_data.locations:
                pygame.display.update((x.coordinates[0] -5, x.coordinates[1]-5, x.coordinates[0]+5, x.coordinates[1]+5))

            

    def draw(self):
        ''' Redraws all of the map screen.    '''
        font = pygame.font.SysFont("Helvetica", 15)
        self.draw_world_map()
        self.draw_bottom_bar(font)
        self.draw_sites()
        self.draw_detailed_site_info(font)
        self.draw_pause_button()
        self.refresh_screen()
