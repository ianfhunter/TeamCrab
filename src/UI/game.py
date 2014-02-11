import pygame
import pgu

class Game:
    def __init__(self, gamedata):
        self.gamedata = gamedata
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.draw()
        while True:
            pass

    def draw(self):
        # draw map
        worldMap = pygame.image.load("../../media/map.png")
        self.screen.blit(worldMap, (0, 0))
        # draw bottom line
        pygame.draw.rect(self.screen, 0x33333, (0, 460, 640, 20))
            # balance
        # draw locations
        # draw currently selected location
        pygame.draw.rect(self.screen, 0x3f3f3f, (0, 310, 200, 150))
        # draw pause button
        pygame.display.flip()
       
if __name__ == "__main__":
    g = Game(None)
