from Asset import Asset

class Cookie(Asset):
    def __init__(self):
        # Time the cookie was created (in UTC)
        self.creationTime = None
        # The domain
        self.hostKey = None
        # The name
        self.name = None
        # The value
        self.value = None
        # The path the cookie is valid for.
        self.path = None
        # Expiration date (UTC)
        self.expireTime = None
        self.secure = None
        self.httpOnly = None
        # The time the cookie was last accessed, according to the browser (UTC)
        self.lastAccessed = None
        # Chrome
        self.hasExpires = None
        self.persistent = None
        self.priority = None

        Asset.__init__(self)

    def pretty(self, print_output=False):
        lines = []
        lines.append('[COOKIE] %s' % self.hostKey)
        lines.append('    Created: %s' % self.formatTimestamp(self.creationTime))
        lines.append('    Expires: %s' % self.formatTimestamp(self.expireTime))
        lines.append('    Last Accessed: %s' % self.formatTimestamp(self.lastAccessed))
        lines.append('    Name: %s' % self.name)
        lines.append('    Value: %s' % self.value)
        subs = []
        if self.secure:
            subs.append('[SECURE]')
        if self.persistent:
            subs.append('[PERSISTENT]')
        if self.priority:
            subs.append('[Priority %d]' % int(self.priority))
        if len(subs):
            lines.append('    ' + ' '.join(subs))
        if print_output:
            for line in lines:
                print line
            return True
        return "\n".join(lines)

        
