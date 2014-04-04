Software Engineering Simulator
======

## Group Project for CS4098 - Team Crab

In which you are a production manager in charge of various global software teams and you must try to complete your product with maximal cost efficiency.

![Master Branch Build Status](https://magnum.travis-ci.com/ianfhunter/TeamCrab.png?token=XVnqqNujPPiH7bQNyxKk&branch=master)

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
All tests are contained within the test/ directory and any items that cannot be tested have been listed in NOT_TESTED.csv and have corresponding reasons for their exclusion.

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

Here the install_pyc_prefix value is the directory into which the SESimulator_$(version) directory containing all the game pyc files will be placed. The install_sh_prefix value is the directory into which the SESimulator script will be placed.
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
All default scenarios are in the games directory in the root of the repository. New scenarios can be written by creating
a new .json file. The file should contain a single JSON object representing the project as a whole. The format for the 
file is as follows:
```json
{
	"Name" : "Name of your project",
	"Budget" : 123456,
	"Revenue Tier" : "Low, Medium or High",
	"Home location" : "Dublin",
	"Locations" : [
		{
			"Name" : "Dublin",
			"Culture" : "Irish",
			"Capacity" : 30
		}
	],
	"Teams" : [
		{
			"Name" : "Dublin Team",
			"Size" : 20,
			"Location" : "Dublin"
		}
	],
	"Modules" : [
		{
			"Name" : "Module Name",
			"Cost" : 1000,
			"Assigned Team" : "Dublin Team"
		}
	]
}

```
The three arrays for Locations, Teams and Modules each contain comma separated object of the appropriate kind of object.
So for example, to add more Locations to the example above a user can simple add in a new object containing the Name,
Culture and Capacity fields.

It is important to note that the Location field in each Team object must match the name of a Location exactly. The same
can be said about the Assigned Team field in Module objects.

Once a new scenario has been created, it should be available in game immediately.

## Documentation
Documentation is generated by Pydoc. 
```python
def function():
    """Documentation Comment"""
    Code
```
to generate html documentation use
``` pydoc -w Module.file ``` or the provided 'make docs' command


## Inspection of Features
1. Feature #17 - Master configuration file
  * The master configuration file is in the form of a Python file which is interpreted by the game, kept in global_config.py.
  * It contains a dictionary of key/value pairs for configuration values.
  * To modify this file, you must modify the version in bin/global_config.py if running straight from the project repository/tarfile.
  * After the simulator has been installed, you must modify global_config.py in the install path in order to see changes reflected.
  * An obvious value to change is bar_colour: change this to ffffff to see a white bar at the bottom of the screen instead of grey.
  * We were asked to have both of the following to be configurable in the master config:
    - average cost of a developer-day across all sites
    - cost of developer-day at each site
  * However, since one is dependent on the other we chose to make the average configurable and then calculate site vaule as a simple function of the average.
  * Each configurable parameter has corressponding comments above it to aid any user changes

2. Feature #9 - Process simulator
  * Simply start the game with a chosen scenario from the start screen .
  * Output from the process simulator will automatically be displayed in the console every game hour as each task progresses
  * This output is of the form:
    "Module: Front end (Module Location) - Current Effort Expended: x ph - Expected Total Effort: y ph - Actual Total Effort: x ph (ph = person-hours)"
        where x, y and z are numerical values in Person Hours.
        Current Effort Expended = the amount of actual effort in person hrs that a team has expended so far.
        Expected Total Effort = the amount of actual effort estimated for this module to be completed.
        Actual Total Effort = the actual amount of effort that will be required to complete this module, given the +-25% variance.
  * The time at GMT is also printed on each turn, it is shown as a 24 hour clock in the form "d-m-y h:mm GMT".
  * IMPORTANT NOTE: If a site's "Actual Total Effort" exceeds 125% of its "Expected Total Effort", this is because a PROBLEM has occurred at that site.
    * This is caused by the problem simulator feature - since a problem has occurred, the site's Actual Total Effort (the total effort necessary to complete this module) is increased and therefore can be outside the initial range of 75% - 125% of the estimate.
    * Further information about the game trace can be seen below. 
3. Feature #6 - Status display
  * Once the program is launched with a selected senario, the status screen is shown.
  * Green represents sites that are progressing at a rate that is satisfactory (not under 75% of estimated progress)
  * Yellow represents sites that have been delayed, This state occurs when a problem has been generated and has set progress of a team back significantly. These delays can be mitigated by interventions
  * Red represents sites that have been stalled and need an intervention to progress any further. This state occurs as part of a critical failure generated by a problem such as flooding of a datacenter. To resolve this an intervention MUST be made, or no progress will be made.
  * Grey represents sites that are inactive - waiting on a dependency or completed. They are not supposed to be doing anything.
  * Changes between colours indicate a change in status information in line with the above statuses.
  * Sites are clickable to view more detailed information about a site.
  * Clicking the ? in the top-right shows detailed information about what the colours of sites mean. you can close the window with the X in the top right corner.
4. Feature #20 - Default scenarios
  * To choose a provided scenario, launch the game and select one from the dropdown list.
  * To inspect a chosen scenario, press the Details button to see information about the sites, modules and more.
  * To start the game press the Select button
  * If no scenario is selected, the default scenario is the first item in the dropdown list.
5. Feature #14 - End of game report 
  * Start the game with any chosen game file.
  * Wait until the end of the game.
  * A summary of the report will be displayed on the screen, with the full report written to report.txt in the game's working directory (the same directory as SESimulator.py)
6. Feature #5 - Nominal schedule calculator
   * The nominal deadline is the sum of all the efforts estimated for each module, divided by a default developer-period effort value.
   * This figure is calculated at the start of the game and can be seen in the bottom bar of the main game screen. It can also be seen in the end game summary so a user can compare their own time to it
   * Each scenario has its own nominal deadline
7. Feature #3 - Game score calc. 
  * Play a game through until the end-game screen.
  * Your game score is shown.
  * Game score is calculated by "score = remaining_budget + [(6 - number_of_months_behind_schedule) * (yearly_revenue / 12)]".
8. Feature #8 - Module Completion calc.
  * When a module is set up, its base cost is taken and modified by up to +/-25% of its base cost.
  * This is shown in the game trace as the variation between Expected Total Cost and Actual Total Cost.
  * It is also shown in the end game screen with Estimated Cost and Actual Cost.
  * NOTE: the Problem Simulator can further modify the Actual Cost resulting in a varation of greater then 25%
9. Feature #11 - Problem Simulator
  * Start the game with one of the sample scenarios.
  * By its nature, this feature is difficult to inspect since it runs in the background as part of the game engine.
  * If a problem occurs, the site at which it occurs will be reported in the console trace, as well as the nature 
    of the problem. e.g. Problem occured at Belarus Problem: Module failed to deploy properly
  * Depending on the nature of the problem, the Actual Cost of the module will be increased by the appropriate amount. 
10. Feature #7 - Inquiry Interface
  * To open the inquiry interface, click the 'inquiries' button in the bottom right corner.
  * Select a site to give inquiries to by clicking on the text links
  * Choose a type of inquiry to issue and select corresponding button. Each inquiry will hold up developers at a site for the displayed amount of time
  * Results of the inquiry for each team at the site are shown in the text box below the buttons.
  * There are 5 different types of inquiry
     1.  Ask sites if they are on schedule or not. Dishonest sites will always report that they are on schedule
     2.  Ask sites the status of their assigned modules. Dishonest sites report list of modules with 'on schedule' for all; others report actual status
     3.  Ask sites for a list of their completed tasks - All sites report actual tasks completed, but not status of other tasks (in progress or late)
     4.  A video conference - All sites report actual tasks completed; Asian & Russian sites report other tasks with 50% accuracy
     5.  Visit the site - All sites provide accurate list of completed, on-schedule, and late tasks

11. Feature #37 - Time Penalty
  * Make time penalty 50% of original cost

12. Feature #36 - Detailed site visit report
  * Problems in the Inquiry Interface now list their Module & Task on which they have occurred.

13. Feature #39 - Daily variation
  * Each site's productivity varies hourly as specified by a master parameter.

14. feature #16 - Intervention interface
  * similar setup to the inquiry interface. Open a window by selecting the desired site and clicking the intervene button.
  * Interventions have costs associated with them on four tiers - High, Med High, Med Low & Low
  * They also have similar levels of impact. The levels of impact apply a modifier of (impact/1-impact) to the problem rate at a site.
  * Excluded interventions:
    1. 'Adopt Follow The Sun Development' as Follow the Sun Development was not an assigned feature
    2. 'Relocate to Adjacent Time Zone' as we agreed in the meeting that moving staff around was out of scope because of the additional time pressures

15. feature #38 - Scenarios from JSON
  * TODO

16. Feature #35 - Optimistic budget calculation 
  * TODO



## Game console trace
When running the game, information related to the current progress of modules is displayed in the console.
The game time is printed to the console every turn. A turn equates to an hour of work in the game. The time
displayed takes the form "1-1-2014 8:00 GMT" for example.

The progress of each module currently being worked on is printed every turn that the assigned team is
"working". Teams are considered to be working from 9:00 to 17:00 local time. An example of the output
of the progress of a module is:

"Module: Sample Module ( Module Location ) - Current Effort Expended: 60.0 ph - Expected Total Effort: 800 ph - Actual Total Effort: 968.0 ph (ph = person-hours)"

First the name of the module is printed. After this, there are 3 values related to the progress of the
module.
Current Effort Expended is the amount of actual effort in person hrs that a team has expended so far.
Expected Total Effort is the amount of actual effort in person hrs estimated for this module to be completed.
Actual Total Effort is the actual amount of effort in person hrs that will be required to complete this module, given the +-25% variance.

When a module is completed, a message will be printed to the console. For example, "Team C's module has
completed".

When a team has no module assigned during a working hour and are sitting idle, a warning will be printed
to the console. For example, "Warning: Team Team B has no module assigned".
 
IMPORTANT NOTE: If a site's "Actual Total Effort" exceeds 125% of its "Expected Total Effort", this is because a PROBLEM has occurred at that site.
This is caused by the problem simulator feature and is not an error in game logic.

## Untested functions

Functions and classes that are untested for legitimate reasons (calls to external libraries, UI drawing functions, for example) are marked with the @untestable attribute in their documentation string. An example of this would be:

```
'''
Foos the Bar `bar'.

@untestable - just a call to external library baz.
'''
def foo_bar(bar):
    return baz(bar)
```

## Attributions:
* Map Image - http://dezignus.com/vector-world-map/#more-912
* Man Icon - Man by Tamiko Young from The Noun Project http://thenounproject.com/term/man/12173/
* Gear Icon - Gear by Reed Enger from The Noun Project
* Clock Icon - Clock by Nicholas Burroughs from The Noun Project
* Target Icon - Target by Laurent Patain from The Noun Project 
* Location Icon - Designed by Vladimir Dubinin from the Noun Project
* People Icon - Designed by Sagiev Farid from the Noun Project
* Question Icon - Designed by Mateo Zlatar from the Noun Project
* Coloured Buttons modifed from the existing PGU buttons by Ian
* Retro Sunbeams - http://www.vectorportal.com/subcategory/166/RETRO-SUN-RAYS-VECTORS.eps/ifile/11646/detailtest.asp
* Bellerose Font - James M. Harris http://www.dafont.com/bellerose.font
* Any icons not mentioned were either in the public domain or designed by a member of the team
