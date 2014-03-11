import random
from Task import Task
import datetime

def random_element(prog):
    ''' Generates a random value between -25 and 25 used as a percentage to offset prog.
    '''
    amount = float(random.randint(-25, 25))
    direction = random.choice([-1, 1])
    return prog * (1 + (amount / 100.0))

class Module(object):
    def __init__(self, name, cost):
        self.name = name
        self.expected_cost = cost
        self.actual_cost = random_element(cost)
        self.modules = list()
        self.tasks = list()
        self.completed_tasks = list()

        self.tasks.append(Task('design', self.actual_cost/100*15, self.expected_cost/100*15, self))
        self.tasks.append(Task('implementation', self.actual_cost/100*15, self.expected_cost/100*15, self))
        self.tasks.append(Task('unit_test', self.actual_cost/100*10, self.expected_cost/100*10, self))
        self.tasks.append(Task('integration', self.actual_cost/100*15, self.expected_cost/100*15, self))
        self.tasks.append(Task('system_test', self.actual_cost/100*15, self.expected_cost/100*15, self))
        self.tasks.append(Task('deployment', self.actual_cost/100*15, self.expected_cost/100*15, self))
        self.tasks.append(Task('acceptance_test', self.actual_cost/100*15, self.expected_cost/100*15, self))

        self.is_on_time = True # Keeps track of whether this module is on time for the traffic light system
        self.deadline = None # The deadline (by date) of this module
        self.overall_task_progress = 0 # This is the amount of effort put into fully completed tasks
        self.progress = 0.0
        self.completed = False
        self.stalled = False
        self.hours_taken = 0 # This is productive time
        self.total_hours = 0 # number of hours from start of project including non productive hours. 

    # TODO: Consider changing tasks to be a dictionary for O(1) lookups
    # by name.
    # Doing a linear search through the list here will be slow and a dict
    # would be preferable.

    # Reason for list is so task have to be performed in order. 
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
        if self.progress >= (self.overall_task_progress + self.tasks[0].actual_cost):
            if current_time <= self.tasks[0].deadline:
                self.is_on_time = True
            self.overall_task_progress = self.progress
            self.completed_tasks.append(self.tasks[0])
            self.tasks.pop(0)

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

