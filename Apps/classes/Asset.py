"""
This class represents an item in the users history.
Since browsers store different data, type None should be used for all defaults, meaning "No information"
"""
import re, datetime, time

class Asset:
    def __init__(self):
        self.timeFormat = '%H:%I:%S'
        self.dateFormat = '%a, %b %d %Y'
        self.datetimeFormat = self.dateFormat + ' ' + self.timeFormat

        
    def set(self, prop, val):
        try:
            # Check the title for interesting stuff when it's set
            if prop == 'title':
                data = self.parseTitle(val)
                if data:
                    self.notes.append("Found in Title: %s" % data)

            setattr(self, prop, val)
            return True
        except:
            return False

    # This function looks for interesting things in the title of a website, like email addresses.
    # Okay, so it really only looks for email addresses in the title right now. But it's a start.
    def parseTitle(self, title_text):
        if '@' in title_text:
            # Check for a valid email address. This could also be a twitter user, or anything else.
            matches = re.search(r'[\w\.-]+@[\w\.-]+', title_text)
            if matches:
                return match.group(0)
        return False

        
    def fill(self, value, default='No data'):
        if value == None or value == '':
            return default
        return value

    def formatTimestamp(self, ts, is_webkit_time=False):
        webkit_offset = 11644473600 # Webkit uses Epoch date of 1601, not 1970 
        ts = int(ts)
        if ts == 0:
            return "No Data"
        if ts - webkit_offset > 0:
            ts = int(float(ts) / 1000000) - webkit_offset
        #return datetime.datetime.strptime(str(ts), self.datetimeFormat)
        return time.strftime(self.datetimeFormat, time.localtime(ts))
            
