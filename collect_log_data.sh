#!/bin/bash
# Collects essential data from the logs generated after the run_main_tool.sh runs and completes
# Owner: Rohit Kumar, date: 07/24/2018

# This script runs over the .txt and/or any files of your interest
# The input to this script is the location of the log files. This input should be an absolute path.
# NOTE: This script may require another python scripts, analysis_log_data.py to be present in the same directory as 
# this script

folder_name=$(date +'data_collected_%Y%m%d_%H%M%S')
#folder_name='debugging_data_logs'

path_loc=$1

if [ -z "$path_loc" ]
then
        echo "ERROR: Provide location to the log files. Command format is ./collect_log_data.sh <absolute_path_of_log_dir>"
        exit 1
fi

mkdir -p $folder_name
if [ $? -ne 0 ]
then
        echo "ERROR: Cannot create folder to store collected log data "
        exit 1
fi

echo 'Collecting data from: ' $path_loc

echo "Finding all first type of data and recording in: first_data.txt"
#find $path_loc -type f -exec grep -i "First_data_keyword" --include=\*{.h,.txt} {} \; -print > first_data.txt
find $path_loc -name '*.txt' -exec grep -A 2 "First_keyword \|Second_keyword \|Third_ketword \|Fourth_Keyword" --include=\*{.h,.txt} {} \; -print > $folder_name/first_data.txt
if [ $? -ne 0 ]
then
        echo "ERROR: Command failed for finding first type of data "
        exit 1
fi

cd $folder_name
OUTPUT=$(grep "${path_loc}" 'first_data.txt' | wc -l)
echo '---Number of Found data lines = ' $OUTPUT
cd ..

echo "Logging second type of data and recording in: second_data.txt"
#find $path_loc -name '*.txt' -exec sed -e '/first_keyword /!d' -e '/second_keyword/!d' {} \; -print > second_data.txt
find $path_loc -name '*.txt' -exec grep -E 'first_keyword.*second_keyword|first_keyword.*third_keyword' {} \; -print > $folder_name/second_data.txt
if [ $? -ne 0 ]
then
        echo "ERROR: Command failed for finding second data "
        exit 1
fi


echo "Extracting elements of interest and recording in: third_data.txt "
python analysis_log_data.py $folder_name $path_loc
if [ $? -ne 0 ]
then
        echo "ERROR: Python command for extracting data of interest failed  "
        exit 1
fi

echo 'Collecting all data of interest complete, files present in ' $folder_name

