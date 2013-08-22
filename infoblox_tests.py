"""
Infoblox Tests

"""
import mock
import requests
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import infoblox


class InfobloxTest(unittest.TestCase):

    HOST = '127.0.0.1'

    def setUp(self):
        self.infoblox = infoblox.Infoblox(self.HOST)
        self.url = 'https://%s/wapi/v1.0/' % self.HOST

    def test_infoblox_url(self):
        self.assertEqual(self.url, self.infoblox.url)

    def test_default_auth(self):
        self.assertEqual(('admin', 'infoblox'), self.infoblox.auth)

    """
    @mock.patch.object(requests, 'delete')
    def test_private_delete(self, delete):
        reference = '_abc123'
        url = self.url + reference
        self.infoblox._delete(reference)
        delete.assert_called_with(url)
    """
