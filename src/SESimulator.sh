#!/bin/bash

v=RC1_rc3

if [[ $1 = "--simv" ]]; then
	v=$2
	shift 2
fi

exec python /opt/SESimulator_v$v/bin/SESimulator.pyc "$@"

# This script is placed in /usr/local/bin when "make install" is run
# and is used to call SESimulator which is actually installed to /opt
# This is done to allow SESimulator access to all the necessary .pyc
# files which are apart of the application
