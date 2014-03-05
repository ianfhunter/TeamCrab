from engine.Project import Project
from engine.Location import Location
from engine.Module import Module
from engine.Team import Team

class Scenario_Test_Game():
    def get_name(self):
        return "test_game"

    def load_game(self):
        project = Project('Sample Project', 'Agile', (12,3,2014))

        location_a = Location('Dublin', 0, "culture1", 20, 25, (375,148))
        team_a = Team('Team A', 1.0, 15, 10)

        location_a.add_team(team_a)

        project.locations.append(location_a)

        location_b = Location('Florida', -8, "culture2", 30, 5, (192,207))
        team_b = Team('Team B', 1.0, 20, 25)

        location_b.add_team(team_b)

        project.locations.append(location_b)

        location_c = Location('New Dehli', -11, "culture3", 30, 35, (570,264))
        team_c = Team('Team C', 1.0, 10, 5)

        location_c.add_team(team_c)

        project.locations.append(location_c)

        module1 = Module('Sample Module 1', 50)
        module2 = Module('Sample Module 2', 50)
        module3 = Module('Sample Module 3', 50)
        module4 = Module('Sample Module 4', 50)
        module5 = Module('Sample Module 5', 50)
        module6 = Module('Sample Module 6', 50)

        project.locations[0].teams[0].modules.append(module1)
        project.locations[1].teams[0].modules.append(module2)
        project.locations[2].teams[0].modules.append(module3)
        project.locations[0].teams[0].modules.append(module4)
        project.locations[1].teams[0].modules.append(module5)
        project.locations[2].teams[0].modules.append(module6)

        project.modules.append(module1)
        project.modules.append(module2)
        project.modules.append(module3)
        project.modules.append(module4)
        project.modules.append(module5)
        project.modules.append(module6)

        return project
