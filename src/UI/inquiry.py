import pygame
import random
import json
from pgu import gui
from time import sleep

import ctypes

class Inquiry:
    ''' Class used for drawing the Inquiry UI.

    @untestable - Just draws UI elements onscreen, makes no sense to test.
    ''''
    def __init__(self, screen, config, project, site):
        self.config = config
        self.project = project
        self.screen = screen
        self.app = gui.App()
        self.app.connect(gui.QUIT, self.app.quit, None)
        self.contain = gui.Container(width=self.config["screenX"],
                                     height=self.config["screenY"])

        self.inquiry_site = site
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

        #Attempt at removing thread crashing issue
        # try:
        #     x11 = ctypes.cdll.LoadLibrary('libX11.so')
        #     x11.XInitThreads()
        #     print "XInitThreads"
        # except:
        #     pass
        pygame.display.update()

    def draw_inquiry(self):
        '''
        Draws details of an inquiry onscreen.

        @untestable - Just draws UI elements onscreen, makes no sense to test.
        '''
        pygame.draw.rect(self.screen, 0xFAFCA4,
                            (100,20,650,410))

        info_x = 150
        font = pygame.font.SysFont("Helvetica", 22)
        smallfont = pygame.font.SysFont("Helvetica", 18)

        label = smallfont.render( "Press Enter to close this window", 1, (0, 0, 0))
        self.screen.blit(label, (info_x, 400))

        if self.inquiry_site:
            y_offset = 50
            font = pygame.font.SysFont("Helvetica", 24)
            bellerose_font = pygame.font.Font(self.config["bellerose_font"], 40)

            label = bellerose_font.render("Inquiries - {}".format(self.inquiry_site.name)
                     , 1, (0, 0, 0))

            #Centering
            name_length = len("Inquiries - {}".format(self.inquiry_site.name))
            name_length = name_length*10
            self.screen.blit(label, (500 - name_length , y_offset - 50))

            y_offset += 30
            if self.firstOptions:
                button = gui.Button('Send "are you on schedule?" email')
                button.connect(gui.CLICK, self.do_inquiry,"on_schedule")
                self.contain.add(button, info_x, y_offset)

            font = pygame.font.SysFont("Helvetica", 16)
            label = font.render("0 Working Days"
                    , 1, (0, 0, 0))
            self.screen.blit(label, (info_x + 365 + 60, y_offset))

            y_offset += 20
            if self.firstOptions:
                button = gui.Button('Send "please report status of modules" email')
                button.connect(gui.CLICK, self.do_inquiry,"status")
                self.contain.add(button, info_x, y_offset)

            label = font.render("0.1 Working Days"
                    , 1, (0, 0, 0))
            self.screen.blit(label, (info_x + 365 + 60, y_offset))

            y_offset += 20
            if self.firstOptions:
                button = gui.Button('Send "please list completed tasks" email')
                button.connect(gui.CLICK, self.do_inquiry,"list_c_tasks")
                self.contain.add(button, info_x, y_offset)

            label = font.render("0.5 Working Days"
                    , 1, (0, 0, 0))
            self.screen.blit(label, (info_x + 365 + 60, y_offset))

            y_offset += 20
            if self.firstOptions:
                button = gui.Button('Hold video conference')
                button.connect(gui.CLICK, self.do_inquiry,"video_conf")
                self.contain.add(button, info_x, y_offset)

            label = font.render("2 Working Days"
                    , 1, (0, 0, 0))
            self.screen.blit(label, (info_x + 365 + 60, y_offset))

            y_offset += 20
            if self.firstOptions:
                button = gui.Button('Make site visit')
                button.connect(gui.CLICK, self.do_inquiry,"visit")
                self.contain.add(button, info_x, y_offset)

            label = font.render("7 Working Days"
                    , 1, (0, 0, 0))
            self.screen.blit(label, (info_x + 365 + 60, y_offset))

            if self.firstOptions:
                #make sure doesnt add next time
                self.firstOptions = False
                self.app.init(self.contain)


            hel_font = pygame.font.SysFont("Helvetica", 12)
            if self.inquiry_type:
                inquiry_result = []
                if self.firstScroll:
                    self.firstScroll = False
                    my_list = gui.List(width=560,height=200,name="report_details")
                    inquiry_result.append(gui.Label("Inquiry Results:"))
                    for team in self.inquiry_site.teams:
                        inquiry_result.append(gui.Label("Team " + team.name))

                        #Are you on Schedule?
                        if self.inquiry_type == "on_schedule":
                            if not team.module:
                                inquiry_result.append(gui.Label("We aren't working on anything at the moment" ))
                            else:
                                if self.inquiry_site.culture[0] == 0:
                                    inquiry_result.append(gui.Label("Yes, We are on schedule."))
                                else:
                                    if team.module.is_on_time:
                                        inquiry_result.append(gui.Label("Yes, We are on schedule."))
                                    else:
                                        inquiry_result.append(gui.Label("No, We are not on schedule."))


                        #What is your status?
                        if self.inquiry_type == "status":
                            if not team.module:
                                inquiry_result.append(gui.Label("We aren't working on anything at the moment" ))
                            else:
                                team.module.actual_cost = team.module.actual_cost + 1
                                if self.inquiry_site.culture[0] == 0:
                                    inquiry_result.append(gui.Label( "We are on schedule."))
                                else:
                                    if team.module.is_on_time:
                                        inquiry_result.append(gui.Label("We are on schedule."))
                                    else:
                                        inquiry_result.append(gui.Label("We are delayed & experiencing " + str(len(team.module.problems_occured)) + " problems." ))

                                        # #Problems
                                        # inquiry_result.append(gui.Label("Problems:"))
                                        # for prob in team.module.problems_occured:
                                        #     inquiry_result.append(gui.Label(prob))

                        #List your completed tasks.
                        if self.inquiry_type == "list_c_tasks":
                            inquiry_result.append(gui.Label("Completed Tasks:"))

                            #Completed Modules.
                            for module in team.completed_modules:
                                for task in module.completed_tasks:
                                    inquiry_result.append(gui.Label(module.name + " - " + task.name))

                            #Completed Tasks of the Current Module
                            if not team.module:
                                inquiry_result.append(gui.Label("We are not working on a module at the moment."))
                            else:
                                team.module.actual_cost = team.module.actual_cost + 4

                                if len(team.module.completed_tasks) == 0:
                                    inquiry_result.append(gui.Label("We have not completed any tasks."))
                                else:
                                    for task in team.module.completed_tasks:
                                        inquiry_result.append(gui.Label(team.module.name + " - " + task.name))


                        #Host Video Conference
                        if self.inquiry_type == "video_conf":
                            #Completed Modules
                            inquiry_result.append(gui.Label("Completed Tasks:"))
                            for module in team.completed_modules:
                                for task in module.completed_tasks:
                                    inquiry_result.append(gui.Label(module.name + " - " + task.name))

                            #Completed Tasks of the Current Module
                            if not team.module:
                                inquiry_result.append(gui.Label("We are not working on a module at the moment."))
                            else:
                                team.module.actual_cost = team.module.actual_cost + 16
                                if len(team.module.completed_tasks) == 0:
                                    inquiry_result.append(gui.Label("We have not completed any tasks."))
                                else:
                                    for task in team.module.completed_tasks:
                                        inquiry_result.append(gui.Label(team.module.name + " - " + task.name))


                                #Current Task & If we are on schedule for it.
                                #Dishonest Culture
                                if self.inquiry_site.culture[0] == 0:
                                    if random.randint(0,1) == 0:
                                        #50% chance of continuing to lie
                                        inquiry_result.append(gui.Label("We are on schedule for the current task: " + team.module.name + " - " + team.module.tasks[0].name))
                                    else:
                                        if team.module.is_on_time:
                                            inquiry_result.appendd(gui.Label("We are on schedule for the current task : " + team.module.name + " - " + team.module.tasks[0].name))
                                        else:
                                            inquiry_result.append(gui.Label("We are delayed for the current task: " + team.module.name + " - " + team.module.tasks[0].name +" & experiencing " + str(len(team.module.problems_occured)) + " problems." ))
                                            #Problems
                                            inquiry_result.append(gui.Label("Problems for module " + team.module.name + ":"))
                                            for prob in team.module.problems_occured:
                                                inquiry_result.append(gui.Label(prob))
                                #Honest Culture
                                else:
                                    if team.module.is_on_time:
                                        inquiry_result.append(gui.Label("We are on schedule for the current task: " + team.module.name + " - " + team.module.tasks[0].name))
                                    else:
                                        inquiry_result.append(gui.Label("We are delayed for the current task: " + team.module.name + " - " + team.module.tasks[0].name +" & experiencing " + str(len(team.module.problems_occured)) + " problems." ))
                                        #Problems
                                        inquiry_result.append(gui.Label("Problems for module " + team.module.name + ":"))
                                        for prob in team.module.problems_occured:
                                            inquiry_result.append(gui.Label(prob))


                        if self.inquiry_type == "visit":
                            inquiry_result.append(gui.Label("Completed Tasks:"))
                            for module in team.completed_modules:
                                for task in module.completed_tasks:
                                    inquiry_result.append(gui.Label(module.name + " - " + task.name))

                            if not team.module:
                                inquiry_result.append(gui.Label("We are not working on a module at the moment."))
                            else:
                                team.module.actual_cost = team.module.actual_cost + 56
                                if len(team.module.completed_tasks) == 0:
                                    inquiry_result.append(gui.Label("We have not completed any tasks."))
                                else:
                                    for task in team.module.completed_tasks:
                                        inquiry_result.append(gui.Label(team.module.name + " - " + task.name))

                                if team.module.is_on_time:
                                    inquiry_result.append(gui.Label("On schedule for the current task - "  + team.module.name))
                                else:
                                    inquiry_result.append(gui.Label("We are delayed & experiencing " + str(len(team.module.problems_occured)) + " problems." ))
                                    #Problems
                                    inquiry_result.append(gui.Label("Problems for module " + team.module.name + ":"))
                                    for prob in team.module.problems_occured:
                                        inquiry_result.append(gui.Label(prob))

                    for label in inquiry_result:
                        label.set_font(hel_font)
                        my_list.add(label)

                    self.contain.add(my_list,info_x,y_offset+30)
                    self.app.init(self.contain)


    def draw(self):
        '''
        Draws UI for inquiry interface.
        The parent draw function of the end game screen.

        @untestable - Just draws UI elements onscreen, makes no sense to test.
        '''
        self.draw_inquiry()
        self.refresh_screen()
#        sleep(self.config["ui_refresh_period_seconds"])
