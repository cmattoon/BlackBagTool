class Browser:
    def __init__(self):
        self.domains = []
        pass

    def normalizePath(self, path):
        if path[-1] == "/":
            return path
        else:
            return path + "/"
        
    def addURL(self, url):
        if 'image/jpeg;base64' in url: # Fuck b64 data, it's not even a URL... @todo - why is it showing up here?
            return None
        from urlparse import urlparse

        if '.' in url and url.index('.') == 0:
            # Some cookies will be passed in as ".sitename.com"
            url = url[1:]
        parts = urlparse(url)

        if parts.netloc:
            result = parts.netloc
        elif parts.path:
            result = parts.path # Add the path
        else:
            # Not sure what this is...
            return False

        if 'www.' in result and result.index('www.') == 0: 
            result = result[4:]

        if result not in self.domains:
            self.domains.append(result)
            """
            @todo - 
            Turn this into a dict, {'domain_as_key' : int(visits)}
            Add a method to print this nicely (or export to CSV)
            """
            return True
        else:
            return None # Nothing was added because it already exists

                
        
