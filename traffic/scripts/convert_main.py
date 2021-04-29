#!/usr/bin/env python3
from pathlib import Path
import shutil
import subprocess as sp
from halo import Halo
import lxml.etree as ET
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
def generate_stat_xml(net_file):
    root = ET.Element('city')
    ## expand <general> element
    _attribs = {
        "inhabitants"       : "1000",
        "households"        : "500",
        "childrenAgeLimit"  : "19",
        "retirementAgeLimit": "66",
        "carRate"           : "0.58",
        "unemploymentRate"  : "0.05",
        "footDistanceLimit" : "250",
        "incomingTraffic"   : "200",
        "outgoingTraffic"   : "50",
        "laborDemand"       : "1.05"
    }
    _general = ET.SubElement(root, 'general', **_attribs)

    ## expand <parameters> element
    _attribs = {
        "carPreference"         : "1.00", #no other transportation
        "meanTimePerKmInCity"   : "6",
        "freeTimeActivityRate"  : "0.15",
        "uniformRandomTraffic"  : "0.20",
        "departureVariation"    : "300"
    }
    _parameters = ET.SubElement(root, 'parameters', **_attribs)

    ## expand <population> element
    _population = ET.SubElement(root, 'population')
    ET.SubElement(_population, 'bracket', beginAge="0",  endAge="30", peopleNbr="50") # 50% in age [0,30)
    ET.SubElement(_population, 'bracket', beginAge="30", endAge="60", peopleNbr="30") # 30% in age [30, 60)
    ET.SubElement(_population, 'bracket', beginAge="60", endAge="90", peopleNbr="20") # 20% in age [60, 90)

    ## expand <workHours> element; FIXME: change to random
    _workHours = ET.SubElement(root, 'workHours')
    ET.SubElement(_workHours, 'opening', hours='30600', proportion="0.30") #30% starts working at 0830;
    ET.SubElement(_workHours, 'opening', hours='32400', proportion="0.70") #70% starts working at 0900.
    ET.SubElement(_workHours, 'closing', hours='43200', proportion="0.20") #20% stops working at 1200;
    ET.SubElement(_workHours, 'closing', hours='63000', proportion="0.20") #20% stops working at 1730;
    ET.SubElement(_workHours, 'closing', hours='64800', proportion="0.60") #60% stops working at 1800.

    ## expand <streets> element
    _streets = ET.SubElement(root, 'streets')
    #TODO: allocate "population" and "workPosition" on edge
    net_tree = ET.parse(net_file)
    

    ## expand <cityGates> element
    _cityGates = ET.SubElement(root, 'cityGates')
    #TODO: allocate entrance on edge

    ## return
    # print( ET.tostring(root, pretty_print=True).decode('utf-8') )
    return root

generate_stat_xml()
with Halo(text='Generate *.stat.xml file.') as sh:
    if CHOICES['GEN_STAT']:
        net_file_glob = NET_FOLDER.glob('*.net.xml')
        for net_file in net_file_glob:
            
            pass
        # _obj = sp.run(['activitygen',
        #         '--net-file', '%s.net.xml',
        #         '--stat-file', '%s.stat.xml',
        #         '--output-file', '%s.trips.rou.xml',
        #         '--random']
        # , capture_output=True)
        pass
    else:
        sh.info('GEN_STAT skipped.')
    pass

#=====================================================#
with Halo(text='Generate *.stat.xml file.') as sh:
    if CHOICES['GEN_ROU']:
        _obj = sp.run(['duarouter',
                '--net-file', '%s.net.xml',
                '--route-files', '%s.trips.rou.xml',
                '--output-file', '%s.rou.xml',
                '--ignore-errors']
        , capture_output=True)
    else:
        sh.info('GEN_ROU skipped.')
    pass
