Software Engineering Simulator
======

## Group Project for CS4098 - Team Crab

In which you are a production manager in charge of various global software teams and you must try to complete your product with maximal cost efficiency.

![Build Status](https://magnum.travis-ci.com/ianfhunter/TeamCrab.png?token=XVnqqNujPPiH7bQNyxKk&branch=master)

## Requirements:
The project uses python 2.7 to run. The following packages are required and can be installed via apt:
* python-pygame
* python-nose
* python-pip

The following can be installed using pip:
* pgu

While it is not required for running the game, installing "timidity" through apt will remove the "No sound card" message 
that some players receive at the start of the game.

## Building, installing and everything in-between

The Makefile in the root of the project provides all functionality for building, testing and installing the project.
The file provides the following targets:

* build
* test
* clean
* install
* uninstall
* uninstall-script
* run
* docs

The build target compiles each of the .py source files in the src directory into corresponding .pyc files in the bin 
directory (it will create the bin directory first if it does not already exist). The built project can then be run locally
via the command "make run".

The test target will build the project as outlined above and then perform the unit tests which are in the test directory.
At the moment there are no tests since the project is only at a zero velocity release, so this target will perform the
same function as build for the time being.

The clean target deletes all the files in the bin directory.

The install target will first build the project (using the build target). It will then copy all the .pyc files in the 
bin directory into /opt/SESimulator_$(version). The inclusion of the version in the directory will allow for multiple
versions of the game to be installed alongside one another. So, for example release RC1_rc3 of the game will install
to the directory /opt/SESimulator\_RC1\_rc3/. Next, the script SESimulator.sh in the src directory will be copied into
/usr/local/bin/ so that users on the machine can start the simulator simply by using the command "SESimulator". Root
access is required to add files to opt/ and /usr/local/bin.

Once the game has been installed, it can be run using the command "SESimulator" as mentioned above. This command
can take an optional argument "--simv version" to specify which version of the game should be run (if there are
multiple versions installed). If this flag is not specified then the script will load the newest version of the
game to be installed.

The uninstall target simply removes all SESimulator files from /opt. It will only uninstall
the version of the game that this source tree contains.

The uninstall-script target will delete the run script in /usr/local/bin. It is assumed that make uninstall
has been run for all installed versions of the game, since this target will not remove any game files from
/opt.

The run target will simply call "python bin/SESimulator.pyc" in the local directory. It can be used for quickly
running a local build.

Finally, the docs target will generate pydocs for the all source files in the src directory and place them
into the docs directory.

### How to install in a different directory
As mentioned above, the game will install by default in /opt and /usr/local/bin. This can be changed by passing
two different variables to make install. As an example, if you wanted to install the game so that the run script
is in /bin and the game files to be in /bin/SE_sim then you could run:

make install install_pyc_prefix=/bin/SE_sim install_sh_prefix=/bin

Here the install_pyc_prefix value is the directory into which the SESimulator_$(version) directory containing all the game
pyc files will be placed. The install_sh_prefix value is the directory into which the SESimulator script will be placed.
Multiple versions of the game can be installed in this way. The --simv flag mentioned above can be used to access different
versions of the game installed into the same directory.

## Writing unit tests
The following is a simple example of the form a unit test should take in the test directory

```python
import importme
import unittest

class TestEngine(unittest.TestCase):

    def setUp(self):
        pass

    def test_method(self):
        pass

if __name__ == '__main__':
    unittest.main()
```

Each test directory contains an importme.py file. This must be imported at the start of each unit test. This allows
the test to see the modules contained in the bin directory at the root of the project.

Each file must contain a class which inherits from unittest.TestCase as shown. This provides a whole bunch of features
provided by the Python unittest framework. The setUp function must be provided to initialize any values required by each
test in this class. Every method that is a unittest must begin with "test_"

## Writing default scenarios
All default scenarios are in the src/games directory. New scenarios can be written by creating a new .py file in this
directory with the following structure:

```python
from engine.Project import Project
from engine.Location import Location
from engine.Module import Module
from engine.Team import Team

def get_name():
    return "x sites - scenario name"

def load_game():
    ''' Place a description of the scenario here
    '''
    pass
```

The string returned by the get_name function is displayed in the UI for user selection. The load_game function should return
an instance of the Project class containing all necessary information for the game to run (e.g. Modules, Teams, Locations).
If necessary, please check one of the existing scenarios to see how this is done.

Once this is done, the new scenario must be imported into src/games/scenarios.py and an instance of the new scenario must
be appended to the scenarios list in the get_scenarios function. Once this has been done, the new scenario should be visible
in the game (after a rebuild).

## Documentation
Documentation is generated by Pydoc. 
```python
def function():
    """Documentation Comment"""
    Code
```
to generate html documentation use
``` pydoc -w Module.file ```


## Inspection of Features
1. Feature #17 - Master configuration file
  * The master configuration file is in the form of a Python file which is interpreted by the game, kept in global_config.py.
  * It contains a dictionary of key/value pairs for configuration values.
  * To modify this file, you must modify the version in bin/global_config.py if running straight from the project repository/tarfile.
  * After the simulator has been installed, you must modify global_config.py in the install path in order to see changes reflected.
  * An obvious value to change is bar_colour: change this to ffffff to see a white bar at the bottom of the screen instead of grey.
2. Feature #9 - Process simulator
  * Simply start the game with the sample game file (this happens automatically at the moment).
  * Output from the process simulator will automatically be displayed in the console every game hour as each task progresses
  * This output is of the form:
    "Module: Front end - Current Effort Expended: x ph - Expected Total Effort: y ph - Actual Total Effort: x ph (ph = person-hours)"
        where x, y and z are numerical values in Person Hours.
        Current Effort Expended = the amount of actual effort in person hrs that a team has expended so far.
        Expected Total Effort = the amount of actual effort estimated for this module to be completed.
        Actual Total Effort = the actual amount of effort that will be required to complete this module, given the +-25% variance.
  * The time at GMT is also printed on each turn, it is shown as a 24 hour clock in the form "[hours, minutes]".
3. Feature #6 - Status display
  * Once the program is launched with a selected senario, the status screen is shown.
  * Green represents sites that are progressing at a rate that is satisfactory (not under 75% of estimated progress)
  * Yellow represents sites that have been delayed, This state occurs when a problem has been generated and has set progress of a team back significantly. These delays can be mitigated by interventions
  * Red represents sites that have been stalled and need an intervention to progress any further. This state occurs as part of a critical failure generated by a problem such as flooding of a datacenter. To resolve this an intervention MUST be made, or no progress will be made.
  * Grey represents sites that are inactive - waiting on a dependency or completed. They are not supposed to be doing anything.
  * Changes between colours indicate a change in status information in line with the above statuses.
  * Sites are clickable to view more detailed information about a site.
  * Clicking the ? in the top-right shows detailed information about what the colours of sites mean
4. Feature #20 - Default scenarios
  * To choose a provided scenario, launch the game and select one from the dropdown list.
  * If no scenario is selected, the default scenario is the first item in the dropdown list.
5. Feature #14 - End of game report 
  * Start the game with the sample game file (this happens automatically at the moment).
  * Wait until the end of the game.
  * A summary of the report will be displayed on the screen, with the full report written to report.json in the game's working directory (the same directory as SESimulator.py)
6. Feature #5 - Nominal schedule calculator
   * The nominal deadline is the sum of all the efforts estimated for each module, divided by a default developer-period effort value.
   * This figure is calculated at the start of the game and can be seen in the bottom bar of the main game screen
   * Each scenario has its own nominal deadline
7. Feature #3 - Game score calc. 
  * Play a game through until the end-game screen.
  * Your game score is shown.
  * Game score is calculated by "score = remaining_budget + [(6 - number_of_months_behind_schedule) * (yearly_revenue / 12)]".
8. Feature #8 - Module Completion calc.
  * This is currently not implemented as specified. 
  * Instead of taking the base and modifying the required amount by up to +/- 25%, the amount of work done by a team is modified by up to +/- 25% each hour worked. 
  * This is so it can be seen when a module is falling behind schedule.
  * This can be seen in the trace - Actual Progress - how much work a team has actually done on the module - compared to Expected Progress - how much work a team should have done with no random element.
9. Feature #11 - Problem Simulator
  * If a problem occurs, the site at which it occurs will be reported in the trace, as well as the nature of the problem. e.g. Problem occured at Belarus Problem: Module failed to deploy properly
10. Feature #7 - Inquiry Interface
  * TODO

## Game console trace
When running the game, information related to the current progress of modules is displayed in the console.
The game time is printed to the console every turn. A turn equates to an hour of work in the game. The time
displayed takes the form "1-1-2014 8:00 GMT" for example.

The progress of each module currently being worked on is printed every turn that the assigned team is
"working". Teams are considered to be working from 9:00 to 17:00 local time. An example of the output
of the progress of a module is:

"Module: Sample Module - Current Effort Expended: 60.0 ph - Expected Total Effort: 800 ph - Actual Total Effort: 968.0 ph (ph = person-hours)"

First the name of the module is printed. After this, there are 3 values related to the progress of the
module.
Current Effort Expended is the amount of actual effort in person hrs that a team has expended so far.
Expected Total Effort is the amount of actual effort in person hrs estimated for this module to be completed.
Actual Total Effort is the actual amount of effort in person hrs that will be required to complete this module, given the +-25% variance.

When a module is completed, a message will be printed to the console. For example, "Team C's module has
completed".

When a team has no module assigned during a working hour and are sitting idle, a warning will be printed
to the console. For example, "Warning: Team Team B has no module assigned".

##Attributions:
* Map Image - http://dezignus.com/vector-world-map/#more-912
* Man Icon - Man by Tamiko Young from The Noun Project http://thenounproject.com/term/man/12173/
* Gear Icon - Gear by Reed Enger from The Noun Project
* Clock Icon - Clock by Nicholas Burroughs from The Noun Project
* Target Icon - Target by Laurent Patain from The Noun Project 
* Location Icon - Designed by Vladimir Dubinin from the Noun Project
* People Icon - Designed by Sagiev Farid from the Noun Project
* Question Icon - Designed by Mateo Zlatar from the Noun Project
