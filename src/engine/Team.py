from global_config import config


class Team(object):
    '''
    This class represents a team of employees who can work on modules as part of a project.
    '''
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.module = None
        self.modules = list()
        self.completed_modules = list()

    def calc_progress(self, current_time):
        '''
        Calculates the progress of the taks currently assigned to this team.
        Progress is 1 point per hour per person on the team -
        so each hour + size of team.
        '''
        if not self.module or self.module.completed:
            if len(self.modules) > 0 :
                self.module = self.modules[0]
                self.modules.pop(0)
            else:
                return

        tmp_prog = self.module.progress
        self.module.stalled = False
        if not self.module.completed:
            self.module.hours_taken += 1
            self.module.progress_module(self.size/config["developer_period_effort_value"], current_time)

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
