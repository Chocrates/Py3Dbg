# import sys
# import os
# from ctypes import *
#
#
# libc = CDLL('libc.so.6')
# pid = libc.fork()
# _ptrace = libc.ptrace
# _ptrace.argtypes = [c_uint, c_uint, c_long, c_long]
# _ptrace.restype = c_long

# if pid == 0:
    #try:
    # res = libc.ptrace(0)#PTRACE_TRACEME

    # except ArgumentError as err:
    #     print("Error setting TRACEME")
    #     print(err)
    #     exit(1)
    #
    # if res == -1:
    #     try:
    #         errno = libc.get_errno()
    #     except NameError:
    #             errno = get_errno()
    #
    #     if errno != 0:
    #         print("ERROR! : %s", os.strerror(errno))
    #         exit(1)

    #print('Execling?: %d' % res)
#     libc.execl(str.encode('/usr/bin/gnome-calculator'),str.encode('/usr/bin/gnome-calculator'),0)
# else:
#     print('I am the parent')


import sys
import os
from ctypes import *


libc = CDLL('libc.so.6')
pid = libc.fork()
if pid == 0:
    res = None
    res = libc.ptrace(0,0,c_void_p(0),0)#PTRACE_TRACEME
    if res != None:
        print('ptrace return: %d' % res)
    libc.execl(str.encode('/usr/bin/gnome-calculator'),str.encode('/usr/bin/gnome-calculator'),0) # This will start then immediately throw a SIGTRAP
else:
    libc.wait()
    res = libc.ptrace(16,pid,0,0)# Attach
    print('[*] Attach Res: %d' % res)
    res = libc.ptrace(7,pid,0,0)# Continue
    print('[*] Continue Res: %d' % res)
    print('%s' % os.strerror(get_errno()))