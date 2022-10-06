#!/usr/bin/python3
# coding: utf-8
'''
Yet Another Log Analyzer. This tool analizes the content of log files, it has diferent operations to get usefull info. It takes a file/directory as input an processes it generating a json output file. 
'''
import argparse
import sys
import os
import re

def argumentParser(arguments: any) -> any:
    '''Parses arguments and creates help'''
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    optional = parser._action_groups.pop() #Pops element from parser stack in order to put required argument first
    required = parser.add_argument_group('required arguments')
    required.add_argument("-i","--input", required=True, help="Path to one plain-text file, or a directory")
    optional.add_argument("--mfip", action="store_true", help="Most frequent IP")
    optional.add_argument("--lfip", action="store_true", help="Less frequent IP")
    optional.add_argument("--eps", action="store_true", help="Events per second")
    optional.add_argument("--bytes", action="store_true", help="Total amount of bytes exchanged")
    optional.add_argument("-o""--output", default="output.json", help="Path of the file where you want to store the output")
    parser._action_groups.append(optional) #Adds back into the stack optional arguments, but this time after the required.
    args = parser.parse_args(arguments)
    return args

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
    print(f"File to process: {input_path}")
    lines=[]
    try:
        with open(input_path,"r", encoding='utf-8') as logfile:
            for line in logfile:
                line=line.strip()
                line_elements=re.split('\s+', line)
                if len(line_elements)==10: #Checking if the line has all the elements
                    elements={
                        "timestamp":line_elements[0],
                        "headerbytes":line_elements[1],
                        "ipaddress":line_elements[2],
                        "responsebytes":line_elements[4]
                    }
                    lines.append(elements)
    except Exception as e:
        print("Error reading the file.")
    return lines

def logProcessor(input_path: str) -> None:
    '''
    Normalizes filename, if file, reads it and process. If directory, reads each file and process.
    '''
    normalized_path=os.path.normpath(input_path)
    if os.path.isfile(normalized_path):
        file_elements=parseFile(normalized_path)

    elif os.path.isDirectory(input_path):
        return
        #TODO Add capability to process more than one file

    else:
        print(f"The path passed as argument is not file or directory: {input_path}")

def main(arguments: any) -> None:
    results={
        "most_frequent_ip":"",
        "less_frequent_ip":"",
        "events_per_second": 0,
        "total_bytes_exchanged": 0
        }
    args=argumentParser(arguments)
    parsedList=logProcessor(args.input)
    
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
