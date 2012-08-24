#!/usr/bin/python
import urllib2
from CustomHttpClient import CustomHttpClient

router_url = "https://192.168.1.1"
router_user = "admin"
router_password = "ballard66"

dhcp_url = "https://192.168.1.1/DHCPTable.asp"
netbook_name = "zelda"
pc_name = "AsusPC"

mac_filter_url = "https://192.168.1.1/Wireless_MAC.asp"
apply_changes_url = "https://192.168.1.1/apply.cgi"


http_client = CustomHttpClient(router_url, router_user, router_password)
response = http_client.open(router_url)

login_status = response.getcode()
if login_status == 200:
    #dhcp_response = urllib2.urlopen(dhcp_url)
    dhcp_response = http_client.open(dhcp_url)
    print dhcp_response.read()

# print response.read()

