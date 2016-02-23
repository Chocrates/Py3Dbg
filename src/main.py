from ctypes import *
import errno
import sys
import debugger
import os
import time


if __name__ == '__main__':
    # Get program path
    if len(sys.argv) < 2:
        print('Error: Please enter binary location')
        sys.exit(1)
    else:
        print(sys.argv[1])

    path = sys.argv[1]

    dbg = debugger.debugger()
    pid = os.fork()

    if pid == 0: # Child
        dbg.run_process(path)
    else:
        #run_debugger(pid,0x0000000000400710)
        dbg.set_pid(pid)
        print(dbg.get_strsignal()) # Halts right after it overwrites the process memory
        bp = dbg.set_bp(0x0000000000400710)
        dbg.run()
        dbg.unset_bp(bp)
        dbg.detach()
        os.wait()

