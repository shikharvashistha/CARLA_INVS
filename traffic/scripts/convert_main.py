#!/usr/bin/env python3
from sys import argv
from pathlib import Path
import create_sumo_vtypes as vtypes
import netconvert_carla as net

MAP_NAME = argv[1]
VTYPE_FOLDER = Path('./output/global')
VTYPE_FOLDER.mkdir(exist_ok=True, parents=True)
NET_FOLDER = Path('./output/net')
NET_FOLDER.mkdir(exist_ok=True, parents=True)

#========================== ==========================#
vtype_args = vtypes.getArgParser().parse_args([
                '--carla-map', MAP_NAME,
                '--output-file', '%s.carlavtypes.rou.xml'%(VTYPE_FOLDER / MAP_NAME)
            ])
try:
    vtypes.main(vtype_args)
except Exception as e:
    raise e
else:
    print('========== vtypes.rou.xml generated for %s =========='%MAP_NAME)
    pass

#========================== ==========================#
try:
    net.netconvert_carla(
        xodr_file = 'data/%s.xodr'%MAP_NAME,
        output = '%s.net.xml'%(NET_FOLDER / MAP_NAME),
        guess_tls = False)
except Exception as e:
    raise e
else:
    print('========== *.net.xml generated for %s =========='%MAP_NAME)
    pass
