import pygame
import os
import json
from pgu import gui
from time import sleep

from engine.Project import Project
from engine.Location import Location
from engine.Module import Module
from engine.Team import Team
from engine.RevenueTier import LowRevenueTier, MediumRevenueTier, HighRevenueTier


this_dir = os.path.dirname(__file__)
root_dir = os.path.join(this_dir, '../..')
games_dir = os.path.join(root_dir, 'games/')
class Start_Screen:
    def __init__(self, game_config,screen):
        self.config = game_config
        self.selected_site = None
        self.screen = screen

        # Get all the scenario json files from the games dir
        scenario_files = [ f for f in os.listdir(games_dir) if os.path.isfile(os.path.join(games_dir, f)) ] # get all files in the games dir
        # This is a dict of scenario names to their filenames
        self.scenarios = dict()
        for scenario in scenario_files:
            scenario_data = json.load(open(os.path.join(games_dir, scenario)))
            self.scenarios[scenario_data['Name']] = scenario
        self.sel_val = self.load_scenario(self.scenarios.itervalues().next())
        self.sel_val.value = "wow"

        self.app = gui.App()
        self.app.connect(gui.QUIT, self.app.quit, None)
        self.contain = gui.Container(width=self.config["screenX"],
                                     height=self.config["screenY"])
        self.font = pygame.font.SysFont("Helvetica", 15)

    def load_scenario(self, scenario):
        project_data = json.load(open(os.path.join(games_dir, scenario)))

        # Get the revenue tier for the project. Assumed to be low if not specified or incorrectly specified
        if project_data['Revenue Tier'] == 'High':
            revenue_tier = HighRevenueTier()
        elif project_data['Revenue Tier'] == 'Medium':
            revenue_tier = MediumRevenueTier()
        else:
            revenue_tier = LowRevenueTier()

        # Initialise the project
        project = Project(project_data['Name'], 'Agile', project_data['Budget'], revenue_tier)

        # Initialise each of the locations
        for location_data in project_data['Locations']:
            new_location = Location(location_data['Name'], location_data['Culture'], location_data['Capacity'])
            project.locations.append(new_location)

        # Initialise each of the teams and add them to the specified locations
        for team_data in project_data['Teams']:
            new_team = Team(team_data['Name'], team_data['Size'])
            location = [location for location in project.locations if location.name == team_data['Location']]
            if location:
                location[0].add_team(new_team)
            else:
                print 'Unknown location', team_data['Location'], 'specified in team', team_data['Name']
                raise Exception('Unknown location exception')

        # Initialise each of the modules and add them to specified teams and to the project
        for module_data in project_data['Modules']:
            new_module = Module(module_data['Name'], module_data['Cost'])
            project.modules.append(new_module)
            for location in project.locations:
                team = [team for team in location.teams if team.name == module_data['Assigned Team']]
                if team:
                    team[0].modules.append(new_module)
                    break

        # Set the home site, this is set to the first location specified if no home site is selected
        location = location = [location for location in project.locations if location.name == project_data['Home location']]
        if location:
            project.home_site = location[0]
        else:
            project.home_site = project.locations[0]

        return project

    def run(self):
        '''Handles all input events and goes to sleep.
        @untestable
        '''
        self.complete = False
        self.draw()
        while True:
            sleep(self.config["ui_refresh_period_seconds"])
            # Handle all events.
            for event in pygame.event.get():
                self.app.event(event)
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    os._exit(1)
            if self.complete:
                return self.sel_val
            else:
                self.draw()

    def refresh_screen(self):
        ''' Updates the screen - but only the updated portion of it so we save
        on refreshing the entire screen.

        @untestable - UI redrawing code.
        '''
        pygame.display.flip()

    def update_scenario_choice(self,selection):
        ''' Callback for changing scenarios with PGU select element
        @untestable - UI redrawing code.
        '''
        self.sel_val = self.load_scenario(self.scenarios[selection.value.value])



    '''
    Displays info about the selected scenario so users can make more informed choices
    This is UI code and untestable

    @untestable
    '''
    def show_scenario(self):
        ''' Callback for changing scenarios with PGU select element'''
        if self.contain.find("scenario_details"):
            self.contain.remove(self.contain.find("scenario_details"))


        my_list = gui.List(width=700,height=275,name="scenario_details")
        my_list.add(gui.Label("Scenario Details:"))

        my_list.add(gui.Label("Expected Revenue - $" + str(self.sel_val.expected_revenue())))

        for location in self.sel_val.locations:
            my_list.add(gui.Label("    " +location.name + ":"))
            for itr,team in enumerate(location.teams):
                my_list.add(gui.Label("        Team "+ str(itr+1) +"("+str(team.size)+" Persons)" + ":"))
                for module in team.modules:
                    my_list.add(gui.Label("            Module - "+ module.name + " [" + str(module.expected_cost) + " Expected Cost (Person Hours)]"))




        self.contain.add(my_list,70,190)
        self.app.init(self.contain)



    '''
    Flags that the start screen setup is completed.
    Simple attribute setter so not tested.

    '''
    def complete_setup(self):
        self.complete = True
        return

    '''
    Draws the possible scenarios onscreen in a selection box.

    This is UI code and untestable.
    @untestable
    '''
    def draw_choices(self):
        ''' Takes different scenarios and puts them in the selection gui element '''
        bar_position = 160
        if self.contain.widgets == []:

            #selection
            sel = gui.Select()
            sel.value = self.scenarios.iteritems().next()[0]
            for label,filename in self.scenarios.iteritems():
                sel.add(str(label), str(label))
            sel.connect(gui.CHANGE,self.update_scenario_choice ,sel)
            self.contain.add(sel, 205, bar_position )

            #button
            button = gui.Button("Details")
            button.connect(gui.CLICK, self.show_scenario)
            self.contain.add(button, 605, bar_position )


            button = gui.Button("Submit")
            button.connect(gui.CLICK, self.complete_setup)
            self.contain.add(button, 685, bar_position )

            #scrolls
            self.app.init(self.contain)


        self.screen.blit(pygame.image.load(self.config["start_background_path"]),(0,0))
        self.screen.blit(pygame.image.load(self.config["logo_path"]),(380,0))


        font = pygame.font.Font(self.config["bellerose_font"], 40)
        label = font.render("Software Engineering Simulator", 1, (0, 0, 0))
        self.screen.blit(label, (200, bar_position -80))

        font = pygame.font.Font(self.config["bellerose_font"], 28)
        label = font.render("Scenarios:", 1, (0, 0, 0))
        self.screen.blit(label, (85, bar_position -25))


        self.app.paint(self.screen)

        #select APP

    '''
    Draws the start screen onscreen.

    This is UI code and untestable.
    '''
    def draw(self):
        ''' Redraws all of the map screen. '''
        pygame.draw.rect(self.screen, self.config["background_colour"],
                         (0, 0, self.config["screenX"],self.config["screenY"]))
        self.draw_choices()
        self.refresh_screen()
