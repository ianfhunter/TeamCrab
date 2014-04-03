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
        self.total_estimated_effort = 0

    def calc_nominal_schedule(self):
        if self.development_method == 'Agile':
            project_deadline = self.start_time
            for location in self.locations:
                for team in location.teams:
                    last_deadline = self.start_time
                    for module in team.modules:
                        module.calc_deadline(last_deadline, team.size, 9-location.time_zone)
                        last_deadline = module.deadline
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
        self.total_estimated_effort = total_module_effort *config["developer_period_effort_value"] 
        return self.total_estimated_effort * config["developer_hourly_cost"] * config["budget_mod"]


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


    def add_intervention(self,location_name, intervention_type):
        ''' 
            Adds an intervention to a site, meaning problem rates are lowered
            
            Intervention Costs are subtracted from Current Cash.
            Intervention Impact is added to intervention_level which increases the intervention_modifier when caclulating failures.

            Lvl  Name        Cost       Impact
            0    None        $0         +0
            1    Low         $5,000     +1
            2    Med Low     $25,000    +2
            3    Med High    $125,000   +3
            4    High        $500,000   +4

            TODO: Add tests. Side-Effects?
        '''
        cost = 0
        impact = 0

        #GEO INTERVENTIONS
        if intervention_type == "Exchange Program":
            #High,         Medium High
            cost = 4
            impact = 3
        elif intervention_type == "Synchronous Communication Possibilities":
            #Med High,     Low
            cost = 3
            impact = 1
        elif intervention_type == "Support for Video Conference":
            #Med Low,      Low
            cost = 2
            impact = 1
        elif intervention_type == "Suitable select of Communication Tools":
            #Med Low,      Low
            cost = 2
            impact = 1

        #TIME INTERVENTIONS
        elif intervention_type == "Relocate to Adjacent Time Zone":
            #High,         High
            cost = 4
            impact = 4
        elif intervention_type == "Adopt Follow The Sun Development":
            #Med High,     High
            cost = 3
            impact = 4
        elif intervention_type == "Create Bridging Team":
            #Med High,     Med High
            cost = 3
            impact = 3

        #CULTURE INTERVENTIONS
        elif intervention_type == "Face to Face Meeting":
            #High,         Med Low
            cost = 4
            impact = 2
        elif intervention_type == "Cultural Training":
            #Med High,     Med Low
            cost = 3
            impact = 2
        elif intervention_type == "Cultural Liason/Ambassador":
            #Med High,     Med High
            cost = 3
            impact = 3
        elif intervention_type == "Adopt low-context communication style":
            #Low,         Low
            cost = 1
            impact = 1
        elif intervention_type == "Reduce interaction between teams":
            #Low,         Low
            cost = 1
            impact = 1

        for location in self.locations:
            if location.name == location_name:
                location.intervention_add(intervention_type,impact)
                break

        if cost == 1:
            self.cash -= 5000 
        elif cost == 2:
            self.cash -= 25000            
        elif cost == 3:
            self.cash -= 125000            
        elif cost == 4:
            self.cash -= 500000
