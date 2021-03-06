#!/usr/bin/env python
import sys
import os
os.chdir("E:\\workspace\\graphProject\\commandLine")
sys.path.append(r"E:\\workspace\\graphProject\\commandLine")
from MyParser import Parser
from panel import Panel

print("This is my command line interface for graph operations")
usage="USAGE: ./main.py outputDir [input_file]"
args=sys.argv
if len(args)<=1:
    print(usage)
    exit(0)
outputDir=args[1]
parser=Parser()
panel=Panel(outputDir=outputDir)
if len(args)==2:
    print("Start operating based on your keyboard input...")
    try:
        while True:
            if parser.waitSecondLine==False:
                userInput=input(">> ")
            else:
                userInput=input(".. ")
            parser.analyzeLine(userInput,panel)
    except EOFError as e:
        print("Thanks for using.")
        exit(0)
elif len(args)==3:
    print("Start operating based on input file...")
    try:
        f=open(args[2],"r")
    except IOError as e:
        print("Error happened while opening file:",e)
        print(usage)
        exit(1)
    lines=f.readlines()
    for l in lines:
        parser.analyzeLine(l,panel)
else:
    print(usage)