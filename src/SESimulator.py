#!/usr/bin/env python

import pygame
from pgu import gui

import threading

from UI import game     #frontend mainscreen.
from engine import Simulation_Engine as simeng


class FrontEndThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        g = game.Game(None)

class BackEndThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        simeng.run_engine(None)


def main():
    pygame.init()
    frontend = FrontEndThread()
    backend = BackEndThread()
    frontend.start()
    backend.start()
    frontend.join()
    backend.join()

if __name__ == "__main__":
    main()