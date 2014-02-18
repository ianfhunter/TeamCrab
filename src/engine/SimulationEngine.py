from Project import Project
from Team import Team
from Location import Location
import threading
from time import sleep
from Repeated_Timer import Repeated_Timer

from UI import game

# gmt_time is represented as a list [hours, minutes]
gmt_time = [0, 0]
finished = False
project = None
game_obj = None


def calc_progress(gmt_time):
    ''' This function calculates the progress of each task assigned to each team 
    if the team is currently working. A team is considered to be working between 
    9:00 and 17:00 local time.
    '''
    global project
    for location in project.locations:
        local_time = (gmt_time[0] + location.time_zone) % 24
        if local_time >= 9 and local_time <= 17:
            for team in location.teams:
                team.calc_progress(location.calc_mod())
                print 'Module:', team.task.module.name, 'Task:', \
                    team.task.name, '- Actual Progress:', \
                    str(team.task.progress), '- expected Progress:', \
                    str(team.task.expected_progress)


def progress_time():
    ''' This function is called every x seconds to "progress" the game by 1 hour.
    '''
    gmt_time[0] += 1
    if gmt_time[0] == 24:
        gmt_time[0] = 0

    print gmt_time

    calc_progress(gmt_time)

    global project
    global game_obj
    game_obj.update(project)  # Tell UI to update


def run_engine(game, proj):
    ''' Runs the backend engine for the game.
    '''
    global project
    project = proj

    global game_obj
    game_obj = game

    thread_time = (0, 0)
    timer = Repeated_Timer(0.5, progress_time)

    while not finished:
        sleep(10)
        # Main logic of the simulator will go here
