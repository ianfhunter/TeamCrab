from Project import Project
from Team import Team
from Location import Location
import threading
import datetime
from time import sleep
from Repeated_Timer import Repeated_Timer
from global_config import config

from UI import game
from global_config import config

# gmt_time is represented as a list [hours, day, month, year]
gmt_time = datetime.datetime(2014,1,1,0,0,0)
finished = False
project = None
game_obj = None

def all_finished():
    ''' Returns True when all modules in all modules have completed, False otherwise
    '''
    global project
    for module in project.modules:
        if not module.completed:
            return False
    return True

def calc_progress(gmt_time):
    ''' This function calculates the progress of each module assigned to each team 
    if the team is currently working. A team is considered to be working between 
    9:00 and 17:00 local time.
    '''
    global project
    global cmd_args
    for location in project.locations:
        local_time = (gmt_time.hour + location.time_zone) % 24
        if local_time >= 9 and local_time <= 17:
            for team in location.teams:
                project.cash -= (team.salary*team.size)
                team.calc_progress()

                if team.module:
                    if local_time is 9:
                        if location.calc_fail(project.home_site):
                            team.module.add_problem()
                            print "NEW PROBLEM AT SITE ", location.name, "List of problems to occur at site to date: "
                            for x in team.module.problems_occured:
                                print x
                    if not cmd_args["P_SUPPRESS"]:
                        print 'Module:', team.module.name, '- Progress:', \
                            str(team.module.progress), '- Expected Cost:', \
                            str(team.module.expected_cost), '- Actual Cost:', \
                            str(team.module.actual_cost)
                else:
                    if not cmd_args["P_SUPPRESS"]:
                        print 'Warning: Team ' + team.name + ' has no module assigned.'


def progress_time():
    ''' This function is called every x seconds to "progress" the game by 1 hour.
    '''
    global gmt_time
    gmt_time += datetime.timedelta(hours=1)

    global cmd_args
    if not cmd_args["P_SUPPRESS"]:
        print str(gmt_time.day) + "-" + str(gmt_time.month) + "-" + str(gmt_time.year) + " " + str(gmt_time.hour) + ":00 GMT"

    calc_progress(gmt_time)

    global project
    global game_obj

    project.current_time += datetime.timedelta(hours=1)    #add to overall

    game_obj.update(project)  # Tell UI to update

    global finished
    finished = all_finished()
    if finished:
        timer.stop()


def run_engine(game, proj,c_args):
    ''' Runs the backend engine for the game.
    '''
    global cmd_args
    cmd_args = c_args

    global project
    project = proj

    project.calc_nominal_schedule(config["developer_period_effort_value"])

    global game_obj
    game_obj = game


    thread_time = (0, 0)
    global timer
    timer = Repeated_Timer(config["game_speed"], progress_time)

    while not finished:
        sleep(1)

        # Main logic of the simulator will go here

    
