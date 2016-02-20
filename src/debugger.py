from ctypes import *
from debugger_defines import *
import datetime

libc = CDLL("libc.so.6")
get_errno_loc = libc.__errno_location
get_errno_loc.restype = POINTER(c_int)
ERRNO = -1







class debugger():
    pid =-1
    debugger_active = False
    breakpoints = []

    def _get_error(self,ret, func, args):
        if ret == -1:
            e = get_errno_loc()[0]
            #raise OSError(e)
            self.ERRNO = e
        return ret

    def __init__(self):
        self.ptrace = libc.ptrace
        self.ptrace.errcheck = self._get_error

    def open_process(self, path_to_elf):
        # Opens a process at the specified path
        # Open the child process by forking a new process and replacing the process memory with the exe
        self.pid = libc.fork()
        if self.pid < 0:
            print('[*] Error fork failed, pid returned was %d' % self.pid)
        elif self.pid > 0:# Parent
            self.debugger_active = True
            return self.pid
        else: # Child
            self.ptrace(PTRACE_TRACEME,0,0,0) # Tell the kernel that we are ok to trace, else we have to be root
            args = [str.encode(path_to_elf), None]
            args = (c_char_p * len(args))(*args)
            libc.execv(str.encode(path_to_elf), args)

    def attach_process(self,pid):
        # Attaches to process on the specified PID
        self.pid = pid
        if self.ptrace(PTRACE_ATTACH,c_int(self.pid),None,None) != 0:
            print('Error failed to attach to process: ERRNO %s' % self.ERRNO)
        else:
            self.debugger_active = True

    def detach(self):
        if self.ptrace(PTRACE_DETACH,c_int(self.pid),None,0) != 0:
            print('Error detaching')
        else:
            self.debugger_active = False

    def set_bp(self,address):
        if not self.breakpoints.has_key(address):
            # Store proc memory at address
            data = self.ptrace(PTRACE_PEEKTEXT, self.pid, c_uint(address),0)
            # Write int 0xcc to address
            trapped_data = (c_uint(data) & 0xFFFFFF00) | 0xCC
            self.ptrace(PTRACE_POKETEXT, self.pid, address, trapped_data)









