from ctypes import *

PTRACE_ATTACH = 16
PTRACE_DETACH = 17
PTRACE_TRACEME = 0
PTRACE_PEEKTEXT = 1
PTRACE_CONT = 7

# http://lxr.free-electrons.com/source/arch/x86/include/asm/user_64.h#L68
class registers(Structure):
    _fields_ = [
        ('r15', c_ulong),
        ('r14', c_ulong),
        ('r13', c_ulong),
        ('r12', c_ulong),
        ('bp', c_ulong),
        ('bx', c_ulong),
        ('r11', c_ulong),
        ('r10', c_ulong),
        ('r9', c_ulong),
        ('r8', c_ulong),
        ('ax', c_ulong),
        ('cx', c_ulong),
        ('dx', c_ulong),
        ('si', c_ulong),
        ('di', c_ulong),
        ('orig_ax', c_ulong),
        ('ip', c_ulong),
        ('cs', c_ulong),
        ('flags', c_ulong),
        ('sp', c_ulong),
        ('ss', c_ulong),
        ('fs_base', c_ulong),
        ('gs_base', c_ulong),
        ('ds', c_ulong),
        ('es', c_ulong),
        ('fs', c_ulong),
        ('gs', c_ulong)
    ]