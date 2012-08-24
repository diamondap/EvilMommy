import unittest
import EvilMommy.Config, time
from test.unit import TestHelper, TestLinksysParser, TestWirelessAccessManager, TestSecurity
from EvilMommy.WirelessAccessManager import WirelessAccessManager

def run():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(TestLinksysParser)
    suite.addTests(loader.loadTestsFromModule(TestWirelessAccessManager))
    suite.addTests(loader.loadTestsFromModule(TestSecurity))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

def integration_test():
    """
    These only run manually, if you uncomment the last line of this file.
    """

    mgr = WirelessAccessManager(EvilMommy.Config)

    # Get the blacklist, add a MAC address to it, then get the list
    # again to see if it was really added.
    print mgr.get_blacklist()
    print "Adding '00:55:55:55:55:55' to the blacklist"
    mgr.add_to_blacklist('00:55:55:55:55:55')
    print mgr.get_blacklist()

    # Now remove the MAC address and see if it really worked.
    print "Removing '00:55:55:55:55:55' from the blacklist"
    mgr.remove_from_blacklist('00:55:55:55:55:55')
    print mgr.get_blacklist()


    

if __name__ == "__main__":
    run()
#    integration_test()
