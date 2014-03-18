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

class SimulationEngine():
    ''' @untestable - Would require running an entire scenario in the game to test
    '''
    def __init__(self):
        # gmt_time is represented as a list [hours, day, month, year]
        self.gmt_time = datetime.datetime(2014,1,1,0,0,0)
        self.finished = False
        self.project = None
        self.game_obj = None

    def all_finished(self):
        ''' Returns True when all modules in all modules have completed, False otherwise
        '''
        for module in self.project.modules:
            if not module.completed:
                return False
        return True

    def calc_progress(self):
        ''' This function calculates the progress of each module assigned to each team 
        if the team is currently working. A team is considered to be working from 
        9:00 for a number of hours based on "developer_daily_effort".
        '''
        for location in self.project.locations:
            local_time = (self.gmt_time.hour + location.time_zone) % 24
            for team in location.teams:
                if team.module:
                    team.module.total_hours += 1     
                if local_time >= 9 and local_time <= 9 + config["developer_daily_effort"]:
                    self.project.cash -= config["developer_hourly_cost"] * team.size
                    self.project.budget += config["developer_hourly_cost"] * team.size
                    team.calc_progress(self.gmt_time)
                    if team.module:
                        if location.calc_fail(self.project.home_site):
                            problem = team.module.add_problem()
                            if problem and not self.cmd_args["P_SUPPRESS"]:
                                print "Problem occured at", location.name
                                print "Problem:", problem
                        if not self.cmd_args["P_SUPPRESS"]:
                            print 'Module:', team.module.name, '(', location.name, ')', '- Current Effort Expended:', \
                                str(team.module.progress), 'ph - Expected Total Effort:', \
                                str(team.module.expected_cost), 'ph - Actual Total Effort:', \
                                str(team.module.actual_cost), 'ph (ph = person-hours)'
                    else:
                        if not self.cmd_args["P_SUPPRESS"]:
                            print 'Warning: Team ' + team.name + ' has no module assigned.'


    def progress_time(self):
        ''' This function is called every x seconds to "progress" the game by 1 hour.
        '''
        self.gmt_time += datetime.timedelta(hours=1)

        if not self.cmd_args["P_SUPPRESS"]:
            print str(self.gmt_time.day) + "-" + str(self.gmt_time.month) + "-" + str(self.gmt_time.year) + " " + str(self.gmt_time.hour) + ":00 GMT"

        self.calc_progress()

        self.project.current_time += datetime.timedelta(hours=1)    #add to overall

        self.game_obj.update(self.project)  # Tell UI to update

        self.finished = self.all_finished()
        if self.finished:
            self.timer.stop()


    def run_engine(self, game, proj,c_args):
        ''' Runs the backend engine for the game.
        '''
        self.cmd_args = c_args
        self.project = proj

        self.project.calc_nominal_schedule()

        self.game_obj = game


        thread_time = (0, 0)
        self.timer = Repeated_Timer(config["game_speed"], self.progress_time)

        while not self.finished:
            sleep(1)

    def pause(self):
        self.timer.stop()

    def resume(self):
        self.timer.start()
