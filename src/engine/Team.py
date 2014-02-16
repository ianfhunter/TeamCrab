import random

class Team(object):

    def __init__(self, name, effiency, salary, size):
        self.name = name
        self.salary = salary
        self.efficiency = effiency
        self.size = size
        self.task = None

    def calc_progress(self, mod):
        if not self.task.completed:
		
            prog = self.efficiency * mod * self.size 
            self.task.progress += prog + self.random_element(prog)
			
            if self.task.expected_progress < self.task.cost:
                self.task.expected_progress += self.size 
            if self.task.progress >= self.task.cost:
                print self.name + '\'s task has completed!'
                self.task.module.completed_tasks.append(self.task)
                self.task.module.tasks.remove(self.task)
                self.task.completed = True
				
    def random_element(self, prog):
        amount = random.randint(0, 25)
        direction = random.choice([-1, 1])
        return direction * prog / 100 * amount
        