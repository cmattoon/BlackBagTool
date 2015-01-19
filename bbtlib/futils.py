"""
File utils
"""
import os
import bbtlib.mathlib
from bbtlib.cli import *

class FileSystem:
    """Provides data about the operating system that is mounted at self.root
    """
    
    def __init__(self, root):
        self.linux = None
        self.osx = None
        self.windows = None
        
        self.root = os.path.realpath(root)
        self.detectOS()

    def detectOS(self):
        """Determines windows/linux/mac and calls sub-checks.
        """
        files = [filename.lower() for filename in os.listdir(self.root)]
        
        nix = ['bin', 'boot', 'dev', 'etc', 'home', 'lib' 'media', 'mnt',
                 'opt', 'sbin', 'srv', 'tmp', 'usr', 'var', 'root', 'proc',
                 'initrd.img', 'vmlinuz']
        
        osx = ['Applications', 'Library', 'Network', 'System',
               'User Information', 'Users', 'Volumes', 'bin', 'cores', 'dev',
               'etc', 'home', 'mach_kernel', 'net', 'private', 'sbin', 'tmp',
               'usr', 'var']

        win = ['$Recycle.Bin', 'Boot', 'Documents and Settings', 'inetpub',
                   'PerfLogs', 'ProgramData', 'Program Files', 'Recovery',
                   'Program Files (x86)', 'System Volume Information', 'Users',
                   'Windows']

        results = {osname: bbtlib.mathlib.cosine_similarity(files, lst) 
                   for (osname, lst) in zip(('linux', 'osx', 'windows'), 
                                            (nix, osx, win))}
        self._os = max(results, key=results.get)
        
        if self._os == 'linux':
            return self._detectLinux()

        elif self._os == 'osx':
            return self._detectOSX()

        elif self._os == 'windows':
            return self._detectWindows()

        else:
            warn("Could not determine base operating system!")
            debug(" ".join(["(%s: %0.2f" % (key, value * 100) for (key, value) in 
                            results.iteritems()]))
            return results

    def _detectLinux(self):
        from bbtlib.platforms import Linux as lx
        nix = lx.LinuxBase(self.root)
        return nix

    def _detectOSX(self):
        return None

    def _detectWindows(self):
        return None


    
def get_os(fs_root):
    """Given a filesystem root directory (e.g., '/mnt/external_drive' or '/'),
    returns a DictObj of information.
    """

def list_home(user, **kwargs):
    """OS-independent way to return a list of files in the specified user's
    home directory. 

    If usernames can appear in different formats, or require translation to a 
    home folder (e.g., alt. home folders in Linux), and that requires additional
    configuration, consider adding kwargs.

    """
if __name__ == "__main__":    
    fs = FileSystem('/')
    opsys = fs.detectOS()
    users = opsys.getUsers()
