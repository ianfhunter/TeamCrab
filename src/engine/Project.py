from Module import Module
from Location import Location
import datetime

class Project():
    def __init__(self, name, method, budget):
        self.name = name
        self.development_method = method
        self.delivery_date = None
        self.cash = budget
        self.modules = list()
        self.locations = list()
        self.start_time = datetime.datetime(2014,1,1,0,0,0)
        self.current_time = datetime.datetime(2014,1,1,0,0,0)

    def calc_nominal_schedule(self, dev_effort_val):
        if self.development_method == 'Agile':
            max_team_cost = 0
            for location in self.locations:
                for team in location.teams:
                    team_cost = 0
                    for module in team.modules:
                        team_cost += module.cost/team.size
                    if team_cost > max_team_cost:
                        max_team_cost = team_cost
            nominal_schedule = max_team_cost / dev_effort_val
            self.delivery_date = self.start_time + datetime.timedelta(days=nominal_schedule/8)
