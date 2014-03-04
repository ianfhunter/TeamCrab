import pygame
import csv
from pgu import gui

class EndGame:
    def __init__(self, screen, config, project):
        self.config = config
        self.project = project
        self.screen = screen
        self.app = gui.App()
        self.app.connect(gui.QUIT, self.app.quit, None)
        self.contain = gui.Container(width=400,
                                     height=400)

    def generate_report(self):
        ''' Generate table with information about the end of the game '''
        report = list()
        report.append(['Team', 'Module', 'Estimated Time', 'Actual Time'])
        for location in self.project.locations:
            for team in location.teams:
                for module in team.completed_modules:
                    estimated_hours = module.cost / team.size
                    report.append([team.name, module.name, estimated_hours, module.hours_taken])
        return report

    def total_person_hours(self):
        total_estimated = 0
        total_actual = 0
        for location in self.project.locations:
            for team in location.teams:
                for module in team.completed_modules:
                    estimated_hours = module.cost / team.size
                    total_estimated += estimated_hours    
                    total_actual += module.hours_taken
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


        my_list = gui.List(width=750, height=180)
        
        table = gui.Table(font=monofont)

        for (team, module, estimate, actual) in report:
            # I'm not proud of this
            s = team + (" " * (20 - len(team))) + module + (" " * (20 - len(module))) \
            + str(estimate) + (" " * (20 - len(str(estimate)))) + str(actual)
            
            l = gui.Label(s)
            l.set_font(monofont)
            my_list.add(l)

        # We need to empty the container's widgets before adding updated ones or else
        # pgu will draw the new ones over the old ones.
        self.contain.widgets = []    
        self.contain.add(my_list, 0, 180)
        self.app.init(self.contain)
        self.app.paint(self.screen)

    def draw(self):
        ''' The parent draw function of the end game screen .'''
        # Draw background
        padding = 20
        pygame.draw.rect(self.screen, 0x2DABFE, (padding , padding,
                                                 self.config["screenX"] - 20 - padding,
                                                 self.config["screenY"] - 40 - padding))
        # Draw endgame stats
        self.draw_endgame()

        self.refresh_screen()
