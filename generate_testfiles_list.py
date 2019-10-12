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
import os
import traceback
import argparse
import json
import csv
import datetime
import math



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

    parser.add_argument('-c','--conf',
        action='store',
        default='config.json',
        type=str,
        required=False,
        help='Specify configuration json file.')

    parser.add_argument('-o','--output',
        action='store',
        default='list_of_copy_files.csv',
        type=str,
        required=False,
        help='Specify output CSV file.')

    return( parser.parse_args() )


def create_folders(period):

    # Initialize
    folders = []

    # set period day
    start_day = datetime.datetime.strptime(period["StartDate"], '%Y/%m/%d')
    end_day = datetime.datetime.strptime(period["EndDate"], '%Y/%m/%d')
    if start_day > end_day:
        print("Invalid StartDate or EndDate.")
        return

    # generate foler path
    pd = start_day
    while pd <= end_day:
        for hour in range(0,24):
            folders.append( "{0:04d}/{1:02d}/{2:02d}/{3:02d}/".format( pd.year, pd.month, pd.day, hour) )

        # Add 1day
        pd += datetime.timedelta(days=1)
    
    #set
    ret = {
        "PathOfFolders": folders,
        "NumberOfFolders": len(folders)
    }
    return(ret)


def load_configuration_file(args):
    
    conf = {
        "NumberOfFiles" : -1,
        "Source": []
    }

    # Load a json file and set source files.
    try:
        fp = open(args.conf)
        data = json.load(fp)

        if args.debug:
            print("===Raw data of the JSON Configuration file===")
            print(json.dumps(data, indent=2))

        # Set General parameters
        conf["NumberOfFiles"] = int(data["NumberOfFiles"])
        conf["Destination"] = data["Destination"]["DestPath"]
        conf["Period"] = data["Period"]

        # Generate folders list
        conf["Folders"] = create_folders(conf["Period"])
        conf["NumberOfFileInFolder"] = float(conf["NumberOfFiles"]) / float(conf["Folders"]["NumberOfFolders"])

        # Set Sourece files list
        total = 0
        for src_dic in data["Source"]:
            total += int(src_dic["Ratio"])
        
        for src_dic in data["Source"]:
            src = {
                "Path": src_dic["Path"],
                "Number": int( math.ceil( float( conf["NumberOfFileInFolder"] ) * float(src_dic["Ratio"]) / float(total) ) )
            }
            conf["Source"].append(src)

        # Debug Print
        if args.debug:
            print("===Configration ===")
            print(json.dumps(conf, indent=2))

        return( conf )

    except IOError as e:
        print(e)
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))
    
    return

# ---------------------------
# Generate CSV
# ---------------------------
def generate_a_folder(args, config, dest_folder_path):

    # Initilize
    files = []

    for src in config["Source"]:

        for i in range(0, src["Number"]):
            name,ext = os.path.splitext( os.path.basename(src["Path"]) )
            # Generate a CSV row data
            row = [
                src["Path"],
                os.path.join( dest_folder_path, name+"_{:06d}".format(i)+ext )
            ]
            files.append(row)
    
    return( files )




def generate_file_list(args, config):

    # open CSV file for write
    try:
        fp = open( args.output, 'w')
        writer = csv.writer(fp, lineterminator='\n')
    except IOError as e:
        print(e)
        return
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))
        return

    # Generate list
    for folder in config["Folders"]["PathOfFolders"]:
        dest = os.path.join(config["Destination"], folder)
        files = generate_a_folder(args, config, dest)
        writer.writerows(files)


    # Close
    fp.close()


# ---------------------------
# The main function
# ---------------------------
def main():

    # Initialize
    args = get_args()

    # Read configuration json file
    config = load_configuration_file(args)
    if config is None: return False

    # Generate a CSV File of copy files list
    generate_file_list(args, config)


if __name__ == "__main__":
    sys.exit(main())