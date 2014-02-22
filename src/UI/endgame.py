import pygame
import csv
from pgu import gui
from time import sleep

class EndGame:
    def __init__(self, screen, config, project):
        self.config = config
        self.project = project
        self.screen = screen
        self.app = gui.App()
        self.app.connect(gui.QUIT, self.app.quit, None)
        self.contain = gui.Container(width=400,
                                     height=400)
        self.hasList = False

    def generate_report(self):
        ''' Generate table with information about the end of the game '''
        report = list()
        report.append(['Team', 'Module', 'Task', 'Estimated Time', 'Actual Time'])
        for location in self.project.locations:
            for team in location.teams:
                for task in team.completed_tasks:
                    estimated_hours = task.cost / team.size
                    report.append([team.name, task.module.name, task.name, estimated_hours, task.hours_taken])
        return report

    def total_person_hours(self):
        total_estimated = 0
        total_actual = 0
        for location in self.project.locations:
            for team in location.teams:
                for task in team.completed_tasks:
                    estimated_hours = task.cost / team.size
                    total_estimated += estimated_hours    
                    total_actual += task.hours_taken
        return (total_estimated, total_actual)

    def refresh_screen(self):
        pygame.display.flip()

    def write_endgame_csv(self, report):
        with open('report.csv', 'w') as reportcsv:
            writer = csv.writer(reportcsv)
            for row in report:
                writer.writerow(row)

    def draw_endgame(self):
        ''' Shows the user the end game stats and generates a report.'''
        report = self.generate_report()
        self.write_endgame_csv(report)

        font = pygame.font.SysFont("Helvetica", 15)
        monofont = pygame.font.SysFont("monospace", 15)
        font_large = pygame.font.SysFont("Helvetica", 56)

        label = font_large.render("Game Over.", 1, (0, 0, 0))
        self.screen.blit(label, (260, 20))

        time = self.project.current_time - self.project.start_time
        label = font.render("You finished the project in: " + str(time) + " hours", 1, (0, 0, 0))
        self.screen.blit(label, (80, 100))

        # TODO: Get real cost value here when implemented, currently dummy.
        cost = 1337
        label = font.render("Profit Margin: $" + str(cost), 1, (0, 0, 0))
        self.screen.blit(label, (80, 140))

        
        estimated_hours, actual_hours = self.total_person_hours()
        label = font.render("Total man hours used:" + str(actual_hours) +
        " (estimate " + str(estimated_hours) + ")", 1, (0, 0, 0))
        self.screen.blit(label, (80, 180))

        
        if not self.hasList:
            my_list = gui.List(width=750, height=180)

            for (team, module, task, estimate, actual) in report:
                # I'm not proud of this
                s = team + (" " * (20 - len(team))) + task + (" " * (20 - len(task))) \
                + str(estimate) + (" " * (20 - len(str(estimate)))) + str(actual)
                
                l = gui.Label(s)
                l.set_font(monofont)
                my_list.add(l)

            self.contain.add(my_list, 0, 180)
            self.app.init(self.contain)
            self.app.paint(self.screen)
            self.hasList = True
        else:
            self.app.paint(self.screen)
            self.app.update(self.screen)

    def draw(self):
        ''' The parent draw function of the end game screen .'''

        while(True):

            # Draw background
            padding = 20
            if(self.hasList):
                pygame.draw.rect(self.screen, 0x2DABFE, (padding , padding,
                                                     self.config["screenX"] - 20 - padding,
                                                     self.config["screenY"] - 40 - padding))
            # Draw endgame stats
            self.draw_endgame()

            self.refresh_screen()

            sleep(0.05)