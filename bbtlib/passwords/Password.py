from bbtlib.contrib import HashTag

class Password:
    """A password object to manipulate and possibly recover
    """
    def __init__(self):
        self._username = ''
        self._plaintext = ''
        self._hashvalue = ''
        self._hashType = ''
        self._description = ''
        self._dateChanged = None
        self.requiresChange = None

    def username(self, name=None):
        if name is not None:
            self._username = name
        return self._username

    def plaintext(self, pt=None):
        """Getter/setter for plain text value (should be a string)
        """
        if pt is not None:
            self._plaintext = pt
        return self._plaintext

    def hash(self, val=None):
        """Getter/setter for hash value (should be a string)
        """
        if val is not None:
            self._hashvalue = val
            self.getType()

        return self._hashvalue
        
    def getType(self):
        """Returns the hash type of the password.
        """
        if not self._hashvalue:
            return None
        try:
            self._hashType = HashTag.identifyHash(self._hashValue)
        except:
            self._hashType = None
        return self._hashType

    @staticmethod
    def fromShadow(shadow_line):
        """Returns a LinuxUserPassword object with properties populated from 
        a line in /etc/shadow:

        Fields:
            0 - username
            1 - password hash
            2 - date of last change (epoch days)
            3 - days before passwd can be changed (0=any)
            4 - days after which passwd MUST be changed (99999=never)
            5 - days to warn user of an expiring password
            6 - number of days after password expiration that acct is disabled
            7 - disable date (epoch days)
            8 - reserved
        """
        parts = shadow_line.split(':')
        if len(parts) is not 9:
            raise ValueError("Invalid data for /etc/shadow line")

        pwd = Password()
        pwd.username(parts[0])
        pwd.hash(parts[1])
        return pwd
        """@todo - handle date functions
        """

class LinuxUserPassword(Password):
    def __init__(self):
        super(LinuxUserPassword, self).__init__()
        
