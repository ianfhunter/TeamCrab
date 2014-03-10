

class Team(object):
    def __init__(self, name, salary, size):
        self.name = name
        self.salary = salary
        self.size = size
        self.module = None
        self.modules = list()
        self.completed_modules = list()

    def calc_progress(self):
        ''' Calculates the progress of the taks currently assigned to this team.
        Progress is 1 point per hour per person on the team -
        so each hour + size of team.

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
            self.module.progress += self.size

            if self.module.progress >= self.module.actual_cost:
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



