import pygame,os
from pgu import gui

glob_game = None


def pauseClick(self):
    #to bring up menu & pause clock
    print("Pause Clicked!")
#    os._exit(1)



class Game:
    def __init__(self, gamedata):
        glob_game = self
        self.gamedata = gamedata
        self.firstDraw = True

        #surface setup
        self.screen = pygame.display.set_mode((850, 480))
        self.app = gui.App()
        self.app.connect(gui.QUIT,self.app.quit,None)        
        self.contain = gui.Container(width = 850,height = 480)
       
    def run(self):    
        self.draw()
        while True:
            #handle events
            for event in pygame.event.get():
                #tell PGU  about all events.
                self.app.event(event)
                #handle quitting
                if event.type == pygame.QUIT:
                    os._exit(1)
                #escape to exit
                # elif event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_ESCAPE:
                #         os._exit(1)

    def update(self,project):
        self.gamedata = project
        self.draw()
 
    def draw(self):
        # draw map
    
        worldMap = pygame.image.load("../media/map.png")
        self.screen.blit(worldMap, (0, 0))
        
        # draw bottom bar
        pygame.draw.rect(self.screen, 0x9b9b9b, (0, 460, 850, 20))

        # Balance & Statistics
        myfont = pygame.font.SysFont("Helvetica", 15)
        label = myfont.render("-$" + str(int(self.gamedata.locations[0].teams[0].task.progress)), 1, (255,0,0))
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
        btn.connect(gui.CLICK, pauseClick,None)

        self.contain.add(btn,780,460)
        self.app.init(self.contain)       
        self.app.paint(self.screen)

        #update the screen - but only the updated portion of it so we save on refreshing the entire screen
        if self.firstDraw:
            pygame.display.flip()
            self.firstDraw = False
        else:
            pygame.display.update((0, 460, 850, 20))    #bottom bar
            pygame.display.update((0, 320, 200, 140))    #grey box
# if __name__ == "__main__":
#     g = Game(None)
