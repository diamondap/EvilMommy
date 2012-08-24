import urllib, urllib2

class CustomHttpClient:
    
    default_headers = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.79 Safari/537.1",
                        }

    def __init__(self, base_url, user, password):
        """
        Creates a new HTTP client that knows how to respond to
        401 (authorization required) responses, and knows how to
        send the HTTP Basic Authentication headers required by
        Linksys routers.

        base_url is the url of the router's web-based admin page
        user is the user name required for HTTP Basic Auth
        password is the HTTP Basic Auth password
        """

        # We could install this opener globally using 
        # urllib2.install_opener, but I like to avoid doing things 
        # that affect any part of the global environment, unless it's 
        # necessary and the changes are easily visible.

        pwd_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        pwd_manager.add_password(None, base_url, user, password)
        auth_handler = urllib2.HTTPBasicAuthHandler(pwd_manager)
        self.opener = urllib2.build_opener(auth_handler)

    def open(self, url, data = None, headers = None):
        """
        Requests the specified URL, and returns a response object
        with methods get_code() and read(). If data is None, this
        executes a GET request. Otherwise, it does a POST.
        """
        encoded_data = None
        all_headers = CustomHttpClient.default_headers
        if data is not None:
            encoded_data = urllib.urlencode(data)
        if headers is not None:
            all_headers = dict(CustomHttpClient.default_headers.items() + 
                               headers.items())
        request = urllib2.Request(url, encoded_data, all_headers)
        return self.opener.open(request)



