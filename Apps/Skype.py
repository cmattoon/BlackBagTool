import os, sqlite3

class Skype():
    contactFields = ['skypename', 'displayname', 'fullname', 'birthday','aliases',
                     'gender', 'nr_of_buddies', 'city', 'province', 'country', 
                     'server_synced', 'isauthorized','popularity_ord','mood_text',
                     'about', 'timezone', 'lastonline_timestamp']
    def __init__(self, root_dir):
        if not os.path.exists(root_dir):
            raise ValueError("Path %s does not exist!" % root_dir)
        self.rootDir = root_dir
        self.users = []
        self.currentUser = ''
        

    def getDB(self, dbname):
        pass

    def getUsers(self):
        users = []
        ignore = ['DbTemp','shared_dynco','shared_httpfe']
        if os.path.exists(self.rootDir):
            for d in os.listdir(self.rootDir):
                if os.path.isdir(self.rootDir + d) and d not in ignore:
                    users.append(d)
        return users

    def getContacts(self, ignore_blocked=True):
        db = self.getDB('main.db')
        c = db.cursor()
        fields = ','.join(self.contactFields)
        query = "SELECT " + fields + " FROM Contacts"
        if ignore_blocked:
            query += " WHERE isblocked IS NOT '1'"
        for row in c.execute(query):
            contact

