from Project import Project
from Team import Team
from Location import Location
import threading
from Repeated_Timer import Repeated_Timer

from UI import game     #frontend 


# gmt_time is represented as a tuple (hours, minutes)
gmt_time = [0, 0]
finished = False
project = None
game_obj = None

def calc_progress(gmt_time):
    global project
    for location in project.locations:
        local_time = (gmt_time[0] + location.time_zone) % 24
        if local_time >= 9 and local_time <= 17 :
            for team in location.teams:
                team.calc_progress(location.calc_mod())             
                print 'Task: '+ team.task.name + ' - Progress: ' + str(team.task.progress)

def progress_time():

  
    gmt_time[0] += 1
    if gmt_time[0] == 24:
        gmt_time[0] = 0

    print gmt_time

    calc_progress(gmt_time)

    global project
    global game_obj
    game_obj.update(project)    #tell UI to update



def run_engine(game,proj):
    global project
    project = proj

    global game_obj
    game_obj = game

    thread_time = (0, 0)
    timer = Repeated_Timer(0.5, progress_time)

    while not finished:
        # Main logic of the simulator will go here
        pass

    
