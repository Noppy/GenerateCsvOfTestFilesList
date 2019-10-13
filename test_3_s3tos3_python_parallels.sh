#!/bin/bash

# Configuration
ListNumOfParallels="100 200 400 800 1000 1500 2000"
ListNumOfParallels="10"
SummaryResultCSVFile=test_3_results_summary.csv
ExecCommand=./test_3_s3tos3_python_parallels_subcommand.sh

#------------------------
# Main
#------------------------

cp /dev/null ${SummaryResultCSVFile}

for parallel in ${ListNumOfParallels}
do
    ${ExecCommand} ${parallel} ${SummaryResultCSVFile}
    sleep 300
done

