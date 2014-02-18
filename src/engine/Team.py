import random


class Team(object):
    def __init__(self, name, efficiency, salary, size):
        self.name = name
        self.salary = salary
        self.efficiency = efficiency
        self.size = size
        self.task = None
        self.tasks = list()
        self.completed_tasks = list()

    def calc_progress(self, mod):
        ''' Calculates the progress of the taks currently assigned to this team.
        Expected_progress is 1 point per hour per person on the team -
        so each hour + size of team.

        Actual progress (Left name as just progress) -
        Affected by -
            Efficiency of team:
                - 1 is standard, no modifier.
                - Less than 1 is a poor team.
                - Greater than 1 is a good team.
            Cultural modifier:
                - 1 is standard, no modifier.
                - Less than 1 is a poor culture.
                - 1 is a good culture.
            Size of team:
                Basic advancement per hour
            Random element:
                + or - 0 to 25% of the progress made in that hour

        formula: team efficiency * cultural efficiency * team size + random element
        random element = +/- up to 25% of
            (team efficiency * cultural efficiency * team size)
        '''
        if self.task and self.task.completed and self.task not in self.completed_tasks:
            self.completed_tasks.append(self.task)

        if not self.task or self.task.completed:
            if self.tasks:
                self.task = self.tasks[0]
                self.tasks.pop(0)
            else:
                return

        tmp_prog = self.task.progress
        self.task.stalled = False
        if not self.task.completed:
            if self.task.module.tasks[0] == self.task:
                self.task.hours_taken += 1
                prog = self.efficiency * mod * self.size
                self.task.progress += prog + self.random_element(prog)

                if self.task.expected_progress < self.task.cost:
                    self.task.expected_progress += self.size
                if self.task.progress >= self.task.cost:
                    print self.name + '\'s task has completed!'
                    self.task.module.completed_tasks.append(self.task)
                    self.task.module.tasks.remove(self.task)
                    self.task.completed = True

        if tmp_prog >= self.task.progress:
            self.task.stalled = True

    def random_element(self, prog):
        ''' Generates a random value between -25 and 25 used as a percentage to offset prog.
        '''
        amount = float(random.randint(0, 25))
        direction = random.choice([-1, 1])
        return prog * (1 + (direction * amount / 100.0))
