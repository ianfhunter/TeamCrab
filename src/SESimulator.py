#!/usr/bin/env python

import pygame
from pgu import gui

import threading

from UI import game     #frontend mainscreen.
from engine import Simulation_Engine as simeng
import test_game as populate

class FrontEndThread(threading.Thread):
    def __init__(self,game,proj):
        threading.Thread.__init__(self)
        self.proj = proj
        self.game = game

    def run(self):
        self.game.run()
        
class BackEndThread(threading.Thread):
    def __init__(self,game,proj):
        threading.Thread.__init__(self)
        self.proj = proj
        self.game = game

    def run(self):
        simeng.run_engine(self.game,self.proj)


def main():
    pygame.init()

    project = populate.load_test_game()
    glob_game = game.Game(project)


    frontend = FrontEndThread(glob_game,project)
    backend = BackEndThread(glob_game,project)
    frontend.start()
    backend.start()
    frontend.join()
    backend.join()

if __name__ == "__main__":
    main()