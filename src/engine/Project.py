from Module import Module
from Location import Location
import datetime
from global_config import config

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

    def home_site(self, site):
        self.home_site = site

    def calc_nominal_schedule(self, dev_effort_val):
        if self.development_method == 'Agile':
            max_team_cost = 0
            for location in self.locations:
                for team in location.teams:
                    team_cost = 0
                    for module in team.modules:
                        module.calc_deadline(self.start_time, team.size)
                        team_cost += module.expected_cost/team.size
                    if team_cost > max_team_cost:
                        max_team_cost = team_cost
            nominal_schedule = max_team_cost / dev_effort_val
            self.delivery_date = self.start_time + datetime.timedelta(days=nominal_schedule/config["developer_daily_effort"])

    def days_behind_schedule(self):
        # Returns a number of days late, divide by 30 to get number of months late
        delta = self.delivery_date - self.start_time
        days_late = delta.days
        return days_late 

    def game_score(self):
        num_months_late = self.days_behind_schedule() / 30.0 
        score = self.cash + ((6 - num_months_late) * (self.expected_yearly_revenue / 12))
        return int(score)

    # From email:
    # expected_budget =
    #  [sum(module estimated effort) /  (avg_developer_effort_day * num_developers)] * 1.24
    # NOTE: IMPORTANT - This calculation doesn't take into account developer wages
    # An adjustment was made below to account for this, rounding up a day.
    def expected_budget(self, developer_effort_day):
        total_module_effort = 0
        total_daily_cost = 0  # in $CURRENCY
        for module in self.modules:
            total_module_effort += module.expected_cost
        num_developers = 0
        for location in self.locations:
            num_developers += location.current_size
            total_daily_cost += (location.salary * developer_effort_day * location.current_size)
        total_effort_hours = ((float(total_module_effort) / (float(developer_effort_day) * float(num_developers)) * 1.24))
        total_effort_days = (total_effort_hours/config["developer_daily_effort"]) + 1
        return (float(total_effort_days) * float(total_daily_cost))

    def actual_budget(self):
        return self.budget

    # From e-mail:
    # expected_revenue = expected_early_revenue / 2
    def expected_revenue(self):
        return self.expected_yearly_revenue / 2

    # From e-mail:
    # actual_revenue = (6 - num_months_late) * (expected_yearly_revenue/12)
    def actual_revenue(self):
        num_months_late = self.days_behind_schedule() / 30.0
        actual_revenue = (6 - num_months_late) * (self.expected_yearly_revenue / 12)
        return int(actual_revenue)
