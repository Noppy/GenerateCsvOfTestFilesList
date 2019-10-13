#!/bin/bash

# Configuration
ListNumOfParallels="1 12 30"
SummaryResultCSVFile=test_3_results_summary.csv
ExecCommand=./test_3_s3tos3_python_parallels_subcommand.sh


#------------------------
# Main
#------------------------

cp /dev/null ${SummaryResultCSVFile}


for parallel in ${ListNumOfParallels}
do
    ${ExecCommand} ${parallel} ${SummaryResultCSVFile}
done

