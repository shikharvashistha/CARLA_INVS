#!/usr/bin/env python3
# amend relative import
import sys
from pathlib import Path
sys.path.append( Path(__file__).resolve().parent.parent.as_posix() ) #repo path
sys.path.append( Path(__file__).resolve().parent.as_posix() ) #file path
from params import *

# normal import
import carla
import argparse

def main():

    pass

if __name__=="__main__":
    try:
        main()
    except Exception as e:
        raise e#print(e)
    finally:
        pass#exit()
