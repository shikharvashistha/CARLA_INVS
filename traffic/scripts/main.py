#!/usr/bin/env python3
from sys import argv
import create_sumo_vtypes as vtypes
import netconvert_carla as net

MAP_NAME = argv[1]

#========================== ==========================#
vtype_args = vtypes.getArgParser().parse_args(
                ['--carla-map', MAP_NAME, '--output-file', '%s.carlavtypes.rou.xml'%MAP_NAME])
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
        output = '%s.net.xml'%MAP_NAME,
        guess_tls = False)
except Exception as e:
    raise e
else:
    print('========== *.net.xml generated for %s =========='%MAP_NAME)
    pass
