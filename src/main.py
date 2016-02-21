from ctypes import *
import errno
import sys
import os
import time

libc = CDLL("libc.so.6")
get_errno_loc = libc.__errno_location
get_errno_loc.restype = POINTER(c_int)

PTRACE_TRACEME = 0
PTRACE_PEEKTEXT = 1
PTRACE_POKETEXT = 4
PTRACE_CONT = 7
PTRACE_GETREGS = 12
PTRACE_SETREGS = 13
PTRACE_ATTACH = 16
PTRACE_DETACH = 17

signals = { 2 : 'HANGUP',
            3 : 'INTERRUPT',
            3 : 'QUIT',
            4 : 'ILLEGAL_INSTRUCTION',
            5 : 'BREAKPOINT_TRAP',
            6 : 'ABORTED',
            7 : 'BUS_ERROR',
            8 : 'FLOATING_POINT_EXCEPTION',
            9 : 'KILLED',
            10 : 'USER_DEFINED_SIGNAL_1',
            11 : 'SEGMENTATION_FAULT',
            12 : 'USER_DEFINED_SIGNAL_2',
            13 : 'BROKEN_PIPE',
            14 : 'ALARM_CLOCK',
            15 : 'TERMINATED',
            16 : 'STACK_FAULT',
            17 : 'CHILD_EXITED',
            18 : 'CONTINUED',
            19 : 'STOPPED_SIGNAL',
            20 : 'STOPPED',
            21 : 'STOPPED_TTY_INPUT',
            22 : 'STOPPED_TTY_OUTPUT',
            23 : 'URGENT_IO_CONDITION',
            24 : 'CPU_TIME_LIMIT_EXCEEDED',
            25 : 'FILE_SIZE_LIMIT_EXCEEDED',
            26 : 'VIRTUAL_TIMER_EXPIRED',
            27 : 'PROFILING_TIMER_EXPIRED',
            28 : 'WINDOW_CHANGED',
            29 : 'IO_POSSIBLE',
            30 : 'POWER_FAILURE',
            31 : 'BAD_SYSTEM_CALL',
            32 : 'UNKNOWN_SIGNAL_32',
            33 : 'UNKNOWN_SIGNAL_33',
            34 : 'REAL_TIME_SIGNAL_0',
            35 : 'REAL_TIME_SIGNAL_1',
            36 : 'REAL_TIME_SIGNAL_2',
            37 : 'REAL_TIME_SIGNAL_3',
            38 : 'REAL_TIME_SIGNAL_4',
            39 : 'REAL_TIME_SIGNAL_5',
            40 : 'REAL_TIME_SIGNAL_6',
            41 : 'REAL_TIME_SIGNAL_7',
            42 : 'REAL_TIME_SIGNAL_8',
            43 : 'REAL_TIME_SIGNAL_9',
            44 : 'REAL_TIME_SIGNAL_10',
            45 : 'REAL_TIME_SIGNAL_11',
            46 : 'REAL_TIME_SIGNAL_12',
            47 : 'REAL_TIME_SIGNAL_13',
            48 : 'REAL_TIME_SIGNAL_14',
            49 : 'REAL_TIME_SIGNAL_15',
            50 : 'REAL_TIME_SIGNAL_16',
            51 : 'REAL_TIME_SIGNAL_17',
            52 : 'REAL_TIME_SIGNAL_18',
            53 : 'REAL_TIME_SIGNAL_19',
            54 : 'REAL_TIME_SIGNAL_20',
            55 : 'REAL_TIME_SIGNAL_21',
            56 : 'REAL_TIME_SIGNAL_22',
            57 : 'REAL_TIME_SIGNAL_23',
            58 : 'REAL_TIME_SIGNAL_24',
            59 : 'REAL_TIME_SIGNAL_25',
            60 : 'REAL_TIME_SIGNAL_26',
            61 : 'REAL_TIME_SIGNAL_27',
            62 : 'REAL_TIME_SIGNAL_28',
            63 : 'REAL_TIME_SIGNAL_29',
            64 : 'REAL_TIME_SIGNAL_30'
        }

