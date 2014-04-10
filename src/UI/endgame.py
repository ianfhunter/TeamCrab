import pygame
from pgu import gui
from time import sleep
import logic

class EndGame:
    '''
    End of game UI elements

    @untestable - entire class untestable as it just draws UI elements onscreen.
    '''
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
        self.monofont = pygame.font.SysFont("monospace", 14)
        self.bellerose_font = pygame.font.Font(self.config["bellerose_font"], 56)
        self.font_large = pygame.font.SysFont("Helvetica", 56)

    def refresh_screen(self):
        '''
        Refreshes the endgame screen.
        '''
        pygame.display.flip()

    def draw_endgame(self):
        ''' Shows the user the end game stats and generates a report.'''
        report = logic.generate_report(self.project)
        logic.write_endgame_json(report)

        font = self.font 
        monofont = self.monofont
        bellerose_font = self.bellerose_font

        label = bellerose_font.render("Game Over.", 1, (0, 0, 0))
        self.screen.blit(label, (270, -20))

        # Total time elapsed
        time = report["total_time"]
        label = font.render("You finished the project in: " + str(time) + " hours", 1, (0, 0, 0))
        self.screen.blit(label, (80, 80))

        # Nominal vs actual end times
        nominal_end = report["nominal_end_time"]
        actual_end = report["actual_end_time"]
        label = font.render("Nominal delivery date: " + str(nominal_end) + "    Actual delivery date: " + str(actual_end), 1, (0, 0, 0))
        self.screen.blit(label, (80, 100))

        # Game score
        score = report["score"]
        label = font.render("Game score: " + str(score) + " points", 1, (0, 0, 0))
        self.screen.blit(label, (80, 120))

        # Person hours
        estimated_hours, actual_hours = logic.total_person_hours(self.project)
        label = font.render("Total Staff Time: " + str(actual_hours) +
            " (estimate " + str(estimated_hours) + ")", 1, (0, 0, 0))
        self.screen.blit(label, (80, 140))

        # Leftover cash
        cost = report["endgame_cash"]
        label = font.render("Endgame cash (leftover budget + revenue): $" + str(cost), 1, (0, 0, 0))
        self.screen.blit(label, (80, 160))

        # Budget calculations
        expected_budget = report["expected_budget"]
        actual_budget= report["actual_budget"]
        penalty = report["budget_penalty"]
        label = font.render("Budget (estimate/actual): $" + str(expected_budget) + 
            " / $" + str(actual_budget), 1, (0, 0, 0))
        if penalty > 0:
             label = font.render("Budget (estimate/actual): $" + str(expected_budget) + 
                " / $" + str(actual_budget + penalty) + " (Actual spend of $" + 
                str(actual_budget) + " + penalty $" + str(penalty) +")", 1, (0, 0, 0))
        self.screen.blit(label, (80, 180))

        # Revenue calculations
        expected_revenue = report["expected_revenue"]
        actual_revenue = report["actual_revenue"]
        label = font.render("Revenue (estimate/actual): $" + str(expected_revenue) + 
            " / $" + str(actual_revenue), 1, (0, 0, 0))
        self.screen.blit(label, (80, 200))

        if not self.hasList:

            my_list = gui.List(width=800, height=195)
            # effort_table.append([team.name, module.name, team.size, expected, actual, wall, productive])
            for (team, module, size, estimate, actual, dollars, wall, productive) in report["effort_table"]:
                s = logic.report_table_line(team, module, size, estimate, actual, dollars, wall, productive)
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
        '''
        Draws the endgame screen.
        '''
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
