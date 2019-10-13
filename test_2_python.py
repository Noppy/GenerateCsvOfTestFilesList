#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  create_iamuser.py
#  ======
#  Copyright (C) 2018 n.fujita
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
from __future__ import print_function

import sys
import argparse
import csv

import boto3
from botocore.exceptions import ClientError

# ---------------------------
# Initialize Section
# ---------------------------
def get_args():
    parser = argparse.ArgumentParser(
        description='Generate a CSV file that lists the test files to created.')

    parser.add_argument('-d','--debug',
        action='store_true',
        default=False,
        required=False,
        help='Enable dry-run')

    parser.add_argument('-i','--input',
        action='store',
        default='list_of_copy_files.csv',
        type=str,
        required=False,
        help='Specify a target list CSV file.')

    parser.add_argument('-o','--output',
        action='store',
        default='test_2_result.csv',
        type=str,
        required=False,
        help='Specify output CSV file.')

    return( parser.parse_args() )


# ---------------------------
# The main function
# ---------------------------
def main():

    # Initialize
    args = get_args()

    # Open csv and result file
    fp_csv = open( args.input )
    reader = csv.reader(fp_csv)

    fp_result = open( args.output, "w")
    writer = csv.writer(fp_result)

    # Get session
    s3 = boto3.client('s3')

    # copy 
    for row in reader:

        copy_source = {
            'Bucket': src_bucket_name,
            'Key': src_object_name
        }


        # Copy the object
        try:
            s3.copy_object(
                CopySource=copy_source,
                Bucket=dest_bucket_name,
                Key=dest_object_name
            )
        except ClientError as e:
            logging.error(e)

    return

if __name__ == "__main__":
    sys.exit(main())