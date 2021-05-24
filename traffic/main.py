#!/usr/bin/env python3
## amend relative import
import sys
from pathlib import Path
sys.path.append( Path(__file__).resolve().parent.parent.as_posix() ) #repo path
sys.path.append( Path(__file__).resolve().parent.as_posix() ) #file path
from params import *
## amend SUMO path
if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")
## normal import
from sys import argv
import subprocess as sp
import argparse
import carla
import sumolib, traci
from utils import *

TRAFFIC_DIRECTORY = Path(__file__).resolve().parent
OUTPUT_DIRECTORY = TRAFFIC_DIRECTORY / 'output'
DATA_DIRECTORY   = TRAFFIC_DIRECTORY / 'my_data'

def main(map_name):
    # with WorkSpace(OUTPUT_DIRECTORY) as ws:
    OUTPUT_DIRECTORY.mkdir(exist_ok=True)
    sp.run([ 'sumo', '-c', '%s.sumocfg'%(DATA_DIRECTORY/map_name),
                '--fcd-output', '%s_fcd.xml'%(OUTPUT_DIRECTORY/map_name)
    ])
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
