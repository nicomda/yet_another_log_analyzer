#!/usr/bin/env python
# coding: utf-8
'''
Yet Another Log Analyzer. This tool analizes the content of log files, it has diferent operations to get usefull info. It takes a file/directory as input an processes it generating a json output file. 
'''
import argparse
import sys
import os
import re
from collections import Counter
import glob
import datetime
import operator
import json


def argumentParser(arguments: any) -> any:
    '''Parses arguments and creates help'''
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # Pops element from parser stack in order to put required argument first
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument("-i", "--input", default=".",
                          help="Path to one plain-text file, or a directory")
    optional.add_argument("--mfip", action="store_true",
                          help="Most frequent IP")
    optional.add_argument("--lfip", action="store_true",
                          help="Less frequent IP")
    optional.add_argument("--eps", action="store_true",
                          help="Events per second")
    optional.add_argument("--bytes", action="store_true",
                          help="Total amount of bytes exchanged")
    optional.add_argument("-o", "--output", default="output.json",
                          help="Path of the file where you want to store the output")
    # Adds back into the stack optional arguments, but this time after the required.
    parser._action_groups.append(optional)
    args = parser.parse_args(arguments)
    return args


def calculateMostAndLessFrequentIp(ips: list) -> list:
    '''Use collections to get the most and less frequent ip'''
    # Assumption: More than 1 IP could match any of the filters, but we'll consider first and last element of Counter(Dict subclass) to simplify
    occurences = Counter(ips)
    return occurences.most_common()[0], occurences.most_common()[-1]


def calculateOldestTime(epochs: list) -> str:
    epochs.sort()
    return epochs[0]


def calculateNewestTime(epochs: list) -> str:
    epochs.sort()
    return epochs[-1]


def calculateEventsPerSecond(epochs: list, events: int) -> float:
    epochs.sort()
    oldest_date = datetime.datetime.fromtimestamp(float(epochs[0]))
    newest_date = datetime.datetime.fromtimestamp(float(epochs[-1]))
    time_difference_in_seconds = (newest_date-oldest_date).total_seconds()
    return float(events)/time_difference_in_seconds


def parseFile(input_path: str) -> list:
    '''Parses each line of a file via regex, check if the line is okay, and return a list with usefull data'''
    '''
    Elements available to parse:
    Field 1: 1157689324.156 [Timestamp in seconds since the epoch]
    Field 2: 1372 [Response header size in bytes]
    Field 3: 10.105.21.199 [Client IP address]
    Field 4: TCP_MISS/200 [HTTP response code]
    Field 5: 399 [Response size in bytes]
    Field 6: GET [HTTP request method]
    Field 7: http://www.google-analytics.com/__utm.gif? [URL]
    Field 8: badeyek [Username]
    Field 9: DIRECT/66.102.9.147 [Type of access/destination IP address]
    Field 10: image/gif [Response type]       
    '''
    print(f"Processing file: {input_path}")
    lines = []
    try:
        with open(input_path, "r", encoding='utf-8') as logfile:
            for line in logfile:
                line = line.strip()
                line_elements = re.split('\s+', line)
                if len(line_elements) == 10:  # Checking if the line has all the elements
                    elements = {
                        "timestamp": line_elements[0],
                        "headerbytes": line_elements[1],
                        "ipaddress": line_elements[2],
                        "responsebytes": line_elements[4]
                    }
                    lines.append(elements)
    except Exception as e:
        print("Error reading the file.")
    return lines


def logProcessor(args: argumentParser) -> dict:
    '''
    Normalizes filename, if file, reads it and process. If directory, reads each file and process.
    Calculates More & Less frequent IP's
    Calculates
    '''
    file_list = []  # List to get all files in a directory
    ips_max = {}  # Dict to get most frequent values of each file
    ips_min = {}  # Dict to get less frequent values of each file
    ips_list = []  # IP's list
    # Epoch Timestamp list for later calculation of time difference and events/sec
    # List to store all epochs of a file (it will clear itself with each new file)
    epoch_list = []
    epoch_final = []  # List to store oldest and newer epoch of each file
    max_bytes = 0  # Integer to get sum of all bytes
    event_count = 0  # Integer to store total count of events
    results = {}  # Dictionary to return the result array
    # Handling any typical OS filepath
    normalized_path = os.path.normpath(args.input)

    # If it's a directory, fill file_list with any .log match
    if os.path.isdir(normalized_path):
        file_list = glob.glob(f"{normalized_path}/*.log", recursive=True)
        for file in file_list:
            file = os.path.normpath(file)

    if os.path.isfile(normalized_path):  # If it's a file, fill file_list with itself
        if normalized_path.endswith(".log"):
            file_list.append(normalized_path)

    if len(file_list) > 0:  # If files ready to process, ready to rumble!!
        print(f"{len(file_list)} files are going to be processed")
        for file in file_list:
            file_elements = parseFile(file)
            for elements in file_elements:
                # Preparing IP address list for later calculation
                ips_list.append(elements['ipaddress'])

                # Preparing epoch list for later calculation
                epoch_list.append(elements['timestamp'])

                # Sum of header & response bytes to get the maximum
                max_bytes += int(elements['headerbytes'])
                max_bytes += int(elements['responsebytes'])

                event_count += 1  # Counting events (1 event per element)
            # Calculating more & less frequent IP's
            ip_more_frequent, ip_less_frequent = calculateMostAndLessFrequentIp(
                ips_list)
            ips_max[f"{ip_more_frequent[0]}"] = ip_more_frequent[1]
            ips_min[f"{ip_less_frequent[0]}"] = ip_less_frequent[1]
            # Adding newest and oldest time of a file to final epoch list
            epoch_final.append(calculateNewestTime(epoch_list))
            epoch_final.append(calculateOldestTime(epoch_list))
        # Once all files are read, it's time to generate the results
        if args.mfip:
            results["mfip"] = max(ips_max.items(),
                                  key=operator.itemgetter(1))[0]
        if args.lfip:
            results["lfip"] = min(ips_min.items(),
                                  key=operator.itemgetter(1))[0]
        if args.eps:
            results["eps"] = calculateEventsPerSecond(
                epoch_final, event_count)
        if args.bytes:
            results["bytes"] = max_bytes
    else:
        print(
            f"The path passed as argument is not a valid file or directory: {input_path}")
    return results

def writeDict2JSONFile(output_path: str, data: dict) -> None:
    try:
        normalized_path = os.path.normpath(output_path)
        with open(normalized_path, "w") as json_file:
            json.dump(data, json_file)
        print(f"You can find the resulting .json at: {normalized_path}")
    except Exception as e:
        print("Data couldn't be written into a JSON file")

def main(arguments: any) -> None:
    args = argumentParser(arguments)
    results = logProcessor(args)
    print(results)
    writeDict2JSONFile(args.output, results)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
