import pygame
import json 
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
        self.font = pygame.font.SysFont("Helvetica", 15)
        self.monofont = pygame.font.SysFont("monospace", 12)
        self.font_large = pygame.font.SysFont("Helvetica", 56)


    def generate_report(self):
        ''' Generate table with information about the end of the game '''
        report = {}
        report["score"] = self.project.game_score()
        report["remaining_cash"] = self.project.cash
        report["total_time"] = str(self.project.current_time - self.project.start_time)
        report["months_behind_schedule"] = self.project.months_behind_schedule()
        report["expected_budget"] = self.project.expected_budget(self.config["developer_daily_effort"])
        report["actual_budget"] = self.project.actual_budget()
        report["expected_revenue"] = self.project.expected_revenue()
        report["actual_revenue"] = self.project.actual_revenue()

        # Generate table to compare estimated/actual effort broken down by module
        effort_table = []
# module name | team name | team size | expected cost (man hours) | actual cost (man hours) | wall clock time (actual days) | productive time on task
        '''
        expected_cost()
        actual_cost()
        wall_clock_time()
        productive_time_on_task()

        '''
        effort_table.append(['Team', 'Module', 'Team', 'Estimated', 'Actual cost', 'Wall clock', 'Productive'])
        effort_table.append(['Name', 'Name',   'Size', 'cost (mh)', '(mh)'       , 'time (hrs)', 'time (hrs)'])
        total_estimated = 0
        total_actual = 0
        for location in self.project.locations:
            for team in location.teams:
                for module in team.completed_modules:
                    expected = module.expected_cost
                    actual = module.actual_cost
                    wall = module.wall_clock_time()
                    productive = module.productive_time_on_task()
                    effort_table.append([team.name, module.name, team.size, expected, actual, wall, productive])
                    total_estimated += expected
                    total_actual += actual
        # Add totals row
        # effort_table.append(["Total", "Total", total_estimated, total_actual])
        
        report["effort_table"] = effort_table
        
        return report

    def report_table_line(self, team, module, size, estimate, actual, wall, productive):
        s = ""
        s += team + (" " * (20 - (len(team))))
        s += module + (" " * (20 - len(module)))
        s += str(size) + (" " * (20 - (len(str(size)))))
        s += str(estimate) + (" " * (20 - (len(str(estimate)))))
        s += str(actual) + (" " * (20 - (len(str(actual)))))
        s += str(wall) + (" " * (20 - len(str(wall))))
        s += str(productive)
        return s

    def total_person_hours(self):
        total_estimated = 0
        total_actual = 0
        for location in self.project.locations:
            for team in location.teams:
                for module in team.completed_modules:
                    estimated_hours = module.expected_cost / team.size
                    total_estimated += estimated_hours    
                    total_actual += module.hours_taken
        return (total_estimated, total_actual)

    def refresh_screen(self):
        pygame.display.flip()

    def write_endgame_json(self, report):
        outfile = open('report.json', 'w')
        outfile.write(json.dumps(report))

    def draw_endgame(self):
        ''' Shows the user the end game stats and generates a report.'''
        report = self.generate_report()
        self.write_endgame_json(report)

        font = self.font 
        monofont = self.monofont
        font_large = self.font_large

        label = font_large.render("Game Over.", 1, (0, 0, 0))
        self.screen.blit(label, (260, 20))

        # Total time elapsed
        time = report["total_time"]
        label = font.render("You finished the project in: " + str(time) + " hours", 1, (0, 0, 0))
        self.screen.blit(label, (80, 100))

        # Game score
        score = report["score"]
        label = font.render("Game score: " + str(score) + " points", 1, (0, 0, 0))
        self.screen.blit(label, (80, 120))

        # Leftover cash
        cost = report["remaining_cash"]
        label = font.render("Profit Margin: $" + str(cost), 1, (0, 0, 0))
        self.screen.blit(label, (80, 140))

        # Person hours
        estimated_hours, actual_hours = self.total_person_hours()
        label = font.render("Total person hours used: " + str(actual_hours) +
            " (estimate " + str(estimated_hours) + ")", 1, (0, 0, 0))
        self.screen.blit(label, (80, 160))

        # Budget calculations
        expected_budget = report["expected_budget"]
        actual_budget= report["actual_budget"]
        label = font.render("Budget (estimate/actual): $" + str(expected_budget) + 
            " / $" + str(actual_budget), 1, (0, 0, 0))
        self.screen.blit(label, (80, 180))

        # Revenue calculations
        expected_revenue = report["expected_revenue"]
        actual_revenue = report["actual_revenue"]
        label = font.render("Revenue (estimate/actual): $" + str(expected_revenue) + 
            " / $" + str(actual_revenue), 1, (0, 0, 0))
        self.screen.blit(label, (80, 200))

        if not self.hasList:

            my_list = gui.List(width=750, height=180)
            # effort_table.append([team.name, module.name, team.size, expected, actual, wall, productive])
            for (team, module, size, estimate, actual, wall, productive) in report["effort_table"]:
                s = self.report_table_line(team, module, size, estimate, actual, wall, productive)

                l = gui.Label(s)
                l.set_font(monofont)
                my_list.add(l)

            # We need to empty the container's widgets before adding updated ones or else
            # pgu will draw the new ones over the old ones.
            self.contain.widgets = []    
            self.contain.add(my_list, 0, 200)
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
