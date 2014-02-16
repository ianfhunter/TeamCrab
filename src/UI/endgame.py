import pygame

def refresh_screen():
    # ''' Updates the screen - but only the updated portion of it so we save on
    # refreshing the entire screen.
    # '''
    # if self.firstDraw:
    pygame.display.flip()
        # self.firstDraw = False
    # else:
        # pygame.display.update((0, 460, 850, 20))    #bottom bar
        # pygame.display.update((0, 320, 200, 140))    #grey box

def draw_endgame(screen,config):
    font = pygame.font.SysFont("Helvetica", 15)
    font_large = pygame.font.SysFont("Helvetica", 56)

    label = font_large.render("Game Over.", 1, (0, 0, 0))
    screen.blit(label, (250, 100))


    label = font.render("You Finished the project in:", 1, (0, 0, 0))
    screen.blit(label, (250, 200))

    label = font.render("Profit Margin:", 1, (0, 0, 0))
    screen.blit(label, (250, 250))

    label = font.render("Rank:", 1, (0, 0, 0))
    screen.blit(label, (250, 300))




def draw(screen,config):
    #draw background
    pygame.draw.rect(screen, 0x2DABFE,(10, 10, config["screenX"] - 20, config["screenY"] - 40))
    #draw endgame stats
    draw_endgame(screen,config)
    refresh_screen()
 #   print "HI"