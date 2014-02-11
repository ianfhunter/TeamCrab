from Project import Project
from Team import Team
from Location import Location
import threading
from Repeated_Timer import Repeated_Timer

# gmt_time is represented as a tuple (hours, minutes)
gmt_time = [0, 0]
finished = False
project = None

def calc_progress():
    global project
    for location in project.locations:
        for team in location.teams:
            team.calc_progress(location.calc_mod())

def progress_time():
    update_progress = threading.Thread(target = calc_progress)
    update_progress.start()

    gmt_time[1] += 1
    if gmt_time[1] == 60:
        gmt_time[1] = 0
        gmt_time[0] += 1
    if gmt_time[0] == 24:
        gmt_time[0] = 0

    update_progress.join()
    print gmt_time


def run_engine(proj):
    global project
    project = proj
    thread_time = (0, 0)
    timer = Repeated_Timer(1.0, progress_time)

    while not finished:
        # Main logic of the simulator will go here
        pass

    
