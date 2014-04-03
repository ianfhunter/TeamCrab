#!/usr/bin/env python

import pygame
import sys
from pgu import gui

import threading
from time import sleep
import argparse

from engine import SimulationEngine
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
    def __init__(self, game, proj,cmd_args, engine):
        threading.Thread.__init__(self)
        self.proj = proj
        self.game = game
        self.cmd_args = cmd_args
        self.simeng = engine

    def run(self):
        self.simeng.run_engine(self.game, self.proj,self.cmd_args)

def main():
    #setup standard stuff
    enable_vsync()
    pygame.init()

    parser = argparse.ArgumentParser(description='Software Engineering Simulator')
    parser.add_argument('-q','--quiet', help='supress process simulator logging',action='store_true')
    args = vars(parser.parse_args())

    cmd_args = {}
    cmd_args["P_SUPPRESS"] = False
    if args["quiet"]:
        cmd_args["P_SUPPRESS"] = True
        print "Process Simulator is being supressed. Remove -q/--quiet to show"

    #create our window
    screen = pygame.display.set_mode((config["screenX"], config["screenY"]))

    #startup dialog
    sScreen = start_screen.Start_Screen(config,screen)
    project = sScreen.run()

    # Create the simulator engine
    engine = SimulationEngine.SimulationEngine()

    glob_game = game.Game(project, config, screen, engine)


    #begin simulator
    frontend = FrontEndThread(glob_game, project)
    backend = BackEndThread(glob_game, project, cmd_args, engine)
    frontend.start()
    backend.start()
    backend.join()
    glob_game.endgame(project)
    glob_game.update(project)
    frontend.join()

if __name__ == "__main__":
    main()
