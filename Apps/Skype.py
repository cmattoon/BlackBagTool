import os, sqlite3, datetime
from classes.Asset import Asset

class Skype():
    def __init__(self, root_dir):
        if not os.path.exists(root_dir):
            raise ValueError("Path %s does not exist!" % root_dir)
        self.rootDir = root_dir
        self.users = []
        self.currentUser = ''
        

    def getDB(self, dbname):
        if not self.currentUser:
            raise ValueError("A user must be set.")
        dbpath = self.rootDir + self.currentUser + '/' + dbname
        db = sqlite3.connect(dbpath)
        db.row_factory = sqlite3.Row
        return db

    def getUsers(self):
        users = []
        ignore = ['DbTemp','shared_dynco','shared_httpfe']
        if os.path.exists(self.rootDir):
            for d in os.listdir(self.rootDir):
                if os.path.isdir(self.rootDir + d) and d not in ignore:
                    users.append(d)
        # Set current user if there is only one.
        if len(users) == 1:
            self.currentUser = users[0]
        return users

    def getContacts(self, user=None, ignore_blocked=True):
        db = self.getDB('main.db')
        c = db.cursor()
        fields = '*' # @todo - Make this not so broad
        query = "SELECT " + fields + " FROM Contacts"

        if ignore_blocked:
            query += " WHERE isblocked IS NOT '1'"

        contacts = []
        for row in c.execute(query):
            contact = SkypeContact(row)
            print "==========================="
            print contact.pretty()
            print "==========================="
class SkypeContact(Asset):
    def __init__(self,rowdata):
        self.raw = rowdata

    def pretty(self): 
        lines = []
        namestring = ''
        if self.raw['skypename']:
            namestring += 'Skype User %s' % self.raw['skypename'].encode('UTF-8')
        if self.raw['displayname']:
            namestring += ' [%s]'% self.raw['displayname'].encode('UTF-8')
        if self.raw['fullname']:
            namestring += ' Full name: %s' % self.raw['fullname'].encode('UTF-8')
        namestring  += ' Popularity: %s' % str(self.raw['popularity_ord'])
        lines.append(namestring)
        lines.append("Location: %s" % (self.getLocation()))
        if self.raw['mood_text']:
            lines.append("Mood: %s" % str(self.raw['mood_text'].strip()))
        if self.raw['lastonline_timestamp']:
            lines.append("Last Online: %s" % datetime.datetime.fromtimestamp(int(self.raw['lastonline_timestamp'])).strftime('%m/%d/%Y %H:%M:%S'))
        return "\n".join(lines)

    def getLocation(self):
        parts = []
        if self.raw['city']:
            parts.append(self.raw['city'])
        if self.raw['province']:
            parts.append(self.raw['province'])
        if self.raw['country']:
            parts.append(self.raw['country'].upper())
        return ' '.join(parts)

            



if __name__ == "__main__":
    s = Skype('/home/owner/.Skype/')

    s.currentUser = s.getUsers()[0]
    s.getContacts()
