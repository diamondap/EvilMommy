from LinksysParser import LinksysParser
from CustomHttpClient import CustomHttpClient

class WirelessAccessManager:

    def __init__(self, config):
        self.parser = LinksysParser()
        self.config = config
        self.http_client = CustomHttpClient(config.router_url,
                                            config.router_user, 
                                            config.router_password)

    def get_blacklist(self):
        """
        Returns the MAC addresses on the router's blacklist. MAC 
        addresses on the blacklist cannot connect to the wireless network.
        """
        response = self.http_client.open(self.config.mac_filter_url)
        return self.parser.parse_mac_blacklist(response.read())


    def add_to_blacklist(self, mac_address):
        """
        Adds the specified MAC address to the router's blacklist. The
        device with the specified MAC address will not be allowed to 
        connect.
        """
        current_blacklist = self.get_blacklist()
        post_data = self.build_blacklist_add_request(current_blacklist,
                                                     mac_address)
        response = self.http_client.open(self.config.apply_changes_url, 
                                         post_data)

        # We don't really care about the body of the response, but
        # but if we issue another request to the router before the
        # entire body of this response has come through, the changes
        # will not be applied. So force a read here to block our app
        # from making more requests until this page is done. This
        # page is slow: up to 12 seconds.
        response.read()

        return response.getcode() == 200
                              

    def remove_from_blacklist(self, mac_address):
        """
        Removes the specified MAC address from the router's blacklist.
        """
        current_blacklist = self.get_blacklist()
        post_data = self.build_blacklist_remove_request(current_blacklist,
                                                        mac_address)
        response = self.http_client.open(self.config.apply_changes_url, 
                                         post_data)

        # See the note above in add_to_blocklist for why we read the response
        response.read()

        return response.getcode() == 200


    def blacklist_post_data(self):
        """
        Returns the dictionary of basic data we need to post to the
        router for adding or removing MAC addresses from the blacklist.
        """
        post_data = { 'submit_button': 'Wireless_MAC',
                      'change_action': '',
                      'action':        'Apply',
                      'wl_macmode':    'deny',
                      'wl_macmode1':   'deny',
                      'wl_maclist':    '32',
                      'wait_time':     '3',
                      'wl_mac_filter': '1',
                      'start':         '',
                      'end':           '' }

        # Pad out the request with empty MAC addresses. The router
        # seems to want 32 of these addresses with names m0 - m32.
        for i in range(32):
            post_data['m' + str(i)] = '00:00:00:00:00:00'
            
        return post_data


    def build_blacklist_add_request(self, current_blacklist, mac_address):
        """
        Creates the data for the POST request to add a new MAC address
        to the blacklist. Param current_blacklist is a list of MAC addresses
        (strings) currently on the blacklist. Param mac_address is the
        address to add.
        """
        if not mac_address in current_blacklist:
            current_blacklist.append(mac_address)

        post_data = self.blacklist_post_data()

        # Make sure we send back the existing blacklist, plus
        # our new MAC address.
        for index, value in enumerate(current_blacklist):
            post_data['m' + str(index)] = value

        return post_data


    def build_blacklist_remove_request(self, current_blacklist, mac_address):
        """
        Creates the data for the POST request to remove a MAC address
        from the blacklist. Param current_blacklist is a list of MAC addresses
        (strings) currently on the blacklist. Param mac_address is the
        address to remove.
        """
        if mac_address in current_blacklist:
            current_blacklist.remove(mac_address)

        post_data = self.blacklist_post_data()

        # Make sure all blacklisted MACs go back to the server
        # (except the one we want to remove).
        for index, value in enumerate(current_blacklist):
            post_data['m' + str(index)] = value

        return post_data



    def get_dhcp_clients_table(self):
        """
        Returns a list of hashes with info about all of the DHCP clients
        attached to the router, both wired and wireless. Each hash has the
        following keys:

        hostname:       Hostname of the machine holding the lease        
        ip_address:     IP address assigned to the machine
        mac_address:    The client machine's MAC address
        interface:      WLAN for wireless, LAN for wired
        lease_expires:  Time today when the client's DHCP lease expires
        friendly_name:  The friendly name of the client, if one is specified
                        in the config file. Otherwise, the client name
        """
        response = self.http_client.open(self.config.dhcp_url)
        clients = self.parser.parse_dhcp_clients(response.read())
        for c in clients:
            if c['hostname'] in self.config.machines:
                c['friendly_name'] = self.config.machines[c['friendly_name']]
            else:
                c['friendly_name'] = c['hostname']
        return clients

    def remove_from_dhcp_clients_table(self, ip_address):
        """
        Removes the specified ip_address from the router's DHCP clients
        table. This causes the device to lose its connection. Returns
        true if the call success, false if not.
        """
        post_data = {'submit_button': 'DHCPTable',
                     'change_action': 'gozila_cgi',
                     'submit_type':   'delete_single',
                     'small_screen':  '',
                     'ip':            ip_address,
                     'sortby':        'ip'}
        response = self.http_client.open(self.config.apply_changes_url,
                                         post_data)
        return response.getcode() == 200

