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

    def choose_inquiry_site(self,site):
        '''
        Changes active site when an site is chosen to be inquired.

        @untestable - function manipulates user interface, makes no sense to test.
        '''
        self.inquiry_site = site
        self.inquiry_type = None
        self.firstScroll = True
        if self.contain.find("report_details"):
            self.contain.remove(self.contain.find("report_details"))

    def do_inquiry(self,inquiry_type):
        '''
        Sets the type of inquiry in UI.

        @untestable - function manipulates user interface, makes no sense to test.
        '''
        self.inquiry_type = inquiry_type
        self.firstScroll = True
        if self.contain.find("report_details"):
            self.contain.remove(self.contain.find("report_details"))

    def refresh_screen(self):
        '''
        Refreshes the inquiry interface screen.

        @untestable - Just draws UI elements onscreen, makes no sense to test.
        '''
        self.app.paint(self.screen)
        self.app.update(self.screen)

        pygame.display.flip()

    def draw_inquiry(self):
        '''
        Draws details of an inquiry onscreen.

        @untestable - Just draws UI elements onscreen, makes no sense to test.
        '''
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

                        #Are you on Schedule?
                        if self.inquiry_type == "on_schedule":
                            if not team.module:
                                my_list.add(gui.Label("We aren't working on anything at the moment" ))
                            else:
                                if self.inquiry_site.culture[0] == 0:
                                    my_list.add(gui.Label("Yes, We are on schedule."))
                                else:
                                    if team.module.is_on_time:
                                        my_list.add(gui.Label("Yes, We are on schedule."))
                                    else:
                                        my_list.add(gui.Label("No, We are not on schedule."))

                        #What is your status?
                        if self.inquiry_type == "status":
                            if not team.module:
                                my_list.add(gui.Label("We aren't working on anything at the moment" ))
                            else:
                                team.module.actual_cost = team.module.actual_cost + 1
                                if self.inquiry_site.culture[0] == 0:
                                    my_list.add(gui.Label( "We are on schedule."))
                                else:
                                    if team.module.is_on_time:
                                        my_list.add(gui.Label("We are on schedule."))
                                    else:
                                        my_list.add(gui.Label("We are delayed & experiencing " + str(len(team.module.problems_occured)) + " problems." ))                                           

                                        #Problems
                                        my_list.add("Problems:")
                                        for prob in team.module.problems_occured:
                                            my_list.add(gui.Label(prob))

                        #List your completed tasks.
                        if self.inquiry_type == "list_c_tasks":
                            my_list.add(gui.Label("Completed Tasks:"))
                            for module in team.completed_modules:                                
                                for task in module.completed_tasks:
                                    my_list.add(gui.Label(module.name + " - " + task.name))
                            if not team.module:
                                my_list.add(gui.Label("We are not working on a module at the moment."))
                            else:
                                team.module.actual_cost = team.module.actual_cost + 4

                                if len(team.module.completed_tasks) == 0:
                                    my_list.add(gui.Label("We have not completed any tasks."))
                                else:
                                    for task in team.module.completed_tasks:
                                        my_list.add(gui.Label(task.name))


                        #Host Video Conference
                        if self.inquiry_type == "video_conf":
                            #Completed Tasks
                            my_list.add(gui.Label("Completed Tasks:"))
                            for module in team.completed_modules:                                
                                for task in module.completed_tasks:
                                    my_list.add(gui.Label(module.name + " - " + task.name))

                            if not team.module:
                                my_list.add(gui.Label("We are not working on a module at the moment."))
                            else:
                                team.module.actual_cost = team.module.actual_cost + 16
                                if len(team.module.completed_tasks) == 0:
                                    my_list.add(gui.Label("We have not completed any tasks."))

                            #Current Tasks
                            if self.inquiry_site.culture[0] == 0:
                                if random.randint(0,1) == 0:
                                    #50% chance of continuing to lie
                                    my_list.add(gui.Label("We are on schedule for the current task - " + team.module.name))
                                else:
                                    if team.module.is_on_time:
                                        my_list.add(gui.Label("We are on schedule for the current task - " + team.module.name)) 
                                    else:
                                        my_list.add(gui.Label("We are delayed & experiencing " + str(len(team.module.problems_occured)) + " problems." ))                                           
                                        #Problems
                                        my_list.add("Problems:")
                                        for prob in team.module.problems_occured:
                                            my_list.add(gui.Label(prob))

                            else:
                                #honest team
                                if team.module.is_on_time:
                                    my_list.add(gui.Label("We are on schedule for the current task - " + team.module.name)) 
                                else:
                                    my_list.add(gui.Label("We are delayed & experiencing " + str(len(team.module.problems_occured)) + " problems." ))                                           
                                    #Problems
                                    my_list.add("Problems:")
                                    for prob in team.module.problems_occured:
                                        my_list.add(gui.Label(prob))


                        if self.inquiry_type == "visit":
                            my_list.add(gui.Label("Completed Tasks:"))
                            for module in team.completed_modules:                                
                                for task in module.completed_tasks:
                                    my_list.add(gui.Label(module.name + " - " + task.name))

                            if not team.module:
                                my_list.add(gui.Label("We are not working on a module at the moment."))
                            else:
                                team.module.actual_cost = team.module.actual_cost + 56
                                if len(team.module.completed_tasks) == 0:
                                    my_list.add(gui.Label("We have not completed any tasks."))
                                else:
                                    for task in team.module.completed_tasks:
                                        my_list.add(gui.Label(task.name))

                                if team.module.is_on_time:
                                    my_list.add(gui.Label("On schedule for the current task - "  + team.module.name)) 
                                else:
                                    my_list.add(gui.Label("We are delayed & experiencing " + str(len(team.module.problems_occured)) + " problems." ))                                           
                                    #Problems
                                    my_list.add("Problems:")
                                    for prob in team.module.problems_occured:
                                        my_list.add(gui.Label(prob))

                    self.contain.add(my_list,info_x,y_offset+50)
                    self.app.init(self.contain)


    def draw(self):
        '''
        Draws UI for inquiry interface.
        The parent draw function of the end game screen.

        @untestable - Just draws UI elements onscreen, makes no sense to test.
        '''
        self.draw_inquiry()
        self.refresh_screen()
