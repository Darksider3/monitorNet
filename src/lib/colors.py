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


def get_csbi_attributes(handle):
	import struct
	csbi = ctypes.create_string_buffer(22)
	res = ctypes.windll.kernel32.GetConsoleScreenBufferInfo(handle, csbi)
	assert res
	(bufx, bufy, curx, cury, wattr, left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
	return wattr


# print helper(windows)
def NT_downPrint(str, timeStr):
	handle = ctypes.windll.kernel32.GetStdHandle(NT_STD_OUTPUT_HANDLE)
	reset = get_csbi_attributes(handle)

	# before we finish this, print the timeStr!
	sys.stdout.write(timeStr)
	ctypes.windll.kernel32.SetConsoleTextAttribute(handle, NT_FOREGROUND_RED)
	# print in red!
	sys.stdout.write(str)
	# reset color
	ctypes.windll.kernel32.SetConsoleTextAttribute(handle, reset)
	sys.stdout.write('\n')


def NT_UpPrint(str, timeStr):
	handle = ctypes.windll.kernel32.GetStdHandle(NT_STD_OUTPUT_HANDLE)
	reset = get_csbi_attributes(handle)

	# before we finish this, print the timeStr. In standard Color.
	sys.stdout.write(timeStr)
	ctypes.windll.kernel32.SetConsoleTextAttribute(handle, NT_FOREGROUND_GREEN)
	# print in green now ^.^
	sys.stdout.write(str)
	# reset color
	ctypes.windll.kernel32.SetConsoleTextAttribute(handle, reset)
	sys.stdout.write('\n')


"""
*nix ANSI Escape/Color Codes, POSIX right? Serious question.
Anyway, bash can do it.
"""


def X_UpPrint(str, timestr):
	sys.stdout.write(timestr)
	sys.stdout.write(X_GREEN + str + X_RESET + "\n")
	sys.stdout.flush()


def X_downPrint(str, timestr):
	sys.stdout.write(timestr)
	sys.stdout.write(X_RED + str + X_RESET + "\n")
	sys.stdout.flush()


def printer(str, timestr, down=False):
	if OS == "NT":
		if down == False:
			NT_UpPrint(str, timestr)
		else:
			NT_downPrint(str, timestr)
	else:
		if down == False:
			X_UpPrint(str, timestr)
		else:
			X_downPrint(str, timestr)
