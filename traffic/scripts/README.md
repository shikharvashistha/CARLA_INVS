### How to use

1. Run `./convert_may.py 2>/dev/null`;
2. Select the options for file generation
    - `GEN_VIEW`: generate "viewsettings.xml", for usage in NETEDIT;
    - `GEN_VTYPE`: (need CARLA running) generate "vtypes.rou.xml" file, for vehicle blueprint use in NETEDIT;
    - `GEN_NET`: (need `xodr map file`) generate `network file` based on `xodr map file` in "./data" folder;
    - `GEN_STAT`: (need `network file`) generate random `statistics file` based on `network file`, for use in `activitygen`;
    - `GEN_ROU`: (neeed statistics file) generate route demand file using `activitygen` and `duarouter`.
3. Press `OK` button and wait for generation in "../my_data" folder.