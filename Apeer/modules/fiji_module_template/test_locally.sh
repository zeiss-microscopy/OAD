#!/bin/sh

# sh test_locally.sh executes the script
docker build --rm -t test/apeer_test_fijimodule:latest .
docker run -it --rm -v ${pwd}/input:/input -v ${pwd}/output:/output --env-file wfe.env test/apeer_test_fijimodule:latest
