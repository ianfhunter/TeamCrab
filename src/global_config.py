import os
from constants import constants

root_dir = os.path.join(os.path.dirname(__file__), '../')

config = {
        # Game parameters
        "difficulty" : "normal",
        "ui_refresh_period_seconds" : 0.05,
        "developer_period_effort_value" : 1,
        "developer_daily_effort" : 4,
        "game_speed" : 0.1,
        "fail_rate" : 0.2,
        # UI colours
        "site_colour" : 0x2C8718,
        "bar_colour" : 0x9b9b9b,
        "background_colour" : 0xdedede,
        # File paths
        "root_dir" : root_dir,

        #if changing the icons, keep the same image dimensions. vector images are not supported.
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
    # Name : (honesty Mod, language(possiably expand to array), language_skill, east/west, context, national,organizational )
    "Irish" : (1, "English", "high", "west", "high", "Irish", "Innovative"),
    "American" : (1, "English", "high", "west", "high", "American", "Outcome"),
    "Indian" : (0, "English", "low", "east", "high", "Indian", "Outcome"),
    "Japanese" : (0, "Japanese", "high", "east", "low", "Japanese", "Innovative"),
    "Canadian" : (1, "English", "high", "west", "high", "Canadian", "People"),
    "Australian" : (1, "English", "high", "west", "high", "Australian", "People"),
    "Brazilian" : (1, "Protugise", "high", "west", "low", "Brazilian", "Detail"),
    "Belarusian" : (1, "Belarusian", "high", "east", "low", "Belarusian", "Outcome"),

}

problems = {
    #description,delay
    1: ("a site falls behind more than 25% on a task", .50),
    2: ("module fails to integrate properly", .85),
    3: ("module fails system tests", .60),
    4: ("module or product fails acceptance tests (fails to meet real requirements)", 1.00),
    5: ("module fails to deploy correctly", .45),
}
