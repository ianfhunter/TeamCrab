from engine.Project import Project
from engine.Culture import Culture
from engine.Location import Location
from engine.Module import Module
from engine.Team import Team

def load_test_game():
    project = Project('Sample Project', 'Agile', (12,3,2014))

    culture_a = Culture('Ireland', 0.9, 1.0)
    location_a = Location('Dublin', 0, "culture1", 20, 25, (375,148))
    team_a = Team('Team A', 1.1, 30, 10)

    location_a.add_team(team_a)

    project.locations.append(location_a)

    culture_b = Culture('America', 1.25, 0.7)
    location_b = Location('San Francisco', -8, "culture2", 30, 5, (192,207))
    team_b = Team('Team B', 0.9, 35, 25)

    location_b.add_team(team_b)

    project.locations.append(location_b)

    culture_c = Culture('India', 0.75, 0.35)
    location_c = Location('New Dehli', -11, "culture3", 30, 35, (570,264))
    team_c = Team('Team C', 1.1, 15, 5)

    location_c.add_team(team_c)

    project.locations.append(location_c)

    module = Module('Sample Module', 600)
    project.locations[0].teams[0].tasks.append(module.get_task('design'))
    project.locations[1].teams[0].tasks.append(module.get_task('implementation'))
    project.locations[2].teams[0].tasks.append(module.get_task('unit_test'))
    project.locations[0].teams[0].tasks.append(module.get_task('integration'))
    project.locations[1].teams[0].tasks.append(module.get_task('system_test'))
    project.locations[2].teams[0].tasks.append(module.get_task('deployment'))
    project.locations[2].teams[0].tasks.append(module.get_task('acceptance_test'))

    project.modules.append(module)

    return project
