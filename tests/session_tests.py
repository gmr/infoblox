"""
Infoblox Tests

"""
import httmock
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from infoblox import session


class SessionTests(unittest.TestCase):

    HOST = '127.0.0.1'

    def setUp(self):
        self.session = session.Session(self.HOST)

    def test_default_auth(self):
        self.assertEqual(('admin', 'infoblox'), self.session.auth)


class SessionDeleteTests(SessionTests):
    REF = ('record:host/ZG5zLmhvc3QkLl9kZWZhdWx0LmNvbS5tdG1ldGVzdC5zY3Mub'
           'GRhcHM:ldaps.localhost/default')

    @httmock.all_requests
    def delete_mock(self, url, request):
        return {'content': self.REF,
                'status_code': 200,
                'elapsed': 5}

    def test_delete(self):
        with httmock.HTTMock(self.delete_mock):
            response = self.session.delete(self.REF)
            self.assertEqual(self.REF, response.content)


class SessionGetTests(SessionTests):

    def setUp(self):
        super(SessionGetTests, self).setUp()
        self.content = {'name': 'foo', 'ipv4addr': '127.0.0.1'}

    @httmock.all_requests
    def get_mock(self, url, request):
        return {'content': self.content,
                'headers': {'content-type': 'application/json'},
                'status_code': 200,
                'elapsed': 5}

    def test_get(self):
        with httmock.HTTMock(self.get_mock):
            response = self.session.get('objname', {'name': 'foo'})
            self.assertEqual(self.content, response.json())
