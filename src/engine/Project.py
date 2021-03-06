from Module import Module
from Location import Location
from Intervention import Intervention
import datetime
from global_config import config

class Project():
    '''
    This class represents a full project in the simulator engine.
    This includes all information related to teams, locations, modules, budget, and so.
    It is the top level object used by the simulator for representing a project.
    '''
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
        self.possible_interventions = [
                         #Name             #Impact     #Cost
            #Geo-Based
            Intervention("Exchange Program","High","Med High"),
            Intervention("Synchronous Communication Possibilities","Med High","Low"),
            Intervention("Support for Video Conference","Med Low","Low"),
            Intervention("Suitable select of Communication Tools","Med Low","Low"),
            #Time-Based
#            Intervention("Relocate to Adjacent Time Zone","High","High"),
#            Intervention("Adopt Follow The Sun Development","Med High","High"),
            Intervention("Create Bridging Team","Med High","Med High"),
            #Culture-Based
            Intervention("Face to Face Meeting","High","Med Low"),
            Intervention("Cultural Training","Med High","Med Low"),
            Intervention("Cultural Liason/Ambassador","Med High","Med High"),
            Intervention("Adopt low-context communication style","Low","Low"),
            Intervention("Reduce interaction between teams","Low","Low"),
        ]

    def calc_nominal_schedule(self):
        '''
        Calculates the nominal schedule for this project and sets self.delivery_date to the
        calculated date and time.
        '''
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
        '''
        Returns the number of days that this project is behind schedule.
        '''
        delta = self.current_time - self.delivery_date
        days_late = delta.days
        return days_late 

    def game_score(self):
        '''
        Calculates the game score for this project based on the formula given in the backlog.
        '''
        score_cash = self.cash
        if score_cash < 0:
            score_cash *= config["cash_penalty"]
        return int(score_cash + self.actual_revenue())

    def expected_budget(self):
        '''
        Calculates the expected budget for this project.

        From an email:
            expected_budget = [sum(module estimated effort) /  (avg_developer_effort_day * num_developers)] * 1.24
            NOTE: IMPORTANT - This calculation doesn't take into account developer wages
            An adjustment was made below to account for this, rounding up a day.

        @untestable -  This relies on a value from the global config which is likely to change often so it cannot be veried properly.
        '''

        total_module_effort = 0.0
        for module in self.modules:
            total_module_effort += module.expected_cost
        self.total_estimated_effort = total_module_effort *config["developer_period_effort_value"] 
        return self.total_estimated_effort * config["developer_hourly_cost"] * config["budget_mod"]


    def actual_budget(self):
        '''
        Returns the actual budget for this project.
        '''
        return self.budget

    def expected_revenue(self):
        '''
        Returns the expected revenue of this project.
        '''
        return self.expected_yearly_revenue / 2

    def actual_revenue(self):
        '''
        Returns the actual revenue of this project.
        Actual revenue is calculated as a function of the expected revenue and the number of days the project is late.
        '''
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
        '''
        for intervention in self.possible_interventions:
            #Get our intervention
            if intervention.name == intervention_type:
                #Get our location
                for location in self.locations:
                    if location.name == location_name:
                        #Add intervention to modifier & list of location
                        location.intervention_add(intervention.name,intervention.impact)
                        self.cash -= intervention.get_cost()
                        return
