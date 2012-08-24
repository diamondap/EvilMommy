import os

class TestHelper:

    dhcp_file = "dhcp_table.html"
    mac_file  = "wireless_mac.html"

    def path(self):
        return os.path.abspath(__file__)

    def test_file_path(self, file_name):
        path = os.path.join(self.path(), "..", "..", "data", file_name)
        return os.path.abspath(path)

    def dhcp_response(self):
        """Returns the contents of the sample DHCP response."""
        html = ''
        with open(self.test_file_path(TestHelper.dhcp_file), 'r') as f:
            html = f.read()
        return html

    def mac_response(self):
        """Returns the contents of the sample MAC response."""
        html = ''
        with open(self.test_file_path(TestHelper.mac_file), 'r') as f:
            html = f.read()
        return html
        

if __name__ == "__main__":
    helper = TestHelper()
    print helper.dhcp_response()
    print helper.mac_response()
