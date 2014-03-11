import os
from constants import constants

root_dir = os.path.join(os.path.dirname(__file__), '../')

config = {
        # Game parameters
        "difficulty" : "normal",
        "sleep_duration" : 0.05,
        "developer_period_effort_value" : 1,
        "developer_daily_effort" : 4,
        "game_speed" : 0.4,
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
    # Name : (honesty Mod)
    "culture1" : (1.0),
    "culture2" : (1.0),
    "culture3" : (1.0),

}
