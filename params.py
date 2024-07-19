#!/usr/bin/env python3
import os, sys
from pathlib import Path

CARLA_PATH = Path('~/CARLA').expanduser()
ROOT_PATH  = Path(__file__).parent

# include CARLA egg file
try:
    _egg_file = '/home/user/Desktop/shikharvashistha/carla/PythonAPI/carla/dist/carla-0.9.14-py3.7-linux-x86_64.egg'
    # _egg_file = sorted(Path(CARLA_PATH, 'PythonAPI/carla/dist').glob('carla-*%d.*-%s.egg'%(
    #     sys.version_info.major,
    #     'win-amd64' if os.name=='nt' else 'linux-x86_64'
    # )))[0].as_posix()
    sys.path.append(_egg_file)
except IndexError:
    print('CARLA Egg File Not Found.')
    exit()

##for gen_data
LOG_PATH   = ROOT_PATH / 'log'
RAW_DATA_PATH  = ROOT_PATH / 'raw_data'
COOK_DATA_PATH = ROOT_PATH / 'dataset'
#https://carla.readthedocs.io/en/latest/core_map/#changing-the-map
TOWN_MAP = ['_', 'Town01', 'Town02', 'Town03', 'Town04', 'Town05'][4]
RAW_DATA_START  = 60#frame
RAW_DATA_END    = -10#frame
RAW_DATA_FREQ   = 1#Hz
RAW_DATA_FREQ_ALT=1#Hz, for img_list generation

##for PCDet
ENTRY_FILE = str(ROOT_PATH / 'PCDet' / 'fed.py')
TRAIN_ROOT = ROOT_PATH / 'PCDet' / 'tools'
MODEL_FOLDER = ROOT_PATH / 'model'

##utility
class workSpace:
    def __init__(self, p, *p_l, **kargs):
        self.wrk = Path(p, *p_l).expanduser().resolve()
        self.pwd = Path.cwd()
        if 'forceUpdate' in kargs.keys():
            self.forceUpdate = True
        else:
            self.forceUpdate = False
        pass
    
    def __enter__(self):
        if not Path(self.wrk).is_dir():
            if self.forceUpdate:
                Path(self.wrk).mkdir(mode=0o755, parents=True, exist_ok=True)
            else:
                return self.__exit__(*sys.exc_info())
        else:
            pass
        os.chdir(self.wrk)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        os.chdir(self.pwd)
        if exc_tb: pass
        pass
    pass
