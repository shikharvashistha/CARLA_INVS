#!/usr/bin/env python3
## amend relative import
import sys
from pathlib import Path
sys.path.append( Path(__file__).resolve().parent.parent.as_posix() ) #repo path
sys.path.append( Path(__file__).resolve().parent.as_posix() ) #file path
from params import *
## amend SUMO path
if 'SUMO_HOME' in os.environ:
    SUMO_LIB = Path(os.environ['SUMO_HOME'], 'tools')
    sys.path.append( SUMO_LIB.as_posix() )
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")
## normal import
from sys import argv
import subprocess as sp
import argparse
import carla
import sumolib, traci

TRAFFIC_DIRECTORY = Path(__file__).resolve().parent
OUTPUT_DIRECTORY = TRAFFIC_DIRECTORY / 'output'
DATA_DIRECTORY   = TRAFFIC_DIRECTORY / 'my_data'
TRACE_DIRECTORY  = TRAFFIC_DIRECTORY / 'traces'

def main(map_name):
    pass

if __name__=="__main__":
    try:
        if len(argv)==2:
            main(argv[1])
        else:
            main( input('Map name to run: ') )
    except Exception as e:
        raise e #print(e)
    finally:
        pass #exit()
