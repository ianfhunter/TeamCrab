import pygame
import os
from pgu import gui
from time import sleep
import endgame,inquiry,intervention
from global_config import cultures

glob_game = None

this_dir = os.path.dirname(__file__)
root_dir = os.path.join(this_dir, '../..')


class Game:
    def __init__(self, project_data, game_config, screen, engine):
        glob_game = self
        self.project_data = project_data
        self.config = game_config
        self.firstDraw = True
        self.endscreen = None
        self.gameover = False

        self.inquiry = None         #inquiry object
        self.inquired = None        #boolean
        self.inquiry_site = None
        self.inquiry_type = None

        self.intervention = None         #inquiry object
        self.intervened = None        #boolean
        self.intervention_site = None
        self.intervention_type = None


        self.info_legend = False

        self.selected_site = self.project_data.home_site

        self.engine = engine

        self.buttonsNeedDrawing = True
        self.exitLegendNeedDrawing = True


        self.screen = screen
        self.app = gui.App()
        self.app.connect(gui.QUIT, self.app.quit, None)
        self.contain = gui.Container(width=self.config["screenX"],
                                     height=self.config["screenY"])
        self.font = pygame.font.SysFont("Helvetica", 15)

    def endgame(self, project):
        '''
        Draws endgame screen over game screen.
        Bring up the game over screen on the next draw.

        @untestable - just draws UI so not testable.
        '''
        self.gameover = True
        self.endscreen = endgame.EndGame(self.screen, self.config, project)

    def locationClick(self, site):
        '''
        Event handler for when user clicks a location

        @untestable - just draws UI so not testable.
        '''
        if not self.endscreen:
            print "Site Clicked!", site.coordinates
            self.selected_site = site
            self.draw_detailed_site_info(self.font)

    def info_legend_clicked(self):
        ''' Callback for when info legend is clicked.

        @untestable - just draws UI so not testable.
        '''
        self.info_legend = not self.info_legend

    def inquire(self):
        '''
        Draws inquiry interface screen.

        @untestable - just draws UI so not testable.
        '''
        #toggle window
        site = self.selected_site

        self.inquired = not self.inquired
        self.inquiry = inquiry.Inquiry(self.screen, self.config, self.project_data, site)
        self.engine.pause()

        while(self.inquired):

            self.inquiry.draw()
            sleep(self.config["ui_refresh_period_seconds"])
            # Handle all events.
            for event in pygame.event.get():

                # Tell PGU about all events.
                self.inquiry.app.event(event)
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    self.inquired = False
                    self.engine.resume() 
                    break
                # Handle quitting.
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    os._exit(1)


    def intervene(self):
        '''
        Draws intervention interface screen.

        @untestable - just draws UI so not testable.
        '''
        #toggle window
        site = self.selected_site

        self.intervened = not self.intervened
        self.intervention = intervention.Intervention(self.screen, self.config, self.project_data, site)
        self.engine.pause()

        while(self.intervened):

            self.intervention.draw()
            sleep(self.config["ui_refresh_period_seconds"])
            # Handle all events.
            for event in pygame.event.get():

                # Tell PGU about all events.
                self.intervention.app.event(event)
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    self.intervened = False
                    self.engine.resume() 
                    break
                # Handle quitting.
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    os._exit(1)


    def run(self):
        '''
        Handles all input events and goes to sleep.

        @untestable - just draws UI so not testable.
        '''
        self.draw()
        while True:
            sleep(self.config["ui_refresh_period_seconds"])

            if not self.inquired and not self.intervened:
                # Handle all events.
                for event in pygame.event.get():
                    # Tell PGU about all events.
                    if self.endscreen:
                        self.endscreen.app.event(event)
                    else:
                        self.app.event(event)
       
                    if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                        self.inquired = False
                        self.intervened = False
                        self.engine.resume() 
                    # Handle quitting.
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        os._exit(1)

    def update(self, project):
        """ Retrieves updated information from the backend and redraws the
        screen. 

        @untestable - just draws UI so not testable.
        """
        self.project_data = project
        if self.endscreen:
            self.endscreen.draw()  # Draw the endgame screen when pause pressed
        else:
            self.draw()


    def draw_info_button(self):
        '''
        Draws info button onscreen.

        @untestable - just draws UI so not testable.
        '''
        if self.info_legend:
            #show legend
            pygame.draw.rect(self.screen, 0xA0ECFF,
                            (670,10,170,110))    
            font = pygame.font.SysFont("Helvetica", 10)
            info_x = 680

            label = font.render("Green: Active & On Schedule", 1, (0, 0, 0))
            self.screen.blit(label, (info_x, 30))
            label = font.render("Yellow: Active & Delayed", 1, (0, 0, 0))
            self.screen.blit(label, (info_x, 50))
            label = font.render("Red: Stalled, Needs Intervention", 1, (0, 0, 0))
            self.screen.blit(label, (info_x, 70))
            label = font.render("Grey: Inactive / Concluded", 1, (0, 0, 0))
            self.screen.blit(label, (info_x, 90))

            #dont touch those style settings. very, very hax
            if self.buttonsNeedDrawing:

                button = gui.Button("",width=14,height=28)
                button.connect(gui.CLICK, self.info_legend_clicked)
                button.style.background = \
                    pygame.image.load(self.config["cancel_icon_path"])

                self.contain.add(button, 820, 0)
                self.app.init(self.contain)
                self.app.paint(self.screen)
            self.exitLegendNeedDrawing = True
        else:
            #show question mark icon
            #dont touch those style settings. very, very hax
            if self.exitLegendNeedDrawing:
                self.exitLegendNeedDrawing = False
                button = gui.Button("",width=14,height=28)
                button.connect(gui.CLICK, self.info_legend_clicked)
                button.style.background = \
                    pygame.image.load(self.config["question_icon_path"])

                self.contain.add(button, 810, 10)
                self.app.init(self.contain)
                self.app.paint(self.screen)
        

    def draw_world_map(self):
        '''
        Draws world map onscreen.

        @untestable - just draws UI so not testable.
        '''
        worldMap = pygame.image.load(self.config["map_path"])
        self.screen.blit(worldMap, (0, 0))

    def draw_bottom_bar(self, font):
        '''Draws bottom bar, taking screen geometry from global config file.
        Draws statistics about progress, balance, etc on the bottom bar.

        @untestable - just draws UI so not testable.
        '''
        # TODO: Info to be retrieved from backend, currently dummy data.
        bar_height = self.config["bottom_bar_height"]
        x = self.config["screenX"]
        y = self.config["screenY"]

        # Draw empty bottom bar.
        pygame.draw.rect(self.screen, self.config["bar_colour"],
                         (0, y - bar_height, 850, bar_height))

        # Overlay balance & statistics on bottom bar.
        label_pos = y - bar_height
        if self.project_data.cash >= 0:
            label = font.render("$"+str(self.project_data.cash), 1, (14, 106, 0))
        else:
            label = font.render("-$"+str(self.project_data.cash*-1), 1, (255, 0, 0))
        self.screen.blit(label, (10, label_pos))
        cur_time =self.project_data.current_time
        label = font.render(cur_time.strftime("%a %d %B %Y - %H:00 GMT") , 1, (0, 0, 0))
        self.screen.blit(label, (100, label_pos))
        label = font.render("Nominal Finish Time: " + str(self.project_data.delivery_date.strftime("%d %B %Y - %H:00 GMT")),
                             1, (38, 0, 255))
        self.screen.blit(label, (350, label_pos))

    def draw_sites(self):
        '''
        Draws circles indications site locations onscreen.

        @untestable - just draws UI so not testable.
        '''

        for index, site in enumerate(self.project_data.locations):

            if self.buttonsNeedDrawing:
                button = gui.Button(" ",name=site.name)
            else:
                button = self.contain.find(site.name)
            # Note: Styling buttons via images requires that a _surface_
            # be passed in.
            button.style.background = pygame.image.load(
                self.config["green_button_path"])


            inactive = True
            failing = False
            for team in site.teams:
                 
             #Changed as modules now assigned to teams rather then tasks and modules do not have dependancies at this time.
             #if a module is running, it is not stalled waiting on dependencies or waiting on another.
             #print team.modules[0] ,":",team.module            
                if team.module:
                    inactive = False

                if not failing:
                    if team.module:
                        # If the culture is dishonest then always show as green
                        if cultures[site.culture][0]:
                            # Locations with issues causing a time delay
                            if not team.module.is_on_time:
                                button.style.background = pygame.image.load(
                                    self.config["yellow_button_path"])
                            # Location that needs an intervention before it can
                            # progress any further
                            if team.module.stalled:
                                button.style.background = \
                                    pygame.image.load(self.config["red_button_path"])
                                failing = True

            #lowest priority display.
            if inactive:
                button.style.background = \
                    pygame.image.load(self.config["grey_button_path"])

            if self.buttonsNeedDrawing:
                button.connect(gui.CLICK, self.locationClick, site)
                self.contain.add(button, site.coordinates[0], site.coordinates[1])    
                self.app.init(self.contain)

    def draw_detailed_site_info(self, font):
        ''' Draws detailed info about the currently selected site.

        @untestable - just draws UI so not testable.
        '''
        y = 310

        # Draw plain background.
        pygame.draw.rect(self.screen, self.config["background_colour"],
                         (0, 280, 200, 180))

        if self.selected_site is None:
            label = font.render("No site selected", 1, (0, 0, 0))
            self.screen.blit(label, (40, y))
        else:
    
            site = self.selected_site

            label_y = y # 5
            y_inc = 30

            workerIcon = pygame.image.load(self.config["location_icon_path"])
            self.screen.blit(workerIcon, (1, label_y))
            label = font.render(site.name, 1, (0, 0, 0))
            self.screen.blit(label, (40, label_y))

            label_y += y_inc

            # Draw icons and accompanying text.
            workerIcon = pygame.image.load(self.config["man_icon_path"])
            self.screen.blit(workerIcon, (1, label_y))
            label = font.render(str(len(self.selected_site.teams)) +
                                " Team(s)", 1, (0, 0, 0))
            self.screen.blit(label, (40, label_y))

            label_y += y_inc

            peepIcon = pygame.image.load(self.config["peep_icon_path"])
            self.screen.blit(peepIcon, (1, label_y))
            population = 0
            for team in self.selected_site.teams:
                population += team.size
            label = font.render(str(population) + "  People ", 1,
                                (0, 0, 0))
            self.screen.blit(label, (40, label_y))

            label_y += y_inc

            clockIcon = pygame.image.load(self.config["clock_icon_path"])
            self.screen.blit(clockIcon, (1, label_y))
            progress = int(site.total_module_progress())
            label = font.render(str(progress) + "h Effort Expended", 1, (0, 0, 0))
            self.screen.blit(label, (40, label_y))

            label_y += y_inc

            #TODO: Potentially change this if multiple modules at one site.
            targetIcon = pygame.image.load(self.config["target_icon_path"])
            self.screen.blit(targetIcon, (1, label_y))
            num_on_time = site.num_modules_on_schedule()
            num_modules = site.num_modules()
            if num_modules - num_on_time == 0:
                status = "On Schedule"
            elif not cultures[site.culture][0]:
                status = "On Schedule" # Dishonest cultures always say they are on time
            else:
                status = "Delayed"
            label = font.render(status, 1, (0, 0, 0))
            self.screen.blit(label, (40, label_y))

    def draw_inquiry_button(self):
        ''' Draws the "menu" pause button over the bottom bar.

        @untestable - just draws UI so not testable.
        '''
        if self.buttonsNeedDrawing:
            # TODO: Real implementation for button action, currently dummy action.
            button = gui.Button("Inquire!",width=75)
            button.connect(gui.CLICK, self.inquire)

            self.contain.add(button, 4, self.config["menuY"] - 178)
            self.app.init(self.contain)

    def draw_intervention_button(self):
        ''' Draws the "menu" pause button over the bottom bar.

        @untestable - just draws UI so not testable.
        '''
        if self.buttonsNeedDrawing:
            # TODO: Real implementation for button action, currently dummy action.
            button = gui.Button("Intervene!")
            button.connect(gui.CLICK, self.intervene)

            self.contain.add(button, 102, self.config["menuY"] - 178)
            self.app.init(self.contain)


    def refresh_screen(self):
        ''' Updates the screen - but only the updated portion of it so we save
        on refreshing the entire screen.

        @untestable - just draws UI so not testable.
        '''
        #This is getting complicated and we dont really need it as it 
        self.app.paint(self.screen)

        if self.inquired or self.intervened:
            pygame.display.update((0, 280, 200, 180))
        else:
            pygame.display.flip()

    def draw(self):
        '''
        Redraws all of map screen.

        @untestable - just draws UI so not testable.
        '''
        font = pygame.font.SysFont("Helvetica", 15)

        ''' empty widget container - fix to memory leak
        (I tried to update the objects rather than recreating them, but it
        seems like we'd have trouble maintaining it) '''
        #self.contain.widgets = []

        self.draw_world_map()
        self.draw_bottom_bar(self.font)
        self.draw_sites()
        self.draw_detailed_site_info(self.font)
        self.draw_inquiry_button()
        self.draw_intervention_button()
        self.draw_info_button()
        self.refresh_screen()
        self.buttonsNeedDrawing = False
