import os

class GoogleChrome:
    def __init__(self, root_dir):
        """Call this with the root directory of the mounted partition.
        """
        root_dir = os.path.realpath(root_dir)
        if not os.path.exists(root_dir):
            raise OSError("root_dir '%s' does not exist" % root_dir)

        self._rootDir = root_dir

        self._checkInstallation()

    def _getDataHome(self):
        dirs = {'data': []}
        for homedir in os.listdir(os.path.join(self._rootDir, 'home')):
            usrhome = os.path.join(self._rootDir, 'home', homedir)

            dirs['data'].append(os.realpath())
            
            

    def _checkInstallation(self):
        pass


gc = GoogleChrome('/etc/no')
