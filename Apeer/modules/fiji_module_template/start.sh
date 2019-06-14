#!/bin/sh

# this script works inside the local docker container

# define script to be executed
SCRIPT=/Fiji.app/scripts/my_fijipyscript.py

# run the script in headless mode
/Fiji.app/ImageJ-linux64 --ij2 --headless --console --run $SCRIPT



