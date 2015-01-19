import os
from bbtlib.passwords import Password
import bbtlib.cli as cli

class LinuxBase:
    """Base class for Linux distributions
    """
    def __init__(self, root):
        self.root = os.path.realpath(root)
        self.osUsers = {}
        self._filemap = {
            '/etc/passwd': os.path.join(self.root, 'etc', 'passwd')
            }

    def getUsers(self):
        """Returns a dict of {'username': LinuxUser('username')}
        """
        with open(self._filemap['/etc/passwd'], 'r') as fd:
            lines = fd.readlines()
        usernames = [line.split(':')[0] for line in lines]
        users = {}
        for user in usernames:
            print("Gathering info on %s" % str(user))
            nixuser = LinuxUser(self, username=user)
            users[user] = nixuser
        return users

class Debian(LinuxBase):
    def __init__(self, root):
        super(Debian, self).__init__(root)

class Ubuntu(Debian):
    def __init__(self, root):
        super(Ubuntu, self).__init__(root)

class LinuxMint(Ubuntu):
    def __init__(self, root):
        super(LinuxMint, self).__init__(root)

class LinuxUser:
    """Represents a user on a linux system.
    """
    def __init__(self, osobj, **kwargs):
        """Kwargs:
        username (string)
        uid (int)
        gid (int)
        homeDir (string) Abs path to home dir
        """
        self._os = osobj
        self.root = os.path.realpath(self._os.root)
        self.uid = kwargs.get('uid', None)
        self.gid = kwargs.get('gid', None)
        self.username = kwargs.get('username', None)
        self.homeDir = kwargs.get('homeDir', None)
        self.uinfo = None
        self.shell = None
        self.password = None
        
        self.parseEtcPasswd()
        self.parseEtcShadow()

    def parseEtcPasswd(self):
        """Parses an entry in /etc/passwd for useful information.
        
        """
        passwd = os.path.join(self.root, 'etc', 'passwd')

        with open(passwd, 'r') as fd:
            lines = fd.readlines()

        if self.username is None and self.uid is None:
            raise ValueError("Need a UID or username defined to load info")
        if not lines:
            raise RuntimeError("Couldn't read %s" % passwd)

        for line in lines:
            usr, pwd, uid, gid, uinfo, home, shell = line.split(':')
            if (self.username is not None and self.username == usr) or \
                    (self.uid is not None and self.uid == uid):

                self.uid = int(uid)
                self.password = 'x'
                self.username = str(usr)
                self.gid = int(gid)
                self.userInfo = uinfo
                paths = [os.path.basename(part) for part in os.path.split(home)]
                self.homeDir = os.path.join(self.root, *paths)
                self.shell = str(shell)

                break
            
        return (self.username, self.password, self.uid, self.gid, 
                self.uinfo, self.homeDir, self.shell)
                
    def parseEtcShadow(self):
        """Parses /etc/shadow
        """
        with open('/etc/shadow', 'r') as fd:
            lines = fd.readlines()

        for line in lines:
            if line.startswith(self.username):
                p = Password.Password.fromShadow(line)
                self.password = p
        return self.password

    def getUsername(self):
        return self.username


            
