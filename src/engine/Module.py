import random
from Task import Task
import datetime

def calculate_actual_cost(expected_cost):
    ''' Returns the actual cost of a module based on a random variation between 75% and 125%.
    '''
    amount = float(random.randint(-25, 25))
    return expected_cost * (1 + (amount / 100.0))

class Module(object):
    def __init__(self, name, cost):
        self.name = name
        self.expected_cost = cost
        self.actual_cost = calculate_actual_cost(cost)
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
        self.problems_occured = list() # A list of all problems that have occured for this module

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

        # If the current task has reached its deadline then the module is not on time
        if self.tasks:
            if current_time >= self.tasks[0].deadline:
                self.is_on_time = False
        
        expected_completion = float(self.progress) / self.expected_cost
        actual_completion = float(self.progress) / self.actual_cost
        if actual_completion + 0.25 < expected_completion:
            # Add 50% to the "estimated time"
            self.expected_cost *= 1.5
            for task in self.completed_tasks + self.tasks:
                task.expected_cost *= 1.5

            self.calc_deadline(self.start_date, self.assigned_team_size)
            self.problems_occured.append('Problem: Fallen behind more than 25% on a task')

    def calc_deadline(self, start_date, team_size):
        ''' Calculates the deadline for this module and stores it in self.deadline
        This also sets the deadlines for all tasks in this module
        '''
        self.start_date = start_date
        self.assigned_team_size = team_size
        work_hours_total = 0
        for task in self.completed_tasks + self.tasks:
            work_hours_total += task.expected_cost/team_size
            task.deadline = start_date + datetime.timedelta(days=work_hours_total/8, hours=work_hours_total%8)
        self.deadline = self.tasks[-1].deadline

    def wall_clock_time(self):
        return self.total_hours

    def productive_time_on_task(self):
        return self.hours_taken

    def add_problem(self):
        if self.tasks:
            if self.tasks[0].name == 'integration':
                # Add unit_tests and implementation back onto the tasks list
                self.tasks.insert(0, self.completed_tasks.pop())
                self.tasks.insert(0, self.completed_tasks.pop())

                # Update the actual cost of this module and all tasks
                self.actual_cost = int(self.actual_cost * 1.85)
                for i in range(6):
                    self.tasks[i].actual_cost = int(self.actual_cost/100.0*15.0)
                self.tasks[1].actual_cost = int(self.actual_cost/100.0*10.0) # Unit tests

                self.problems_occured.append('Module failed to integrate properly')
                return 'Module failed to integrate properly'

            elif self.tasks[0].name == 'system_test':
                # Add integration back onto the tasks list
                self.tasks.insert(0, self.completed_tasks.pop())

                # Update the actual cost of this module and all tasks
                self.actual_cost = int(self.actual_cost * 1.6)
                for i in range(4):
                    self.tasks[i].actual_cost = int(self.actual_cost/100.0*15.0)

                self.problems_occured.append('Module failed system tests')
                return 'Module failed system tests'

            elif self.tasks[0].name == 'acceptance_test':
                # Add all tasks back onto the tasks list
                for i in range(6):
                    self.tasks.insert(0, self.completed_tasks.pop())

                # Update the actual cost of this module and all tasks
                self.actual_cost = int(self.actual_cost * 2)
                for i in range(6):
                    self.tasks[i].actual_cost = int(self.actual_cost/100.0*15.0)
                self.tasks[2].actual_cost = int(self.actual_cost/100.0*10.0) # Unit tests

                self.problems_occured.append('Module failed acceptance tests')
                return 'Module failed acceptance tests'

            elif self.tasks[0].name == 'deployment':
                # Add system tests back onto the tasks list
                self.tasks.insert(0, self.completed_tasks.pop())

                # Update the actual cost of this module and all tasks
                self.actual_cost = int(self.actual_cost * 1.45)
                for i in range(3):
                    self.tasks[i].actual_cost = int(self.actual_cost/100.0*15.0)

                self.problems_occured.append('Module failed to deploy properly')
                return 'Module failed to deploy properly'
        return None
