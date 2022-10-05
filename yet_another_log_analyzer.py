#!/usr/bin/python3
# coding: utf-8
'''
Yet Another Log Analyzer\n
Author: Nicolás Moral
'''
import argparse
import sys
import os
def argumentParser(arguments: any) -> any:
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

def main(arguments: any) -> None:
    args=argumentParser(arguments)



if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
