from Browser import Browser
from classes.WebHistory import WebHistory
from classes.Download import Download
from classes.Cookie import Cookie
from ConfigParser import SafeConfigParser
import sqlite3, os, shutil

class Firefox(Browser):
    def __init__(self, filepath, outpath):
        if not os.path.exists(filepath):
            raise ValueError("Filepath %s does not exist!" % filepath)
        if not os.path.exists(outpath):
            raise ValueError("Filepath %s does not exist" % outpath)

        self.path = self.normalizePath(filepath)
        self.outputPath = self.normalizePath(outpath)

        self.dateFormat = "%m/%d/%Y"
        self.timeFormat = "%H:%I:%S"
        self.dateTimeFormat = self.dateFormat + " " + self.timeFormat

        # Firefox uses profiles, and they're set in ~/.mozilla/firefox/profiles.ini
        self.profiles = self.getProfiles()
        # This is used in the path for the databases...
        self.activeProfile = ''

        self.databases = self.getDatabases()
        self.history = {}
        self.domains = []

    def getProfiles(self):
        profiles = []

        cfgfile = self.path + 'profiles.ini'
        if os.path.exists(cfgfile):
            cfg = SafeConfigParser()
            cfg.read(cfgfile)
            for section in cfg.sections():
                if section.lower() == 'general':
                    continue
                try:
                    path = cfg.get(section, 'Path')
                    profiles.append(path)
                except:
                    pass
        return profiles

    def getDatabases(self):
        return ['addons.sqlite', 'content-prefs.sqlite', 'cookies.sqlite','downloads.sqlite', 'extensions.sqlite', 'formhistory.sqlite', 'healthreport.sqlite'
                'permissions.sqlite','places.sqlite','signons.sqlite','webappsstore.sqlite']

    def getDB(self, db_name):
        if not self.activeProfile:
            raise ValueError("Set an active profile.")

        if db_name not in self.databases:
            raise ValueError("Unknown database %s" % db_name)

        try:
            shutil.copyfile(self.path + self.activeProfile + '/' + db_name, self.path + self.activeProfile + '/temp.db')
            return sqlite3.connect(self.path + self.activeProfile + '/temp.db')
        except:
            raise IOError("Could not copy live database. Are you root?")
        return False

        
    def out(self, msg):
        pass
    def getWebHistory(self):
        db = self.getDB('places.sqlite')
        c = db.cursor()
        for row in c.execute('SELECT id, url, title, visit_count, hidden, typed, frecency, last_visit_date, guid FROM moz_places'):
            pass

    def getBookmarks(self):
        db = self.getDB('places.sqlite')
        c = db.cursor()
        for row in c.execute('SELECT id, type, fk, parent, position, title, keyword_id, folder_type, dateAdded, lastModified, guid FROM moz_bookmarks'):
            pass

    def getDownloadHistory(self):
        db = self.getDB('downloads.sqlite')
        c = db.cursor()
        for row in c.execute(('SELECT name, source, target, tempPath, startTime, endTime, state, referrer, entityID, currBytes, maxBytes '
                              'mimeType, preferredApplication, preferredAction, autoResume, guid FROM moz_downloads')):
            pass

    def getSearchTerms(self):
        pass
    def getAutofillProfiles(self):
        db = self.getDB('signons.sqlite')
        c = db.cursor()
        for row in c.execute(('SELECT id, hostname, httpRealm, formSubmitURL, usernameField, passwordField, encryptedUsername, encryptedPassword, guid, '
                              'encType, timeCreated, timeLastUsed, timePasswordChanged, timesUsed FROM moz_logins')):
            pass
        for row in c.execute('SELECT hostname FROM moz_disabledHosts'):
            # "Never remember password for this site"
            pass
        # for row in c.execute('SELECT id, guid, timeDeleted FROM moz_deleted_logins'):

    def getCookies(self):
        pass

