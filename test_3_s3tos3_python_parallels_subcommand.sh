#!/bin/bash

# Configuration
Target_List_CSV_FILE="list_of_copy_files.csv"
NumOfParallels=$1
SummaryResultCSVFile=$2
SarFile=test_3_sar_
ExecCommand=./test_2_s3ts3_python.py

if [ ! ${NumOfParallels} -gt 0 ]; then
    echo "Invalit Number of Paralles.(NumOfParalles=${NumOfParallels})"
    exit 1
fi

if [ ! -f ${SummaryResultCSVFile} ]; then
    echo "Not found a summary csv file(SummaryResultCSVFile=${SummaryResultCSVFile})"
    exit 1
fi


# Initialize
rows=$(grep -c '' ${Target_List_CSV_FILE})
NumOfsplitLines=$(( rows/NumOfParallels ))


#------------------------
# Functions
#------------------------
function utcserial2date {
    #echo $(date -j -f '%s' ${1} '+%Y/%m/%d %H:%M:%S') #for mac
    echo $(date --date="@${1}" '+%Y/%m/%d %H:%M:%S')  #for linux
}

#------------------------
# Main
#------------------------
# Start message
echo "Start test: targetfile=${rows} parallels=${NumOfParallels}"

# Split Target_List_CSV_FILE
split -a 5 -l ${NumOfsplitLines} ${Target_List_CSV_FILE} "test_3_target_list_"

# Lunch sar command
SAR_FILE="${SarFile}${rows}_${NumOfParallels}"
sar -A -o ${SAR_FILE} 1 10000000 >/dev/null 2>&1 &
SAR_PID=$!

# Run by background
echo "Run test programs."
StartTime=$(date '+%s')

i=0
for target in test_3_target_list_*
do
    ${ExecCommand} -i ${target} -o test_3_results_temp_$(printf "%05d" $i) &
    i=$((i+1))
done

# Wait
while [ $( ps -f |grep "${ExecCommand}"|grep -cv grep ) -gt 0 ]
do
    sleep 1
done
EndTime=$(date '+%s')
echo "Done all test programs."

kill -9 ${SAR_PID}
sleep 10

# Print result
cat test_3_results_temp_* > test_3_results_${rows}_${NumOfParallels}.csv
rm test_3_results_temp_*
success=$(grep -c Success test_3_results_${rows}_${NumOfParallels}.csv)
failed=$(grep -c Failed test_3_results_${rows}_${NumOfParallels}.csv)
total=$(( success+failed ))

sar_queue=$(LANG=C sar -f ${SAR_FILE} -q|tail -1)
sar_cpu=$(LANG=C sar -f ${SAR_FILE} -p|tail -1)

echo "${rows},${NumOfParallels},$((EndTime-StartTime)),$(utcserial2date ${StartTime}),$(utcserial2date ${EndTime}),${success},${failed},${total},${sar_queue},${sar_cpu}" >> ${SummaryResultCSVFile}
echo "${rows},${NumOfParallels},$((EndTime-StartTime)),$(utcserial2date ${StartTime}),$(utcserial2date ${EndTime}),${success},${failed},${total},${sar_queue},${sar_cpu}"


# Finall
rm test_3_target_list_*
