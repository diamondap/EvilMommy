import re
from datetime import datetime

class LinksysParser:
    """
    This class parses the HTML returned by the Linksys EA3500 router's
    web-based management UI. The HTML is peppered with JavaScript calls
    to document.write, and so is not parsable with a standard HTML parser.
    """

    def parse_mac_blacklist(self, html):
        """
        Parses the HTML from the router's MAC Address Filter
        page and returns a list of MAC addresses currently on
        the blocked list.
        """
        # The easiest way to parse the addresses on the MAC blacklist
        # is to pull them out of the diagnostic output that the router
        # puts in plain text at the top of the page. Otherwise, we have
        # to parse it from the JavaScript, which is quite messy on this
        # page. The entries look like this:
        #
        # //			1. 22:22:22:22:22:22
        # //			2. 00:33:33:33:33:33
        mac_addrs = []
        for m in re.finditer(r'//\s+\d+\. (\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)', 
                             html):
            mac_addrs.append(m.group(1))
        return mac_addrs

    def parse_dhcp_clients(self, html):
        """
        Parses the HTML from the router's DHCP clients
        page and returns a list of clients currently that have a 
        leased DHCP address. The returned list contains dictionaries
        with these entries:

        hostname:       Hostname of the machine holding the lease
        ip_address:     IP address assigned to the machine
        mac_address:    The client machine's MAC address
        interface:      WLAN for wireless, LAN for wired
        lease_expires:  Time today when the client's DHCP lease expires
        """ 
        clients = []
        # DHCP client entries appear in JavaScript like this:
        # new AAA('Wii','192.168.1.108','00:23:31:6b:a9:89','23:53:37','WLAN')
        # Let's extract what's inside the parens.
        for m in re.finditer(r'AAA\((.*)\);', html):
            client = m.group(1).replace("'", "").split(",")
            
            # Skip dummy entries
            if client[0] == "wlanadv.none":
                continue 

            clients.append({ 'hostname': client[0],
                             'ip_address': client[1],
                             'mac_address': client[2],
                             'interface': client[4],
                             'lease_expires': client[3] })
        return clients

    # No longer in use
    def parse_time(self, time_str):
        """
        Given a string in hh:mm:ss format, returns a datetime object
        representing that time on today's date.
        """
        time = time_str.split(":")
        return datetime.now().replace(hour = int(time[0], 10), 
                                      minute = int(time[1], 10),
                                      second = int(time[2], 10))
