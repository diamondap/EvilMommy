import unittest
from TestHelper import TestHelper
from EvilMommy.Security import Security
from EvilMommy import Config

class TestSecurity(unittest.TestCase):

    def setUp(self):
        self.security = Security(Config.encryption_key)

    def sample_token(self):
        return self.security.create_auth_token('Homer', '127.0.0.1')

    def test_create_auth_token(self):
        token = self.sample_token()
        self.assertTrue(isinstance(token, basestring))
        token2 = self.security.create_auth_token('Homer', '127.0.0.1')
        self.assertFalse(token == token2)

    def test_unpack_auth_token(self):
        token = self.sample_token()
        data = self.security.unpack_auth_token(token)
        self.assertEqual('Homer', data['user_name']);
        self.assertEqual('127.0.0.1', data['remote_addr']);
        self.assertIsNone(self.security.unpack_auth_token('BadAuthToken'))

    def test_is_valid_user(self):
        token = self.sample_token()

        # Valid user and address
        self.assertTrue(self.security.is_valid_user(token, 
                                                    ['Homer', 'Moe'], 
                                                    '127.0.0.1'))
        # User not in user list
        self.assertFalse(self.security.is_valid_user(token, 
                                                     ['Marge', 'Lisa'], 
                                                     '127.0.0.1'))
        # Remote address does not match token
        self.assertFalse(self.security.is_valid_user(token, 
                                                    ['Homer', 'Moe'], 
                                                     '10.10.10.10'))
        # Bad token
        self.assertFalse(self.security.is_valid_user('Bad Token', 
                                                     ['Homer', 'Moe'], 
                                                     '127.0.0.1'))
