from Project import Project
from Team import Team
from Location import Location
import threading
from Repeated_Timer import Repeated_Timer

def calc_progress(project):
    for location in project.locations:
        for team in location.teams:
            team.calc_progress(location.calc_mod())
            print team.task.progress


def run_engine(project):
    Repeated_Timer(1.0, calc_progress, project)

    
