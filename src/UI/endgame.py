import pygame

class EndGame:

    def __init__(self,screen,config):
        self.screen = screen
        self.config = config

    def refresh_screen(self,):
        pygame.display.flip()

    def draw_endgame(self):
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
        #draw background
        pygame.draw.rect(self.screen, 0x2DABFE,(10, 10, self.config["screenX"] - 20, self.config["screenY"] - 40))
        #draw endgame stats
        self.draw_endgame()
        self.refresh_screen()
