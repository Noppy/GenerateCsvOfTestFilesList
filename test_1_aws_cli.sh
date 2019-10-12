#!/bin/bash

if [ "A$1" = "A" -o ! -f $1 ]; then
	echo "not found the csv file.($1)"
fi

while read line
do
    item=(${line//,/ })
    aws --profile=${Profile} s3 cp ${item[0]} ${item[1]}
done < $1
