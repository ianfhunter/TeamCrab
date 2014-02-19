import os

root_dir = os.path.join(os.path.dirname(__file__), '../')

config = {
        # Game parameters
        "difficulty" : "normal",
        "sleep_duration" : 0.05,
        # UI layout parameters
        "reaction_timeout" : 120,
        "screenX" : 850,
        "screenY" : 480,
        "menuX" : 780,
        "menuY" : 460,
        "bottom_bar_height" : 20,
        # UI colours
        "site_colour" : 0x2C8718,
        "bar_colour" : 0x9b9b9b,
        "background_colour" : 0xdedede,
        # File paths
        "root_dir" : root_dir,
        "map_path" : os.path.join(root_dir, "media/map.png"),
        "man_icon_path" : os.path.join(root_dir, "media/man.png"),
        "cog_icon_path" : os.path.join(root_dir, "media/cog.png"),
        "clock_icon_path" : os.path.join(root_dir, "media/clock.png"),
        "location_icon_path" : os.path.join(root_dir, "media/location.png"),
        "target_icon_path" : os.path.join(root_dir, "media/target.png"),
        "green_button_path" : os.path.join(root_dir, "media/green_button.png"),
        "yellow_button_path" : os.path.join(root_dir, "media/yellow_button.png"),
        "red_button_path" : os.path.join(root_dir, "media/red_button.png"),
        "grey_button_path" : os.path.join(root_dir, "media/grey_button.png"),
}

cultures = {
    # Name : (Effiency mod, honesty Mod)
    "culture1" : (1.0, 1.0),
    "culture2" : (1.25, 1.0),
    "culture3" : (0.75, 1.0),

}
