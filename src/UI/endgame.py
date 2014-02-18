import pygame
import csv

class EndGame:
    def __init__(self, screen, config, project):
        self.screen = screen
        self.config = config
        self.project = project

    def generate_report(self):
        report = list()
        report.append(['Team', 'Module', 'Task', 'Estimated Time', 'Actual Time'])
        for location in self.project.locations:
            for team in location.teams:
                for task in team.completed_tasks:
                    estimated_hours = task.cost / team.size
                    report.append([team.name, task.module.name, task.name, estimated_hours, task.hours_taken])
        return report

    def refresh_screen(self):
        pygame.display.flip()

    def draw_endgame(self):
        report = self.generate_report()
        with open('report.csv', 'w') as reportcsv:
            writer = csv.writer(reportcsv)
            for row in report:
                writer.writerow(row)

        font = pygame.font.SysFont("Helvetica", 15)
        font_large = pygame.font.SysFont("Helvetica", 56)

        label = font_large.render("Game Over.", 1, (0, 0, 0))
        self.screen.blit(label, (250, 100))

        label = font.render("You Finished the project in:", 1, (0, 0, 0))
        self.screen.blit(label, (250, 200))

        label = font.render("Profit Margin:", 1, (0, 0, 0))
        self.screen.blit(label, (250, 250))

        label = font.render("Rank:", 1, (0, 0, 0))
        self.screen.blit(label, (250, 300))

    def draw(self):
        # Draw background
        pygame.draw.rect(self.screen, 0x2DABFE, (10, 10,
                                                 self.config["screenX"] - 20,
                                                 self.config["screenY"] - 40))
        # Draw endgame stats
        self.draw_endgame()
        self.refresh_screen()
