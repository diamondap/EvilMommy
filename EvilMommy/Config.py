# Config.py
#
# Configuration parameters for EvilMommy.
#

# --------------------------------------------------------------------------
# Set this to something secret. 
# --------------------------------------------------------------------------
encryption_key    = 'HyeSekurity!'
valid_users       = ['lindsay', 'matt-wt']


# --------------------------------------------------------------------------
# Where is the router?
# --------------------------------------------------------------------------
router_url        = "https://192.168.1.1"
dhcp_url          = router_url + "/DHCPTable.asp"
mac_filter_url    = router_url + "/Wireless_MAC.asp"
apply_changes_url = router_url + "/apply.cgi"

# --------------------------------------------------------------------------
# Credentials for logging into the router
# --------------------------------------------------------------------------
router_user       = "xxxxxx"
router_password   = "xxxxxx"


# --------------------------------------------------------------------------
# These are the machines we are interested in controlling.
# All of this information appears in the router's DHCP clients table,
# which is under Status > Local Network.
#  
# The friendly_name is what we want to show to our user.
# can_message and can_shutdown indicate whether the machine
# supports messaging and remote shutdown. The machine must
# have a web server running and the bad_baby.py cgi script 
# installed to support these features.
# --------------------------------------------------------------------------
machines = [{ 'hostname': 'AsusPC',
              'friendly_name': 'the windows laptop',
              'mac_address': '48:5d:60:96:c4:07',
              'can_message': True,
              'can_shutdown': True },
            { 'hostname': 'zelda',
              'friendly_name': 'the white netbook',
              'mac_address': '00:15:af:e6:6b:da',
              'can_message': False,
              'can_shutdown': False },
            { 'hostname': 'NP-12C1A6074266',
              'friendly_name': 'the roku',
              'mac_address': 'cc:6d:a0:0a:d3:75',
              'can_message': False,
              'can_shutdown': False },
            { 'hostname': 'Wii',
              'friendly_name': 'the wii',
              'mac_address': '00:23:31:6b:a9:89',
              'can_message': False,
              'can_shutdown': False } ]

            

