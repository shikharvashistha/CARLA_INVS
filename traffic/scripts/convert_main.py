#!/usr/bin/env python3
from pathlib import Path
import shutil
import subprocess as sp
from halo import Halo
from enum import Enum
import create_sumo_vtypes as vtypes
import netconvert_carla as net

_PREFIX = Path('../my_data')
GLOBAL_FOLDER = _PREFIX / 'global'; GLOBAL_FOLDER.mkdir(exist_ok=True, parents=True)
NET_FOLDER    = _PREFIX / 'net';    NET_FOLDER.mkdir(exist_ok=True, parents=True)
STAT_FOLDER   = _PREFIX / 'stat';   STAT_FOLDER.mkdir(exist_ok=True, parents=True)
ROU_FOLDER    = _PREFIX / 'rou';    ROU_FOLDER.mkdir(exist_ok=True, parents=True)

print_ = lambda x:print('[convert_main] {}'.format(x))
OPTIONS = ['GEN_VIEW', 'GEN_VTYPE', 'GEN_NET', 'GEN_STAT', 'GEN_ROU']

#=====================================================#
if True: #for code folding
    from picotui.screen import Screen
    from picotui.context import Context
    from picotui.widgets import (Dialog, WCheckbox, WButton, ACTION_OK)

    _choices = ['%d. %s'%(i+1,x) for (i,x) in enumerate(OPTIONS)]
    _status  = [WCheckbox(x, choice=False) for x in _choices] 
    with Context(cls=True):
        _width  = 4 + max( [len(x) for x in _choices] )
        _height = 1 + len(_choices)
        d = Dialog( 0, 0, _width, _height )
        # add multiple checkbox
        for i,x in enumerate(_status):
            d.add(1, i+1, x)
        # add OK butthon
        b = WButton(_width-4, "OK")
        d.add(1+int((_width-b.w)/2), _height, b)
        b.finish_dialog = ACTION_OK
        # rendering
        res = d.loop()
        pass
    Screen.cls() #cleanup the screen
    Screen.goto(0, 0) #cleanup the screen

    CHOICES = dict()
    if res==ACTION_OK:
        for x in _status:
            _key = x.t.split()[1]
            CHOICES[_key] = x.choice
        # print(res, [x.choice for x in _status])
    else:
        exit()
    pass

#=====================================================#
with Halo(text='Generate viewsettings.xml file.') as sh:
    if CHOICES['GEN_VIEW']:
        view_file = Path('./data/viewsettings.xml')
        if view_file.exists():
            shutil.copy(view_file, GLOBAL_FOLDER)
            sh.succeed()
            # print_('viewsettings.xml file generated.')
        else:
            sh.fail()
            # print_('viewsettings.xml file missing.')
    else:
        sh.info('GEN_VIEW skipped.')
    pass    

#=====================================================#
with Halo(text='Generate vtypes.rou.xml file.') as sh:
    if CHOICES['GEN_VTYPE']:
        _obj = sp.run(['bash', '-c', 'ps -a | grep CarlaUE4'], capture_output=True)
        if b'CarlaUE4' not in _obj.stdout:
            sh.fail()
            print('You must have one running CarlaUE4 instance first!')
        else:
            vtype_args = vtypes.getArgParser().parse_args([
                            '--carla-map', 'Town03',
                            '--output-file', '%s'%(GLOBAL_FOLDER / 'carlavtypes.rou.xml')
                        ])
            try:
                vtypes.main(vtype_args)
            except Exception as e:
                sh.fail()
                raise e
            else:
                sh.succeed()
                # print_('vtypes.rou.xml file generated.')
                pass
    else:
        sh.info('GEN_VTYPE skipped.')
    pass

#=====================================================#
with Halo(text='Generate *.net.xml file.') as sh:
    if CHOICES['GEN_NET']:
        xodr_glob = Path('./data').glob('*.xodr')
        for xodr_file in xodr_glob:
            _file = '%s.net.xml'%xodr_file.stem
            sh.start(text='Generate %s file.'%_file)
            try:
                net.netconvert_carla(
                    xodr_file = (xodr_file).as_posix(),
                    output = str(NET_FOLDER / _file),
                    guess_tls = False
                )
            except Exception as e:
                sh.fail()
                # print_('%s.net.xml file failed.'%xodr_file.stem)
            else:
                sh.succeed()
                # print_('%s.net.xml file generated.'%xodr_file.stem)
            pass
    else:
        sh.info('GEN_NET skipped.')
    pass

#=====================================================#
with Halo(text='Generate *.stat.xml file.') as sh:
    if CHOICES['GEN_STAT']:
        pass
    else:
        sh.info('GEN_STAT skipped.')
    pass

#=====================================================#
with Halo(text='Generate *.stat.xml file.') as sh:
    if CHOICES['GEN_ROU']:
        pass
    else:
        sh.info('GEN_ROU skipped.')
    pass
