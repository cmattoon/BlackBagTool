"""
This class represents an item in the users history.
Since browsers store different data, type None should be used for all defaults, meaning "No information"
"""
import re
from Asset import Asset

class WebHistory(Asset):
    def __init__(self):
        # A unique ID, probably from the database. Useful for linking URLS together by referrer
        self.id = None
        # The actual request URI that was entered or clicked. <http://www.google.com/?q=some+search+term>
        self.requestURI = None
        # The domain. Comes from the netloc field of urlparse
        self.domain = None
        # The title of the site, commonly shown in the window (html <title/> tag)
        self.title = None
        # Number of visits to this domain.
        self.visits = None
        # The number of times the user has typed this address into the address bar (as opposed to clicking a referring link)
        self.typed = None
        # The most recent visit to the site, in seconds (Epoch)
        self.lastVisit = None
        # Whether or not the history item is hidden.
        self.hidden = None
        # Misc notes, conclusions, etc drawn from the data. These should be report-ready bullet items.
        self.notes = []
        
        Asset.__init__(self)

    def pretty(self, print_output=False):
        title = self.fill(self.title, '<< No Title >>')

        output = []
        output.append('[+] ' + title)
        if self.hidden:
            output.append('*** HIDDEN ***')

        output.append('    [%s]' % self.domain)
        output.append('    [%s]' % self.requestURI)
        output.append('    Visits: %d, Typed: %d' % (int(self.visits), int(self.typed)))
        output.append('    Last Visit: %s' % (self.formatTimestamp(self.lastVisit)))

        if len(self.notes):
            output.append('    Notes:')
            for note in self.notes:
                output.append('        [*] %s' % note)

        if print_output:
            for line in output:
                print line
            return True
        return "\n".join(output)