class registers(Structure):
    _fields_ = [
        ('r15', c_ulonglong),
        ('r14', c_ulonglong),
        ('r13', c_ulonglong),
        ('r12', c_ulonglong),
        ('rbp', c_ulonglong),
        ('rbx', c_ulonglong),
        ('r11', c_ulonglong),
        ('r10', c_ulonglong),
        ('r9', c_ulonglong),
        ('r8', c_ulonglong),
        ('rax', c_ulonglong),
        ('rcx', c_ulonglong),
        ('rdx', c_ulonglong),
        ('rsi', c_ulonglong),
        ('rdi', c_ulonglong),
        ('orig_rax', c_ulonglong),
        ('rip', c_ulonglong),
        ('cs', c_ulonglong),
        ('eflags', c_ulonglong),
        ('rsp', c_ulonglong),
        ('ss', c_ulonglong),
        ('fs_base', c_ulonglong),
        ('gs_base', c_ulonglong),
        ('ds', c_ulonglong),
        ('es', c_ulonglong),
        ('fs', c_ulonglong),
        ('gs', c_ulonglong)
    ]

def _wifstopped(status):
    return (((status.value) & 0xff) == 0x7f)

def _wstopsig(status):
    return (((status.value) & 0xff00) >> 8)

def strsignal(signal):
    return signals[signal]

def run_process(path):
    libc.ptrace(PTRACE_TRACEME,0,0,0)
    libc.execl(str.encode(path),str.encode(path),0)

def get_registers(pid):
    data = registers()
    res = libc.ptrace(PTRACE_GETREGS,pid,0,byref(data))
    return data

def set_registers(pid,data):
    return libc.ptrace(PTRACE_SETREGS, pid, 0, byref(data))

def print_rip(data):
    print('Rip: 0x%016x' % data.rip)

def get_text(addr):
    return libc.ptrace(PTRACE_PEEKTEXT,pid,addr, 0)

def print_text(addr,data):
    print('Addr 0x%016x : 0x%016x' % (addr.value,data.value))

def set_text(pid,addr,data):
    return libc.ptrace(PTRACE_POKETEXT,pid,addr,data)

def print_errno():
    print('Errno: %s: %s' % (errno.errorcode[get_errno_loc()[0]], os.strerror(get_errno_loc()[0])))

def break_and_restart(addr):
    wait_status = c_int()
    data = registers()

    # Save initial state
    initial_data = get_text(addr)
    print_text(c_ulonglong(addr),c_ulonglong(initial_data))

    # Set breakpoint
    trap_data = (initial_data & 0xFFFFFF00)|0xCC
    set_text(pid,c_ulonglong(addr),c_ulonglong(trap_data))
    print_text(c_ulonglong(addr),c_ulonglong(get_text(c_ulonglong(addr))))

    # Continue to bp
    res = libc.ptrace(PTRACE_CONT,pid,0,0)
    libc.wait(byref(wait_status))

    if _wifstopped(wait_status):
        print('Breakpoint hit. Signal: %s' % (strsignal(_wstopsig(wait_status))))
    else:
        print('Error process failed to stop')
        exit(1)

    # Reset Instruction pointer
    data = get_registers(pid)
    print_rip(data)
    data.rip -= 1
    res = set_registers(pid,data)

    # Verify rip
    print_rip(get_registers(pid))
    # Reset Instruction
    out = set_text(pid,c_ulonglong(addr),c_ulonglong(initial_data))

    if out != 0:
        print_errno()

    print_text(c_ulonglong(addr),c_ulonglong(get_text(c_void_p(addr))))


def run_debugger(pid,addr):
    wait_status = c_int()
    libc.wait(byref(wait_status))
    print('wait_status: %d' % wait_status.value)

    break_and_restart(addr)

    out = libc.ptrace(PTRACE_DETACH,pid,0,0)

    if out != 0:
        print_errno()

    print('ptrace detach %d' % out)

    libc.wait(byref(wait_status))

if __name__ == '__main__':
    # Get program path
    if len(sys.argv) < 2:
        print('Error: Please enter binary location')
        sys.exit(1)
    else:
        print(sys.argv[1])

    path = sys.argv[1]

    pid = libc.fork()

    if pid == 0: # Child
        run_process(path)
    else:
        run_debugger(pid,0x0000000000400710)
