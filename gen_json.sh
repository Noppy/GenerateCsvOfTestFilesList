#!/bin/bash


#要件に応じて設定
NumberOfFiles=$1
StartDate=$2
EndDate=$3
Bucket=$4
DestS3BucketAndPrefix="s3://${Bucket}/original-data/"
#固定設定
CONFIG_FILE="config.json"
MASTER_FILE=$(aws s3 ls ${DestS3BucketAndPrefix} --recursive | awk '{print $4}')

#
echo "{
    \"NumberOfFiles\": \"${NumberOfFiles}\",
    \"Period\": {
        \"StartDate\": \"${StartDate}\",
        \"EndDate\": \"${EndDate}\"
    },
    \"Source\": [" > ${CONFIG_FILE}
TEMP=""
for i in ${MASTER_FILE}
do
	TEMP="${TEMP}      {\n"
	TEMP="${TEMP}            \"Path\": \"s3://${Bucket}/${i}\",\n"
	TEMP="${TEMP}            \"Ratio\": 1\n"
	TEMP="${TEMP}      },\n"
done
echo -e "${TEMP%???}" >> ${CONFIG_FILE}
echo "    ],
    \"Destination\": {
      \"DestPath\": \"s3://${Bucket}\"
    }
}" >> ${CONFIG_FILE}

