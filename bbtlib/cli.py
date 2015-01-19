import os
import sys

def output(message, fd=None, nl=True):
    """Outputs message as a string.
    Args:
      message (string) The message to print
      fd (file descriptor) Something with a write method
      nl (bool) Whether or not to print os.linesep
    """
    fd = sys.stdout if fd is None else fd
    nl = os.linesep if nl is True else ''
    fd.write("%s%s" % (str(message), nl))

def warn(message):
    """Issues a warning
    """
    output("\033[93m [!] %s\033[0m" % (str(message)), sys.stderr)

def debug(message):
    output("[debug] %s" % (str(message)), sys.stderr)

