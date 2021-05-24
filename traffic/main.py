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
