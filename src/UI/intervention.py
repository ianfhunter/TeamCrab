import pygame
import random
import json
from pgu import gui
from time import sleep

class Intervention:
    def __init__(self, screen, config, project, site):
        self.config = config
        self.project = project
        self.screen = screen
        self.app = gui.App()
        self.app.connect(gui.QUIT, self.app.quit, None)
        self.contain = gui.Container(width=self.config["screenX"],
                                     height=self.config["screenY"])

        self.intervention_site = site
        self.intervention_type = None

        self.firstDraw = True
        self.firstOptions = True
        self.firstScroll = True

    def choose_intervention_site(self,site):
        '''
        @untestable - function manipulates user interface, makes no sense to test.
        '''
        self.intervention_site = site
        self.intervention_type = None
        self.firstScroll = True
        if self.contain.find("report_details"):
            self.contain.remove(self.contain.find("report_details"))

    def do_intervention(self,intervention_type):
        '''
        Sets the type of intervention in UI.

        @untestable - function manipulates user interface, makes no sense to test.
        '''
        self.intervention_type = intervention_type
        self.firstScroll = True
        if self.contain.find("report_details"):
            self.contain.remove(self.contain.find("report_details"))

    def refresh_screen(self):
        '''
        Refreshes the intervention interface screen.

        @untestable - Just draws UI elements onscreen, makes no sense to test.
        '''
        self.app.paint(self.screen)
        self.app.update(self.screen)

        pygame.display.update()

    def button_option(self,intervention_name,activity):
        button = gui.Button(intervention_name)
        button.connect(gui.CLICK, self.do_intervention,activity)
        return button


    def perform_intervention(self,intervention_activity):
        print intervention_activity

        project.add_intervention(self.intervention_site.name, "intervention_name")

        intervention_result = [] ## gui.Label

        return intervention_result

    def draw_intervention(self):
        '''
        Draws details of an intervention onscreen.

        @untestable - Just draws UI elements onscreen, makes no sense to test.
        '''
        pygame.draw.rect(self.screen, 0xFAFCA4,
                            (100,20,650,410))

        info_x = 150
        font = pygame.font.SysFont("Helvetica", 22)
        smallfont = pygame.font.SysFont("Helvetica", 18)

        label = smallfont.render( "Press Enter to close this window", 1, (0, 0, 0))
        self.screen.blit(label, (info_x, 400))

        if self.intervention_site:
            y_offset = 50
            font = pygame.font.SysFont("Helvetica", 24)
            bellerose_font = pygame.font.Font(self.config["bellerose_font"], 40)

            label = bellerose_font.render("Interventions - {}".format(self.intervention_site.name), 1, (0, 0, 0))

            y_offset += 10
            #Centering
            name_length = len("Interventions - {}".format(self.intervention_site.name))
            name_length = name_length*10

            self.screen.blit(label, (500 - name_length, y_offset - 60))

            font = pygame.font.SysFont("Helvetica", 16)

            for name, cost in [(i.name, i.get_cost()) for i in self.project.possible_interventions]:
                y_offset += 20
                if self.firstOptions:
                    button = self.button_option(name, name)
                    self.contain.add(button, info_x, y_offset)

                label = font.render("${}".format(cost), 1, (0, 0, 0))
                self.screen.blit(label, (info_x + 365 + 60, y_offset))

            if self.firstOptions:
                #make sure doesnt add next time
                self.firstOptions = False
                self.app.init(self.contain)

            hel_font = pygame.font.SysFont("Helvetica", 12)
            if self.intervention_type:
                intervention_result = []
                if self.firstScroll:
                    self.firstScroll = False
                    my_list = gui.List(width=560,height=80,name="report_details")
                    intervention_result.append(gui.Label("intervention Results:"))
                    for team in self.intervention_site.teams:
                        intervention_result.append(gui.Label("Team " + team.name))
                        intervention_result.extend( self.perform_intervention(self.intervention_type) )

                    for label in intervention_result:
                        label.set_font(hel_font)
                        my_list.add(label)

                    self.contain.add(my_list,info_x,y_offset+30)
                    self.app.init(self.contain)


    def draw(self):
        '''
        Draws UI for intervention interface.
        The parent draw function of the end game screen.

        @untestable - Just draws UI elements onscreen, makes no sense to test.
        '''
        self.draw_intervention()
        self.refresh_screen()
