#!/bin/bash
# Update or run the tool/script that generates the log files
# Owner: Rohit Kumar; Date: 07/24/2018

# All paths should be absolute.


if [ -z "$1" ]
then
        echo "ERROR: No location provided. Command is ./run_main_tool.sh <path_to_tool>"
        exit 1
fi

echo "Starting build"
date
cd $1
echo $PWD

# Add here your call to the tool that generates the log files
#

if [ $? -ne 0 ] 
then
	echo "Build failed"
	exit 1
fi

echo " Log Script complete"
