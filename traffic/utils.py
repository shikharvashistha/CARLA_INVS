#!/usr/bin/env python3
import os, sys
from pathlib import Path

class WorkSpace:
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
        sys.path.append( self.wrk.as_posix() )
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        # sys.path.remove( self.wrk.as_posix() ) #FIXME: ?
        os.chdir(self.pwd)
        if exc_tb: pass
        pass
    pass
