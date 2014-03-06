from engine.Project import Project
from engine.Location import Location
from engine.Module import Module
from engine.Team import Team
from engine.RevenueTier import LowRevenueTier

def get_name():
    return "2 sites - Small webapp development"

def load_game():
    ''' Project is a small web app consisting of 5 modules:
    Framework, database, front end, api, documentation. 

    '''
    project = Project('Web App', 'Agile', 100000, LowRevenueTier())

    # Setup a team in Dublin
    dublin = Location('Dublin', 0, "culture1", 30, 25, (375,148))
    dublin_team = Team('Dublin Team 1', 1.0, 35, 20)
    dublin_team2 = Team('Dublin Team 1', 1.0, 35, 10)
    dublin.add_team(dublin_team)
    dublin.add_team(dublin_team2)
    project.locations.append(dublin)

    # Setup a team in Poland
    poland = Location('Poland', 0, "culture2", 15, 20, (425,148))
    poland_team = Team('Poland Team', 1.0, 30, 15)
    poland.add_team(poland_team)
    project.locations.append(poland)

    # Create modules and assign tasks to appropriate teams
    frame = Module('Framework', 600)
    project.modules.append(frame)
    data = Module('Database', 400)
    project.modules.append(data)
    front = Module('Front end', 800)
    project.modules.append(front)
    api = Module('API', 200)
    project.modules.append(api)
    doc = Module('Documenation', 100)
    project.modules.append(doc)

    project.locations[0].teams[0].modules.append(front)
    project.locations[0].teams[1].modules.append(data)
    project.locations[0].teams[1].modules.append(doc)
    project.locations[1].teams[0].modules.append(frame)
    project.locations[1].teams[0].modules.append(api)

    return project
