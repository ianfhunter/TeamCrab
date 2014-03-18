import pygame
import os
from pgu import gui
from time import sleep
from games import scenarios

this_dir = os.path.dirname(__file__)
root_dir = os.path.join(this_dir, '../..')

class Start_Screen:
    def __init__(self, game_config,screen):
        self.config = game_config
        self.selected_site = None
        self.screen = screen
        self.sel_val = scenarios.get_scenarios().itervalues().next()

        self.app = gui.App()
        self.app.connect(gui.QUIT, self.app.quit, None)
        self.contain = gui.Container(width=self.config["screenX"],
                                     height=self.config["screenY"])
        self.font = pygame.font.SysFont("Helvetica", 15)

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
        self.sel_val = scenarios.get_scenarios().get(selection.value)



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
#        choices = ["Eastern European Teams", "Asia-Based Development", "Worldwide Development"]
        choices =  scenarios.get_scenarios()


        bar_position = 160
        if self.contain.widgets == []:            

            #selection
            sel = gui.Select()
            for itr,label in enumerate(choices):
                sel.add(label,label)
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