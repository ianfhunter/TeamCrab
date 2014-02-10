from Simulation_Engine import run_engine
from Project import Project
from Module import Module
from Task import Task
from Team import Team
from Location import Location
from Culture import Culture
from time import sleep

def main():
    project = Project('test_project', 'Agile', 0)    
    module = Module('test_module', 30)
    task = Task('test_task', 30)
    team = Team('test_team', 2, 0, 0)
    culture = Culture('test_culture', 1.5, 0)
    location = Location('test_location', 0, culture, 0, 0)
    module.tasks.append(task)
    team.task = task
    location.teams.append(team)
    project.locations.append(location)
    project.modules.append(module)
    
    run_engine(project)



if __name__ == "__main__":
    main()
