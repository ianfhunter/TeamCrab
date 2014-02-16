import random

class Team(object):

    def __init__(self, name, efficiency, salary, size):
        self.name = name
        self.salary = salary
        self.efficiency = efficiency
        self.size = size
        self.task = None
        
     """ 
     expected_progress is 1 point per hour per person on the team - so each hour + size of team.

    Actual progress (Left name as just progress) - 
     Effected by -
        efficiency of team - 1 is standard - no modifier - less then 1 is a poor team, greater then 1 is a good team
        Cultural modifier - 1 is standard - no modifier  - less then 1 is a poor culture , greater then 1 is a good culture
        Size of team - basic advancement per hour
        random element - + or - 0 to 25% of the progress made in that hour

    formula - team efficiency * cultural efficiency * size of team + random element
    random element = +/-  up to 25% of (team efficiency * cultural efficiency * size of team)
    """

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
        