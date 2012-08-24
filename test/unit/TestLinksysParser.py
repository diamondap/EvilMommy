import unittest
from datetime import datetime
from TestHelper import TestHelper
from EvilMommy.LinksysParser import LinksysParser

class TestLinksysParser(unittest.TestCase):

    def setUp(self):
        self.parser = LinksysParser()
        self.helper = TestHelper()

    def test_parse_time(self):
        now = datetime.now()
        dt = self.parser.parse_time("12:10:42")
        self.assertEqual(now.year, dt.year)
        self.assertEqual(now.month, dt.month)
        self.assertEqual(now.day, dt.day)
        self.assertEqual(12, dt.hour)
        self.assertEqual(10, dt.minute)
        self.assertEqual(42, dt.second)
        
    def test_parse_dhcp_clients(self):
        clients = self.parser.parse_dhcp_clients(self.helper.dhcp_response())

        # Make sure we got all the records
        self.assertEqual(10, len(clients))

        # Spot check a single record to ensure all the fields are correct
        client = clients[0]
        self.assertEqual('LAN', client['interface'])
        self.assertEqual('zelda', client['hostname'])
        self.assertEqual('192.168.1.107', client['ip_address'])
        self.assertEqual('01:35:10', client['lease_expires'])
        self.assertEqual('00:15:af:e6:6b:da', client['mac_address'])

        
    def test_parse_mac_blacklist(self):
        mac_addrs = self.parser.parse_mac_blacklist(self.helper.mac_response())
        self.assertEqual(3, len(mac_addrs))
        self.assertEqual('22:22:22:22:22:22', mac_addrs[0])
        self.assertEqual('00:33:33:33:33:33', mac_addrs[1])
        self.assertEqual('00:44:44:44:44:44', mac_addrs[2])
