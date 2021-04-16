#!/usr/bin/env python3
from pathlib import Path
import shutil
import subprocess as sp
import create_sumo_vtypes as vtypes
import netconvert_carla as net

_PREFIX = Path('../my_data')
GLOBAL_FOLDER = _PREFIX / 'global'
GLOBAL_FOLDER.mkdir(exist_ok=True, parents=True)
NET_FOLDER = _PREFIX / 'net'
NET_FOLDER.mkdir(exist_ok=True, parents=True)
ROU_FOLDER = _PREFIX / 'rou'
ROU_FOLDER.mkdir(exist_ok=True, parents=True)

print_ = lambda x:print('[convert_main] {}'.format(x))

#=====================================================#
_obj = sp.run(['bash', '-c', 'ps -a | grep CarlaUE4'], capture_output=True)
if b'CarlaUE4' not in _obj.stdout:
    print('You must have one running CarlaUE4 instance first!')
    exit(0)

#=====================================================#
view_file = Path('./data/viewsettings.xml')
if view_file.exists():
    shutil.copy(view_file, GLOBAL_FOLDER)
    print_('viewsettings.xml file generated.')
else:
    print_('viewsettings.xml file missing.')

#=====================================================#
vtype_args = vtypes.getArgParser().parse_args([
                '--carla-map', 'Town03',
                '--output-file', '%s'%(GLOBAL_FOLDER / 'carlavtypes.rou.xml')
            ])
try:
    vtypes.main(vtype_args)
except Exception as e:
    raise e
else:
    print_('vtypes.rou.xml file generated.')
    pass

#=====================================================#
xodr_glob = Path('./data').glob('*.xodr')

for xodr_file in xodr_glob:
    try:

        net.netconvert_carla(
            xodr_file = (xodr_file).as_posix(),
            output = '%s.net.xml'%(NET_FOLDER / xodr_file.stem),
            guess_tls = False
        )
    except Exception as e:
        print_('%s.net.xml file failed.'%xodr_file.stem)
    else:
        print_('%s.net.xml file generated.'%xodr_file.stem)
    pass