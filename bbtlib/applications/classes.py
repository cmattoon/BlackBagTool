"""
Base Classes for bbtlib
"""
class Application:
    """Represents an executable like Chrome, Skype or Microsoft Word
    """
    def getUsers(self):
        """This method should return a list of usernames.
        
        """
        pass

class ApplicationUser:
    """Abstract representation of an application's user.
    """
    def getPassword(self):
        """Returns a dict in the format {'descriptor': 'p@$$w0rd'}
        where 'descriptor' describes where this password is used. The primary
        password for the application is always keyed as 'main'.
        
        Example:
        return {
            'main': 'password', 
            'settings': 'settings password',
            'ftp_accounts': [
                FTPAccount,
                FTPAccount,
                FTPAccount
            ]
        """
        raise NotImplementedError()

    def getUserName(self):
        """Returns the username of this object.
        """
        return None

    def getSettingsFile(self):
        """Returns the absolute path of the settings file. May return a list
        or dict if multiple files are used.
        """
        pass

    def parseSettings(self):
        """Parses whatever application settings can be found for this user.
        """
        pass

    
