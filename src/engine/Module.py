import random
from Task import Task
import datetime
from global_config import problems

class Module(object):
    def __init__(self, name, cost):
        self.name = name
        self.expected_cost = cost
        self.actual_cost = self.calculate_actual_cost(cost)
        self.actual_cost_base = self.actual_cost
        self.modules = list()
        self.tasks = list()
        self.completed_tasks = list()

        self.tasks.append(Task('design', int(self.actual_cost/100.0*15.0), int(self.expected_cost/100.0*15.0), self))
        self.tasks.append(Task('implementation', int(self.actual_cost/100.0*15.0), int(self.expected_cost/100.0*15.0), self))
        self.tasks.append(Task('unit_test', int(self.actual_cost/100.0*10.0), int(self.expected_cost/100.0*10.0), self))
        self.tasks.append(Task('integration', int(self.actual_cost/100.0*15.0), int(self.expected_cost/100.0*15.0), self))
        self.tasks.append(Task('system_test', int(self.actual_cost/100.0*15.0), int(self.expected_cost/100.0*15.0), self))
        self.tasks.append(Task('deployment', int(self.actual_cost/100.0*15.0), int(self.expected_cost/100.0*15.0), self))
        self.tasks.append(Task('acceptance_test', int(self.actual_cost/100.0*15.0), int(self.expected_cost/100.0*15.0), self))

        self.is_on_time = True # Keeps track of whether this module is on time for the traffic light system
        self.deadline = None # The deadline (by date) of this module
        self.overall_task_progress = 0 # This is the amount of effort put into fully completed tasks
        self.progress = 0.0
        self.completed = False
        self.stalled = False
        self.hours_taken = 0 # This is productive time
        self.total_hours = 0 # number of hours from start of project including non productive hours. 
        self.problems_occured = list()

    def calculate_actual_cost(self, expected_cost):
        ''' Returns the actual cost of a module based on a random variation between 75% and 125%.
        '''
        actual_cost_percent = float(random.randint(75, 125)) / 100.0
        return int(float(expected_cost) * actual_cost_percent)

    def get_task(self, name):
        ''' Returns the task object which matches the name specified if it exists, None otherwise.
        '''
        tasks = [task for task in self.tasks if task.name == name]
        if tasks:
            return tasks[0]
        else:
            return None

    def progress_module(self, progress, current_time):
        ''' Progress the module by the specified amount. This will progress tasks as necessary
        as well. If a task has reached its deadline then self.is_on_time will be updated appropriately.
        '''
        self.progress += progress
        
        # If the current task has completed then progress to the next task and place this one on the completed_tasks list
        if self.tasks:
            if self.progress >= (self.overall_task_progress + self.tasks[0].actual_cost):
                if current_time <= self.tasks[0].deadline:
                    self.is_on_time = True
                self.overall_task_progress += self.tasks[0].actual_cost
                self.completed_tasks.append(self.tasks[0])
                self.tasks.pop(0)
                if len(self.tasks) == 0:
                    print "LAST REMOVED"
                    print str(self.progress) + " " + str(self.overall_task_progress) + " " + str(self.actual_cost)

        # If the current task has reached its deadline then the module is not on time
        if self.tasks:
            if current_time >= self.tasks[0].deadline:
                self.is_on_time = False

    def calc_deadline(self, start_date, team_size):
        ''' Calculates the deadline for this module and stores it in self.deadline
        This also sets the deadlines for all tasks in this module
        '''
        work_hours_total = 0
        for task in self.tasks:
            work_hours_total += task.expected_cost/team_size
            task.deadline = start_date + datetime.timedelta(days=work_hours_total/8, hours=work_hours_total%8)
        self.deadline = self.tasks[-1].deadline

    def expected_cost(self):
        return self.expected_cost

    def actual_cost(self):
        return self.actual_cost

    def wall_clock_time(self):
        return self.total_hours

    def productive_time_on_task(self):
        return self.hours_taken

    def add_problem(self):
        prob = random.randint(1, 5)
        self.problems_occured.append(problems[prob][0])
        self.actual_cost += self.actual_cost_base * problems[prob][1]

