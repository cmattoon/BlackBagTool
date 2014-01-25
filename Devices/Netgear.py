"""
Tested on:
    Netgear WGR614v9
"""
import urllib2, BeautifulSoup, re

class Netgear:
    def __init__(self, ip='192.168.1.1', port='8080',username='admin',password='password'):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.baseUrl = 'http://%s:%s/' % (self.ip, self.port)
        self.opener = None
        self.authHandler = None
        self.authenticate()

        self._rawActiveDevices = []

    def connect(self, max_tries=0):
        if not self.authHandler:
            print " [+] I have to build the opener and auth handler first..."
            try:
                self.authenticate()
                print "     [+] Done!"
            except:
                raise RuntimeError("Cannot authenticate")

        if max_tries == 0:
            while True:
                try:
                    self.establishConnection()
                    return
                except:
                    pass
        else:
            for i in range(max_tries):
                try:
                    self.establishConnection()
                    return
                except:
                    pass

    def establishConnection(self):
        # The actual code is here, so connect can accept max_tries easily
        print " [+] Opening Base URL..."
        self.opener.open(self.baseUrl)
        print "     [+] OK!"
        


    def authenticate(self, usr=None, pwd=None):
        if not usr:
            usr = self.username
        if not pwd:
            pwd = self.password

        if not usr and not pwd:
            raise ValueError("Invalid username/password")
        print " [+] Authenticating (User: %s)" % (usr)
        try:
            pwdmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
            pwdmgr.add_password(None, self.baseUrl, usr, pwd)
            self.authHandler = urllib2.HTTPBasicAuthHandler(pwdmgr)
            self.opener = urllib2.build_opener(self.authHandler)
            print " [+] Opening %s" % self.baseUrl
            self.opener.open(self.baseUrl)
            print "     [+] OK!"
            urllib2.install_opener(self.opener)
            return True
        except:
            raise RuntimeError("Error building authentication handler/opener")
        

    def getLog(self, log_path='FW_log.htm'):
        url = self.baseUrl + 'FW_log.htm'
        print " [+] Fetching access log from router at %s" % self.ip
        try:
            response = self.opener.open(url)
            print "     [+] OK!"
            data = response.read()
            return data
        except URLError as e:
            print "     [!] Error: %s" % e.reason
            return False

    def getDevices(self):
        url = self.baseUrl + 'DEV_device.htm' # Laundry
        html = self.opener.open(url).read()

        if html:
            soup = BeautifulSoup.BeautifulSoup(html)
            macs = []
            ips = []
            hosts = []
            i = 0
            for span in soup.table.table.findAll('span', {'class':'ttext'}):
                val = span.contents[0].encode('UTF-8')
                did_something = False
                try:
                    m = re.search('[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}', val, re.I).group()
                    macs.append(m)
                    did_something = True
                except AttributeError:
                    pass
                
                try: 
                    
                    m = re.search(r'[0-9]+(?:\.[0-9]+){3}', val, re.I).group()
                    ips.append(m)
                    did_something = True
                except AttributeError:
                    pass
                if not did_something:
                    hosts.append(val)
                    devices = []
            if len(macs) == len(ips) and len(macs) == len(hosts):
                for i in range(len(macs)):
                    devices.append({'mac': macs[i], 'ip' : ips[i], 'hostname':hosts[i]})
            return devices

    def unblockSites(self):
        inputs = {
            'skeyword': 'never',
            
            }

    def changePassword(self, passwd):
        inputs = {'sysOldPasswd': self.passwd, 'sysNewPasswd': passwd, 'sysConfirmPasswd': passwd, 'cfAlert_Apply': 'Apply'}#, 'Cancel': 'Cancel'}
        
        target = self.host + 'password.cgi'
        """
        @todo
            Make request and shit...
        """
        
    def remoteManagement(self, is_enabled, ip_start=None, ip_fin=None, port='8080'):
        
        fields = {
            'apply': 'Apply',
            'http_rmport': port,
            'local_ip_1': '', 
            'local_ip_2': '',
            'local_ip_3': '',
            'local_ip_4': '',
            'start_ip_1': '',
            'start_ip_2': '',
            'start_ip_3': '',
            'start_ip_4': '',
            'fin_ip_1': '',
            'fin_ip_2': '',
            'fin_ip_3': '',
            'fin_ip_4': ''
            }

        if not port:
            port = '8080'

        if ip_start and not ip_fin:
            access = 'ip_single'
        elif ip_start and ip_fin:
            access = 'ip_range'
        else:
            access = 'all'

        fields['rm_access'] = access

        if access != 'all':
            # Netgear only allows IPv4 fields,  so this will suffice
            # for now.
            if '.' in ip_start:
                ip1_1, ip1_2, ip1_3, ip1_4 = ip_start.split('.')
            if ip_fin and '.' in ip_fin:
                ip2_1, ip2_2, ip2_3, ip2_4 = ip_fin.split('.')
        #                raise ValueError("IP address must be in the format 0.0.0.0")
        

        if access == 'ip_single':
            key1 = 'local_ip_'
            key2 = ''
        elif access == 'ip_range':
            key1 = 'start_ip_'
            key2 = 'fin_ip_'
        else:
            key1 = ''
            key2 = ''

        if key1:
            fields[key1 + '1'] = ip1_1
            fields[key1 + '2'] = ip1_2
            fields[key1 + '3'] = ip1_3
            fields[key1 + '4'] = ip1_4
        if key2:
            fields[key2 + '1'] = ip2_1
            fields[key2 + '2'] = ip2_2
            fields[key2 + '3'] = ip2_3
            fields[key2 + '4'] = ip2_4            
        
        for k in fields:
            print "%s = %s" % (str(k), str(fields[k]))

    def forwardPort(self, ip, port):
        pass




    def close(self):
        # Need to implement it as with..as..
        url = self.baseUrl + 'LGO_logout.htm'
        self.opener.open(url).read()

