import pygame
import random
import json 
from pgu import gui
from time import sleep

class Inquiry:
    def __init__(self, screen, config, project):
        self.config = config
        self.project = project
        self.screen = screen
        self.app = gui.App()
        self.app.connect(gui.QUIT, self.app.quit, None)
        self.contain = gui.Container(width=self.config["screenX"],
                                     height=self.config["screenY"])
    
        self.inquiry_site = None
        self.inquiry_type = None

        self.firstDraw = True
        self.firstOptions = True
        self.firstScroll = True

    '''
    Changes active site when an site is chosen to be inquired.

    @untestable - function manipulates user interface, makes no sense to test.
    '''
    def choose_inquiry_site(self,site):
        self.inquiry_site = site
        self.inquiry_type = None
        self.firstScroll = True
        if self.contain.find("report_details"):
            self.contain.remove(self.contain.find("report_details"))

    '''
    Sets the type of inquiry in UI.

    @untestable - function manipulates user interface, makes no sense to test.
    '''
    def do_inquiry(self,inquiry_type):
        self.inquiry_type = inquiry_type
        self.firstScroll = True
        if self.contain.find("report_details"):
            self.contain.remove(self.contain.find("report_details"))

    '''
    Refreshes the inquiry interface screen.

    @untestable - Just draws UI elements onscreen, makes no sense to test.
    '''
    def refresh_screen(self):
        self.app.paint(self.screen)
        self.app.update(self.screen)

        pygame.display.flip()

    '''
    Draws details of an inquiry onscreen.

    @untestable - Just draws UI elements onscreen, makes no sense to test.
    '''
    def draw_inquiry(self):
        pygame.draw.rect(self.screen, 0xFAFCA4,
                            (100,20,650,410))
        pygame.draw.line(self.screen, 0x000000, (250,20), (250,430))

        start_x = 100
        start_y = 20

        if self.firstDraw:
            self.firstDraw = False
            my_list = gui.List(width=175, height=395)
            s = ""
            for itr,site in enumerate(self.project.locations):
                l = gui.Label(site.name)
                l.connect(gui.CLICK, self.choose_inquiry_site,site)
                my_list.add(l)            
                self.contain.add(l, start_x + 5, start_y + 20 +(20* (itr+1) ))
            self.app.init(self.contain)


        info_x = 250 + 5
        font = pygame.font.SysFont("Helvetica", 18)

        label = font.render( "Inquiries", 1, (0, 0, 0))
        self.screen.blit(label, (info_x + 150, 20))
        label = font.render( "Press Enter to close this window", 1, (0, 0, 0))
        self.screen.blit(label, (info_x, 400))

        if self.inquiry_site:
            y_offset = 50
            font = pygame.font.SysFont("Helvetica", 24)
            label = font.render(self.inquiry_site.name
                     , 1, (0, 0, 0))
            self.screen.blit(label, (info_x, y_offset))

            y_offset += 30
            if self.firstOptions:
                button = gui.Button('Send "are you on schedule?" email')
                button.connect(gui.CLICK, self.do_inquiry,"on_schedule")
                self.contain.add(button, info_x, y_offset)

            font = pygame.font.SysFont("Helvetica", 16)
            label = font.render("0 Working Days"
                    , 1, (0, 0, 0))
            self.screen.blit(label, (info_x + 365, y_offset))

            y_offset += 20
            if self.firstOptions:
                button = gui.Button('Send "please report status of modules" email')
                button.connect(gui.CLICK, self.do_inquiry,"status")
                self.contain.add(button, info_x, y_offset)

            label = font.render("0.1 Working Days"
                    , 1, (0, 0, 0))
            self.screen.blit(label, (info_x + 365, y_offset))

            y_offset += 20
            if self.firstOptions:
                button = gui.Button('Send "please list completed tasks" email')
                button.connect(gui.CLICK, self.do_inquiry,"list_c_tasks")
                self.contain.add(button, info_x, y_offset)

            label = font.render("0.5 Working Days"
                    , 1, (0, 0, 0))
            self.screen.blit(label, (info_x + 365, y_offset))

            y_offset += 20
            if self.firstOptions:
                button = gui.Button('Hold video conference')
                button.connect(gui.CLICK, self.do_inquiry,"video_conf")
                self.contain.add(button, info_x, y_offset)

            label = font.render("2 Working Days"
                    , 1, (0, 0, 0))
            self.screen.blit(label, (info_x + 365, y_offset))

            y_offset += 20
            if self.firstOptions:
                button = gui.Button('Make site visit')
                button.connect(gui.CLICK, self.do_inquiry,"visit")
                self.contain.add(button, info_x, y_offset)

            label = font.render("7 Working Days"
                    , 1, (0, 0, 0))
            self.screen.blit(label, (info_x + 365, y_offset))

            if self.firstOptions:
                #make sure doesnt add next time
                self.firstOptions = False
                self.app.init(self.contain)



            if self.inquiry_type:
                if self.firstScroll:
                    self.firstScroll = False

                    my_list = gui.List(width=480,height=160,name="report_details")

                    my_list.add(gui.Label("Inquiry Results:"))

                    for team in self.inquiry_site.teams:
                        my_list.add(gui.Label("Team " + team.name))

                        if self.inquiry_type == "on_schedule":
                            #if onschedule s = "", else "not "
                            if not team.module:
                                on_or_off = "We aren't working on anything at the moment" 
                            else:
                                if self.inquiry_site.culture[0] == 0:
                                    on_or_off = "Yes, We are on schedule."
                                else:
                                    if team.module.is_on_time:
                                        on_or_off = "Yes, We are on schedule."
                                    else:
                                        on_or_off = "No, We are not on schedule."

                            my_list.add(gui.Label(on_or_off))
                        if self.inquiry_type == "status":
                            if not team.module:
                                on_or_off = "We aren't working on anything at the moment" 
                            else:
                                if self.inquiry_site.culture[0] == 0:
                                    on_or_off = "We are on schedule."
                                else:
                                    if team.module.is_on_time:
                                        on_or_off = "We are on schedule."
                                    else:
                                        on_or_off = "We are delayed & experiencing " + str(len(team.module.problems_occured)) + " problems."

                            my_list.add(gui.Label(on_or_off))
                        if self.inquiry_type == "list_c_tasks":
                            my_list.add(gui.Label("Completed Tasks:"))
                            for module in team.completed_modules:                                
                                for task in module.completed_tasks:
                                    my_list.add(gui.Label(module.name + " - " + task.name))
                            if not team.module:
                                my_list.add(gui.Label("We are not working on a module at the moment."))
                            else:
                                if len(team.module.completed_tasks) == 0:
                                    my_list.add(gui.Label("We have not completed any tasks."))
                                else:
                                    for task in team.module.completed_tasks:
                                        my_list.add(gui.Label(task.name))

                        if self.inquiry_type == "video_conf":
                            my_list.add(gui.Label("Completed Tasks:"))
                            for module in team.completed_modules:                                
                                for task in module.completed_tasks:
                                    my_list.add(gui.Label(module.name + " - " + task.name))

                            if not team.module:
                                my_list.add(gui.Label("We are not working on a module at the moment."))
                            else:
                                if len(team.module.completed_tasks) == 0:
                                    my_list.add(gui.Label("We have not completed any tasks."))
                                else:
                                    for x in team.module.completed_tasks:
                                        my_list.add(gui.Label(x))

                            if self.inquiry_site.culture[0] == 0:
                                if randint(0,1) == 0:
                                    #continue to lie
                                    my_list.add(gui.Label("We are on schedule for the current task"))
                                else:
                                    if team.module.is_on_time:
                                        my_list.add(gui.Label("We are on schedule for the current task")) 
                                    else:
                                        my_list.add(gui.Label("We are delayed for the current task"))  

                        if self.inquiry_type == "visit":
                            my_list.add(gui.Label("Completed Tasks:"))
                            for module in team.completed_modules:                                
                                for task in module.completed_tasks:
                                    my_list.add(gui.Label(module.name + " - " + task.name))

                            if not team.module:
                                my_list.add(gui.Label("We are not working on a module at the moment."))
                            else:
                                if len(team.module.completed_tasks) == 0:
                                    my_list.add(gui.Label("We have not completed any tasks."))
                                else:
                                    for x in team.module.completed_tasks:
                                        my_list.add(gui.Label(x))

                                if team.module.is_on_time:
                                    my_list.add(gui.Label("On schedule for the current task")) 
                                else:
                                    my_list.add(gui.Label("delayed for the current task"))  

                    self.contain.add(my_list,info_x,y_offset+50)
                    self.app.init(self.contain)


    '''
    Draws UI for inquiry interface.

    @untestable - Just draws UI elements onscreen, makes no sense to test.
    '''
    def draw(self):
        ''' The parent draw function of the end game screen .'''
        self.draw_inquiry()
        self.refresh_screen()
