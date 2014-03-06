from Module import Module
from Location import Location
import datetime

class Project():
    def __init__(self, name, method, budget, revenue_tier):
        self.name = name
        self.development_method = method
        self.delivery_date = None
        self.budget = budget
        self.cash = budget
        self.expected_yearly_revenue = revenue_tier.expected_yearly_profits()
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

    def months_behind_schedule(self):
        # Returns a number of days late, divide by 30 to get number of months late
        delta = self.delivery_date - self.start_time
        days_late = delta.days
        num_months_late = days_late/30
        return num_months_late

    def game_score(self):
        num_months_late = self.months_behind_schedule() 
        score = self.cash + ((6 - num_months_late) * (self.expected_yearly_revenue / 12))
        return score

    # From email:
    # expected_budget =
    #  [sum(module estimated effort) /  (avg_developer_effort_day * num_developers)] * 1.24
    def expected_budget(self, developer_effort_day):
        total_module_effort = 0
        for module in self.modules:
            total_module_effort += module.cost
        num_developers = 0
        for location in self.locations:
            num_developers += location.current_size
        return (total_module_effort / (developer_effort_day * num_developers) * 1.24)

    def actual_budget(self):
        return self.budget

    # From e-mail:
    # expected_revenue = expected_early_revenue / 2
    def expected_revenue(self):
        return self.expected_early_revenue / 2

    def actual_revenue(self):
        num_months_late = self.months_behind_schedule() 
        actual_revenue = (6 - num_months_late) * (self.expected_yearly_revenue / 12)
        return actual_revenue
