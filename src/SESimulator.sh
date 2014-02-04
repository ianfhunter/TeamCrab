#! /bin/sh
exec /opt/SESimulator/SESimulator.pyc "$@"

# This script is placed in /usr/local/bin when "make install" is run
# and is used to call SESimulator which is actually installed to /opt
# This is done to allow SESimulator access to all the necessary .pyc
# files which are apart of the application
