import pygame,os
from pgu import gui


def pauseClick():
    #to bring up menu & pause clock
    print("Pause Clicked!")
    os._exit(1)

def close():
    print "no"
    os._exit(1)


class Game:
    def __init__(self, gamedata):
        self.gamedata = gamedata
        
        #surface setup
        self.screen = pygame.display.set_mode((850, 480))
        self.app = gui.Desktop()
        self.app.connect(gui.QUIT,self.app.quit,None)
        
        self.contain = gui.Container(width = 850,height = 480)
        
        self.draw()
        while True:
            pass
 #           print "HI"
            #handle events
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         print "hi1"
            #         os._exit(1)
            #     elif event.type == KEYDOWN:
            #         if event.key == K_ESCAPE:
            #             print "hi2"
            #             os._exit(1)
 
    def draw(self):
        # draw map

        worldMap = pygame.image.load("../media/map.png")
        self.screen.blit(worldMap, (0, 0))
        
        # draw bottom bar
        pygame.draw.rect(self.screen, 0x9b9b9b, (0, 460, 850, 20))

        # Balance & Statistics
        myfont = pygame.font.SysFont("Helvetica", 15)
        label = myfont.render("-$500", 1, (255,0,0))
        self.screen.blit(label, (20, 460))
        label = myfont.render("Jul 21st 14:00 GMT", 1, (0,0,0))
        self.screen.blit(label, (200, 460))
        label = myfont.render("10 Items Needing Review", 1, (238,255,53))
        self.screen.blit(label, (400, 460))

        # draw locations - To be retrieved from backend
        for x in range (5):
            pygame.draw.circle(self.screen, 0x44FFFF, (x*10,x*10), 7)
        # draw currently selected location - Info retrieved from backend

        y = 320
        #background rect
        pygame.draw.rect(self.screen, 0xdedede, (0, y, 200, 140))

        #Icons and accompanying text
        workerIcon = pygame.image.load("../media/man.png")
        self.screen.blit(workerIcon, (1, 325))
        label = myfont.render("2 Teams", 1, (0,0,0))
        self.screen.blit(label, (40, y + 15))

        cogIcon = pygame.image.load("../media/cog.png")
        self.screen.blit(cogIcon, (1, 360))
        label = myfont.render("75% Efficiency", 1, (0,0,0))
        self.screen.blit(label, (40, y + 50))

        clockIcon = pygame.image.load("../media/clock.png")
        self.screen.blit(clockIcon, (1, 395))
        label = myfont.render("127 Days", 1, (0,0,0))
        self.screen.blit(label, (40, y + 85))

        targetIcon = pygame.image.load("../media/target.png")
        self.screen.blit(targetIcon, (1, 430))
        label = myfont.render("On Schedule", 1, (0,0,0))
        self.screen.blit(label, (40, y + 115))

        # draw pause button
        btn = gui.Button("Menu")
        btn.connect(gui.CLICK, pauseClick)
        self.contain.add(btn,780,460)
        
        self.screen.blit(btn.image,(btn.rect.x,btn.rect.y))
#        self.app.run(self.contain)
        #self.app.init(self.contain)
        pygame.display.flip()
       
# if __name__ == "__main__":
#     g = Game(None)
