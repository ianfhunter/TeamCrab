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
    def __init__(self, game, proj,start_screen):
        threading.Thread.__init__(self)
        self.proj = proj
        self.game = game
        self.start_screen = start_screen

    def run(self):
        self.start_screen.run()
        global setup_finished
        setup_finished = True
        self.game.run()

class BackEndThread(threading.Thread):
    def __init__(self, game, proj):
        threading.Thread.__init__(self)
        self.proj = proj
        self.game = game

    def run(self):
        global setup_finished
        while(not setup_finished):
            sleep(1)
        #start simulation once game params have been setup
        simeng.run_engine(self.game, self.proj)

def main():
    # Parse arguments passed to game
    parser = argparse.ArgumentParser(description='Software Engineering Simulator')
    parser.add_argument('-l','--load', help='Load a saved game or default scenario', metavar='game')
    args = vars(parser.parse_args())

    enable_vsync()
    pygame.init()

    if args['load']:
        exec('from games import %s as chosen_game' % args['load'])
        project = chosen_game.load_game()
    else:
        project = populate.load_game()
    
    project.calc_nominal_schedule(config["developer_period_effort_value"])
    screen = pygame.display.set_mode((config["screenX"], config["screenY"]))

    sScreen = start_screen.Start_Screen(config,screen)
    glob_game = game.Game(project, config,screen)

    frontend = FrontEndThread(glob_game,project,sScreen)
    backend = BackEndThread(glob_game,project)
    frontend.start()
    backend.start()
    backend.join()
    glob_game.endgame(project)
    glob_game.update(project)
    frontend.join()

if __name__ == "__main__":
    main()
