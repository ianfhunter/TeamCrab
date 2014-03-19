from Module import Module
from Location import Location
import datetime
from global_config import config

class Project():
    def __init__(self, name, method, budget, revenue_tier):
        self.name = name
        self.development_method = method
        self.delivery_date = None
        self.budget = 0
        self.cash = budget
        self.expected_yearly_revenue = revenue_tier.expected_yearly_profits()
        self.modules = list()
        self.locations = list()
        self.start_time = datetime.datetime(2014,1,1,0,0,0)
        self.current_time = datetime.datetime(2014,1,1,0,0,0)

    def calc_nominal_schedule(self):
        if self.development_method == 'Agile':
            project_deadline = self.start_time
            for location in self.locations:
                for team in location.teams:
                    last_deadline = self.start_time
                    for module in team.modules:
                        module.calc_deadline(last_deadline, team.size, 9-location.time_zone)
                        last_deadline = module.deadline
                        print last_deadline
                    if last_deadline > project_deadline:
                        project_deadline = last_deadline
            self.delivery_date = project_deadline

    def days_behind_schedule(self):
        # Returns a number of days late, divide by 30 to get number of months late
        delta = self.current_time - self.delivery_date
        days_late = delta.days
        return days_late 

    def game_score(self):
        score_cash = self.cash
        if score_cash < 0:
            score_cash *= config["cash_penalty"]
        return int(score_cash + self.actual_revenue())

    # From email:
    # expected_budget =
    #  [sum(module estimated effort) /  (avg_developer_effort_day * num_developers)] * 1.24
    # NOTE: IMPORTANT - This calculation doesn't take into account developer wages
    # An adjustment was made below to account for this, rounding up a day.
    def expected_budget(self):
        '''
        Calculates expected budget.

        @untestable -  This relies on a value from the global config which is likely to change often so it cannot be veried properly.
        '''
        total_module_effort = 0.0
        for module in self.modules:
            total_module_effort += module.expected_cost
        total_effort_hours = total_module_effort *config["developer_period_effort_value"]  * config["budget_mod"]
        return total_effort_hours * config["developer_hourly_cost"]

    def actual_budget(self):
        return self.budget

    # From e-mail:
    # expected_revenue = expected_early_revenue / 2
    def expected_revenue(self):
        return self.expected_yearly_revenue / 2

    # From e-mail:
    # actual_revenue = (6 - num_months_late) * (expected_yearly_revenue/12)
    def actual_revenue(self):
        num_months_late = self.days_behind_schedule() * 12.0 / 365.0
        actual_revenue = (6 - num_months_late) * (self.expected_yearly_revenue / 12.0)
        return int(actual_revenue*100) / 100.0
