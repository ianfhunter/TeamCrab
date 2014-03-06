import random


class Team(object):
    def __init__(self, name, efficiency, salary, size):
        self.name = name
        self.salary = salary
        self.efficiency = efficiency
        self.size = size
        self.module = None
        self.modules = list()
        self.completed_modules = list()

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
        

        if not self.module or self.module.completed:
            if len(self.modules) > 0 :
                self.module = self.modules[0]
                self.modules.pop(0)
            else:
                return
        self.module.hours_taken += 1

        tmp_prog = self.module.progress
        self.module.stalled = False
        if not self.module.completed:
            self.module.hours_taken += 1
            prog = self.efficiency * mod * self.size
            self.module.progress += self.random_element(prog)


            self.module.expected_progress += self.size
            if self.module.progress >= self.module.cost:
                print self.name + '\'s module has completed!'
                self.module.completed = True
                self.completed_modules.append(self.module)
                # Allocate a new module
                if self.modules:
                    self.module = self.modules[0]
                    self.modules.pop(0)
                else:
                    self.module = None

        if self.module and tmp_prog >= self.module.progress:
            pass
#            self.task.stalled = True


    def random_element(self, prog):
        ''' Generates a random value between -25 and 25 used as a percentage to offset prog.
        '''
        amount = float(random.randint(0, 25))
        direction = random.choice([-1, 1])
        return prog * (1 + (direction * amount / 100.0))
