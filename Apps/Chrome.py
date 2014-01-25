from Browser import Browser
from classes.WebHistory import WebHistory
from classes.Download import Download
from classes.Cookie import Cookie
from urlparse import urlparse
import os, shutil, sqlite3

class Chrome(Browser):
    def __init__(self, filepath, outpath):
        if not os.path.exists(filepath):
            raise ValueError("Path %s not found" % filepath)
        if not os.path.exists(outpath):
            try:
                os.mkdirs(outpath)
            except:
                pass
        if not os.path.exists(outpath):
            raise ValueError("Path %s not found" % outpath)

        self.path = filepath
        self.outputPath = outpath
        self.dateFormat = '%m/%d/%Y'
        self.timeFormat = '%H:%I:%S'
        self.dateTimeFormat = self.dateFormat + " " + self.timeFormat
        self.databases = self.getDatabases()
        self.history = {}
        self.domains = []

    def getDatabases(self):
        # Could read from config here, or something more intelligent, like search for what's available.
        # There should be a check somewhere to make sure the DB file exists.
        self.databases = ['Archived History', 'Bookmarks', 'Cookies', 'Current Session', 'Current Tabs', 'Extension Cookies', 'Favicons', 'History', 'History Provider Cache', 'Last Session', 'Last Tabs', 'Login Data', 'Network Action Predictor', 'Origin Bound Certs', 'Preferences', 'Quota Manager', 'Shortcuts', 'Top Sites', 'TransportSecurity', 'Visited Links', 'Web Data']
        return self.databases

    def getDB(self, db_name):
        # Definitely not good for forensics, but useful for reading data while DB is locked (e.g., Chrome is in use)
        if db_name not in self.databases:
            print ""
            print self.databases
            print ""
            raise ValueError("Unknown database %s" % db_name)
        try:
            shutil.copyfile(self.path + 'Default/' + db_name, self.path + 'Default/temp.db')
            return sqlite3.connect(self.path + 'Default/temp.db')
        except:
            raise IOError("Could not copy live database. Are you root?")
        return False
    
    def out(self, message):
        print message
        
    def getWebHistory(self):
        db = self.getDB('History')
        c = db.cursor()
        history = []

        for row in c.execute('SELECT id, url, title, visit_count, typed_count, last_visit_time, hidden FROM urls'):
            h = WebHistory()
            h.id = int(row[0])
            h.requestURI = row[1].encode('UTF-8')
            h.domain = urlparse(h.requestURI).netloc
            h.title = row[2].encode('UTF-8')
            h.visits = int(row[3])
            h.typed = int(row[4])
            h.lastVisit = int(row[5])
            h.hidden = bool(row[6])
            self.addURL(h.requestURI)
            history.append(h)

        self.history['web'] = history
        return history

    def getDownloadHistory(self):
        db = self.getDB('History')
        c = db.cursor()
        downloads = []
        for row in c.execute('SELECT id, current_path, target_path, start_time, opened, referrer, etag, last_modified, received_bytes, total_bytes, interrupt_reason, danger_type, by_ext_id, by_ext_name FROM downloads'):
            d = Download()
            # Current path is empty if download is in progress
            d.filePath = row[2].encode('UTF-8')
            d.startTime = int(row[3])
            d.opened = bool(row[4])
            d.URI = row[5].encode('UTF-8')
            d.lastModified = str(row[7])
            d.downloadedBytes = int(row[8])
            d.totalBytes = int(row[9])
            d.interruptReason = int(row[10])
            d.dangerType = int(row[11])
            d.byExtId = str(row[12])
            d.byExtName = str(row[13])
            self.addURL(d.URI)
            downloads.append(d)

        self.history['downloads'] = downloads
        return downloads

    def getSearchTerms(self):
        db = self.getDB('History')
        c = db.cursor()
        keywords = []
        for row in c.execute('SELECT keyword_id, url_id, term, lower_term FROM keyword_search_terms'):
            keywords.append(row[3].encode('UTF-8')) ## Finish this!

        self.history['keywords'] = keywords
        return keywords

    def getAutofillProfiles(self):
        db = self.getDB('Web Data')
        c = db.cursor()
        profiles = []
        for row in c.execute(('SELECT ap.guid, ap.company_name, ap.address_line_1, ap.address_line_2, ap.city, '
                              'ap.state, ap.zipcode, ap.country, ap.country_code, ap.date_modified, ap.origin, '
                              'apn.first_name, apn.middle_name, apn.last_name, ape.email, app.type, app.number '
                              'FROM autofill_profiles ap ' 
                              '    JOIN autofill_profile_names apn'
                              '    ON ap.guid = apn.guid'
                              '        JOIN autofill_profile_emails ape'
                              '        ON ap.guid = ape.guid'
                              '            JOIN autofill_profile_phones app'
                              '            ON ap.guid = app.guid')):
            #######################################################:
            # Build profile here...
            pass
        return profiles

    def getCookies(self):
        db = self.getDB('Cookies')
        c = db.cursor()
        cookies = []
        for row in c.execute(('SELECT creation_utc, host_key, name, value, path, expires_utc, secure, httponly, last_access_utc, has_expires, persistent, priority '
                              'FROM cookies')):
            cookie = Cookie()
            cookie.creationTime = row[0]
            cookie.hostKey = row[1] # The url
            self.addURL(row[1])
            cookie.name = row[2].encode('UTF-8')
            cookie.value = row[3].encode('UTF-8')
            cookie.path = row[4].encode('UTF-8')
            cookie.expireTime = int(row[5])
            cookie.secure = bool(row[6])
            cookie.httpOnly = bool(row[7])
            cookie.lastAccessed = int(row[8])
            cookie.hasExpires = bool(row[9])
            cookie.persistent = bool(row[10])
            cookie.priority = int(row[11])
            cookies.append(cookie)
        self.history['cookies'] = cookies
        return cookies
