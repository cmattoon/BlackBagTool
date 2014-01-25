"""
This represents a file downloaded by a browser.

"""
import time
from Asset import Asset

class Download(Asset):
    def __init__(self):
        # The browser that this history was retrieved from 
        # @todo - Store more information about the browser (version, etc), or link it to an ID in the project
        # (to handle different versions of the same browser)
        self.browser = None

        # This is the file location on disk ('/home/user/Downloads/image.jpg')
        self.filePath = None

        # This is the file location on the internet ('http://www.example.com/image.jpg')
        self.URI = None

        # This is the number of bytes downloaded
        self.downloadedBytes = None

        # This is the reported download size
        self.totalBytes = None

        # This is the reported start time (from the browser)
        self.startTime = None

        # This is the reported end time (from the browser)
        self.endTime = None

        # Chrome reports if the user has opened the file or not (** Confirm if this is only if opened from within Chrome)
        self.opened = None

        # This is the state of the download, as reported by the browser
        self.state = None

        # Chrome reports an interrupt reason for downloads that aren't complete. See docs for details
        self.interruptReason = None

        # Chrome reports a danger type for some files. Default is zero
        self.dangerType = None

        # Whether or not the downloaded file still exists on the target system.
        # @todo - A separate module should check the filesystem to see if the file has been moved to another location
        self.exists = None
        
        # The time the file was last modified, in seconds. This may be the time the uploader modified the file. (could be prior to download)
        self.lastModified = None

        # This information is derived by analyzing the given data. It should be report-ready, bullet-point style stuff.
        self.notes = []

        # Chrome - The identifier for the extension that initiated this download, if this download was initiated by an extension.
        # Will not change once it is set.
        self.byExtId = None

        # Chrome - The localized name of the extension that initiated this download, if this download was initiated by an extension.
        # Will change if the extension changes its name or the user changes their locale.
        self.byExtName = None

        Asset.__init__(self)

    def pretty(self, print_output=False):
        output = []

        filepath = self.fill(self.filePath)
        uri = self.fill(self.URI)
        dl_bytes = self.fill(self.downloadedBytes, 0)
        total_bytes = self.fill(self.totalBytes, 0)
        state = self.resolveState(self.state)
        start_time = self.fill(self.startTime, 0)

        if start_time:
            start_time = self.formatTimestamp(start_time)
            
        if self.byExtName:
            self.notes.append('Download initiated by extension with name [%s]' % self.byExtName)
        if self.byExtId:
            self.notes.append('Download initiated by extension with id [%s]' % self.byExtId)

        output.append('[Download]: %s' % uri)
        if dl_bytes >= total_bytes:
            output.append('    [Completed] (%d bytes)' % total_bytes)
        else:
            percent_complete = '{:.2%}'.format(float(dl_bytes)/float(total_bytes))
            output.append('    [Incomplete] (%d of %d bytes = %s)' % (dl_bytes, total_bytes, percent_complete))

        output.append('    Download Source: [%s]' % uri)
        output.append('    Current Location: [%s]' % filepath)
        output.append('    State: %s' % state)

        if len(self.notes):
            output.append('    [+] Notes:')
            for note in self.notes:
                output.append('        [*] %s' % note)
        
        if print_output:
            for line in output:
                print line
            return True
        else:
            return "\n".join(output)
            
    def resolveState(self, state):
        # Chrome->in_progress = The download is currently receiving data from the server
        # Chrome->interrupted = An error broke the connection with the file host
        # Chrome->complete = The download completed successfully
        states = {'chrome' : ['in_progress','interrupted','complete']} 

        if state == None or state == False:
            return 'No data'
        if state == 2:
            return "interrupted"
        if state == 0:
            return "in_progress"
        
    # Chrome
    def resolveInterruptReason(self, reason):
        # SERVER_* = HTTP Errors
        # NETWORK_* = Network errors (duh)
        # FILE_* = Filesystem error
        # USER_* = Caused by user 40 = Cancelled
        reasons = ["FILE_FAILED", "FILE_ACCESS_DENIED", "FILE_NO_SPACE", "FILE_NAME_TOO_LONG", "FILE_TOO_LARGE",
                   "FILE_VIRUS_INFECTED", "FILE_TRANSIENT_ERROR", "FILE_BLOCKED", "FILE_SECURITY_CHECK_FAILED", 
                   "FILE_TOO_SHORT", "NETWORK_FAILED", "NETWORK_TIMEOUT", "NETWORK_DISCONNECTED", 
                   "NETWORK_SERVER_DOWN", "SERVER_FAILED", "SERVER_NO_RANGE", "SERVER_PRECONDITION", 
                   "SERVER_BAD_CONTENT", "USER_CANCELED", "USER_SHUTDOWN", "CRASH"]

    # Chrome
    def resolveDangerType(self, danger):
        types = [
            "file",      # download's filename is suspicious
            "url",       # download's URL is known to be malicious
            "content",   # downloaded file is known to be malicious
            "uncommon",  # download's URL is not commonly downloaded and could be dangerous
            "host",      # download came from a host known to distribute malicious binaries and is likely dangerous
            "unwanted",  # download is potentially unwanted or unsafe (e.g., it could make changes to browser/computer settings)
            "safe",      # download presents no known danger
            "accepted"   # user has accepted the dangerous download
            ]
