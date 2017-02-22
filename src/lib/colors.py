import ctypes
import sys
from os import name as os_name

X_RESET = "\x1B[0m"
X_RED = "\x1B[31m"
X_GREEN = "\x1B[32m"

X_SAVE_CURSOR = "\x1B[s"
X_RESTORE_CURSOR = "\x1B[u"
X_EREASE_LINE = "\x1B[K"

NT_STD_OUTPUT_HANDLE = -11
NT_FOREGROUND_RED = 0x0004
NT_FOREGROUND_GREEN = 0x0002

"""
OS HELPER FUNCTIONS 
"""
OS = "linux"
if os_name == "nt":
    OS = "NT"


"""
# print helper(windows)

def NT_downPrint(str, timestring):
    handle = ctypes.windll.kernel32.GetStdHandle(NT_STD_OUTPUT_HANDLE)
    reset = get_csbi_attributes(handle)

    # before we finish this, print the timestring!
    sys.stdout.write(timestring)
    ctypes.windll.kernel32.SetConsoleTextAttribute(handle, NT_FOREGROUND_RED)
    # print in red!
    sys.stdout.write(str)
    # reset color
    ctypes.windll.kernel32.SetConsoleTextAttribute(handle, reset)
    sys.stdout.write('\n')


def NT_UpPrint(str, timestring):
    handle = ctypes.windll.kernel32.GetStdHandle(NT_STD_OUTPUT_HANDLE)
    reset = get_csbi_attributes(handle)

    # before we finish this, print the timestring. In standard Color.
    sys.stdout.write(timestring)
    ctypes.windll.kernel32.SetConsoleTextAttribute(handle, NT_FOREGROUND_GREEN)
    # print in green now ^.^
    sys.stdout.write(str)
    # reset color
    ctypes.windll.kernel32.SetConsoleTextAttribute(handle, reset)
    sys.stdout.write('\n')


*nix ANSI Escape/Color Codes, POSIX right? Serious question.
Anyway, bash can do it.


def X_upPrint(string, timestring):
    sys.stdout.write(timestring)
    sys.stdout.write(X_GREEN + string + X_RESET + "\n")
    sys.stdout.flush()


def X_downPrint(string, timestring):
    sys.stdout.write(timestring)
    sys.stdout.write(X_RED + string + X_RESET + "\n")
    sys.stdout.flush()
"""
if OS == "NT":
    def get_csbi_attributes(handle):
        import struct
        csbi = ctypes.create_string_buffer(22)
        res = ctypes.windll.kernel32.GetConsoleScreenBufferInfo(handle, csbi)
        assert res
        (bufx, bufy, curx, cury, wattr, left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
        return wattr


    def upPrint(string, timestring):
        handle = ctypes.windll.kernel32.GetStdHandle(NT_STD_OUTPUT_HANDLE)
        reset = get_csbi_attributes(handle)

        # before we finish this, print the timestring. In standard Color.
        sys.stdout.write(timestring)
        ctypes.windll.kernel32.SetConsoleTextAttribute(handle, NT_FOREGROUND_GREEN)
        # print in green now ^.^
        sys.stdout.write(string)
        # reset color
        ctypes.windll.kernel32.SetConsoleTextAttribute(handle, reset)
        sys.stdout.write('\n')


    def downPrint(string, timestring):
        handle = ctypes.windll.kernel32.GetStdHandle(NT_STD_OUTPUT_HANDLE)
        reset = get_csbi_attributes(handle)

        # before we finish this, print the timestring!
        sys.stdout.write(timestring)
        ctypes.windll.kernel32.SetConsoleTextAttribute(handle, NT_FOREGROUND_RED)
        # print in red!
        sys.stdout.write(string)
        # reset color
        ctypes.windll.kernel32.SetConsoleTextAttribute(handle, reset)
        sys.stdout.write('\n')

else:
    def upPrint(string, timestring):
        sys.stdout.write(timestring)
        sys.stdout.write(X_GREEN + string + X_RESET + "\n")
        sys.stdout.flush()


    def downPrint(string, timestring):
        sys.stdout.write(timestring)
        sys.stdout.write(X_RED + string + X_RESET + "\n")
        sys.stdout.flush()


def printer(string, timestring, down=False):
    if down==False:
        upPrint(string, timestring)
    else:
        downPrint(string, timestring)