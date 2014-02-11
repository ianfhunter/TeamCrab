from engine.Project import Project
from engine.Culture import Culture
from engine.Location import Location
from engine.Module import Module
from engine.Team import Team

def load_test_game():
    project = Project('Sample Project', 'Agile', (12,3,2014))

    culture_a = Culture('Ireland', 0.8, 0.9)
    location_a = Location('Dublin', 0, culture_a, 20, 25)
    team_a = Team('', 0.8, 30, 10)
    location_a.add_team(team_a)

    project.locations.append(location_a)

    culture_b = Culture('America', 0.7, 0.7)
    location_b = Location('San Francisco', -8, culture_b, 30, 35)
    team_b = Team('', 0.7, 35, 25)
    location_b.add_team(team_b)

    project.locations.append(location_b)

    module = Module('Sample Module', 600)
    project.locations[0].teams[0].task = module.get_task('design')
    project.locations[1].teams[0].task = module.get_task('implementation')

    project.modules.append(module)

    return project
