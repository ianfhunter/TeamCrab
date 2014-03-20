import os
from constants import constants

root_dir = os.path.join(os.path.dirname(__file__), '../')

config = {
        # Game parameters
        "ui_refresh_period_seconds" : 0.05,
        # How much a developer's effort is devided by for every productive work hour
        "developer_period_effort_value" : 2,
        # How many work hours a developer has in one work day 
        "developer_daily_effort" : 8,
        # Cost of a developer per day
        "developer_hourly_cost" : 100,
        # Adjustment to expected budget:
        "budget_mod" : 1.24,
        # Penalty to score if project goes over budget
        "cash_penalty" : 1.25,
        # Real-life seconds per game hour
        "game_speed" : 0.4,
        # Base likelihood value that a site will encounter a "problem" caused by the problem simulator
        # Used with global distance to adjust problem rates. 0.01 = 1%
        # Note: global distances influences the actual problem rate in conjunction with this rate
        "fail_rate" : 0.01,
        # UI colours
        "site_colour" : 0x2C8718,
        "bar_colour" : 0x9b9b9b,
        "background_colour" : 0xdedede,
        # File paths
        "root_dir" : root_dir,
        
        # If changing the images, keep the same image dimensions. vector images are not supported.
        #Start Screen:
        "start_background_path" : os.path.join(root_dir, "media/start_background.png"),
        "logo_path" : os.path.join(root_dir, "media/logo.png"),
        "bellerose_font" :os.path.join(root_dir, "media/Bellerose.ttf"),

        "map_path" : os.path.join(root_dir, "media/map.png"),
        "cancel_icon_path" : os.path.join(root_dir,"media/cancel.png"),
        "question_icon_path" : os.path.join(root_dir,"media/question.png"),
        "man_icon_path" : os.path.join(root_dir, "media/man.png"),
        "peep_icon_path" : os.path.join(root_dir, "media/people.png"),
        "clock_icon_path" : os.path.join(root_dir, "media/clock.png"),
        "location_icon_path" : os.path.join(root_dir, "media/location.png"),
        "target_icon_path" : os.path.join(root_dir, "media/target.png"),
        "green_button_path" : os.path.join(root_dir, "media/green_button.png"),
        "yellow_button_path" : os.path.join(root_dir, "media/yellow_button.png"),
        "red_button_path" : os.path.join(root_dir, "media/red_button.png"),
        "grey_button_path" : os.path.join(root_dir, "media/grey_button.png"),
}

config.update(constants)

cultures = {
    # Name : (honesty Mod, language (possibily expand to array), language_skill, east/west, context, national,organizational)
    "Irish" : (1, "English", "high", "west", "high", "Irish", "Innovative"),
    "American" : (1, "English", "high", "west", "high", "American", "Outcome"),
    "Indian" : (0, "English", "low", "east", "high", "Indian", "Outcome"),
    "Japanese" : (0, "Japanese", "high", "east", "low", "Japanese", "Innovative"),
    "Canadian" : (1, "English", "high", "west", "high", "Canadian", "People"),
    "Australian" : (1, "English", "high", "west", "high", "Australian", "People"),
    "Brazilian" : (1, "Protugise", "high", "west", "low", "Brazilian", "Detail"),
    "Belarusian" : (1, "Belarusian", "high", "east", "low", "Belarusian", "Outcome"),
}

global_distance = {
    "low" : 1,
    "medium_low" : 2,
    "medium_high" : 3,
    "high" : 4,
}
