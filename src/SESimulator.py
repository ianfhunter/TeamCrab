#!/usr/bin/env python

import pygame
import sys
from pgu import gui

import threading
from time import sleep
import argparse

from engine import SimulationEngine as simeng
from games import test_game as populate
from UI import game, endgame, start_screen

from global_config import config

setup_finished = False

#to avoid screen flickering
def enable_vsync():
    if sys.platform != 'darwin':
        return
    try:
        import ctypes
        import ctypes.util
        ogl = ctypes.cdll.LoadLibrary(ctypes.util.find_library("OpenGL"))
        # set v to 1 to enable vsync, 0 to disable vsync
        v = ctypes.c_int(1)
        ogl.CGLSetParameter(ogl.CGLGetCurrentContext(), ctypes.c_int(222), ctypes.pointer(v))
    except:
        print "Unable to set vsync mode, using driver defaults"



class FrontEndThread(threading.Thread):
    def __init__(self, game, proj):
        threading.Thread.__init__(self)
        self.proj = proj
        self.game = game

    def run(self):
        self.game.run()

class BackEndThread(threading.Thread):
    def __init__(self, game, proj):
        threading.Thread.__init__(self)
        self.proj = proj
        self.game = game

    def run(self):
        simeng.run_engine(self.game, self.proj)

def main():
    #setup standard stuff
    enable_vsync()
    pygame.init()

    #create our window
    screen = pygame.display.set_mode((config["screenX"], config["screenY"]))

    #startup dialog
    sScreen = start_screen.Start_Screen(config,screen)
    project = sScreen.run()

    glob_game = game.Game(project, config,screen)

    frontend = FrontEndThread(glob_game,project)
    backend = BackEndThread(glob_game,project)
    frontend.start()
    backend.start()
    backend.join()
    glob_game.endgame(project)
    glob_game.update(project)
    frontend.join()

if __name__ == "__main__":
    main()
