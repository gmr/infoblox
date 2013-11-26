"""The Infoblox Session object is responsible for coordinating communication
with the Infoblox NIOS device.

"""
import json
import logging
import requests
import urllib
import urlparse

LOGGER = logging.getLogger(__name__)

USERNAME = 'admin'
PASSWORD = 'infoblox'


class Session(object):
    """Central object for managing HTTP requests to the Infoblox appliance."""
    BASE_PATH = '/wapi/v1.2'
    HEADERS = {'Content-type': 'application/json'}

    def __init__(self, host, username=None, password=None, https=True):
        """Create a new instance of the Infoblox Session object

        :param str host: The Infoblox host to communicate with
        :param str username: The user to authenticate with
        :param str password: The password to authenticate with

        """
        self.auth = (username or USERNAME, password or PASSWORD)
        self.host = host
        self.scheme = 'https' if https else 'http'
        self.session = requests.session()

    def _request_url(self, path, query=None):
        return urlparse.urlunparse((self.scheme,
                                    self.host,
                                    '/'.join([self.BASE_PATH, path]),
                                    None,
                                    urllib.urlencode(query) if query else None,
                                    None))

    def delete(self, path):
        """Call the Infoblox device to delete the ref

        :param str ref: The reference id
        :rtype: requests.Response

        """
        return self.session.delete(self._request_url(path),
                                   auth=self.auth, verify=False)

    def get(self, path, data=None, return_fields=None):
        """Call the Infoblox device to get the obj for the data passed in

        :param str obj_reference: The object reference data
        :param dict data: The data for the get request
        :rtype: requests.Response

        """
        return self.session.get(self._request_url(path, return_fields),
                                data=json.dumps(data),
                                auth=self.auth, verify=False)

    def post(self, path, data):
        """Call the Infoblox device to post the obj for the data passed in

        :param str obj: The object type
        :param dict data: The data for the post
        :rtype: requests.Response

        """
        LOGGER.debug('Posting data: %r', data)
        return self.session.post(self._request_url(path),
                                 data=json.dumps(data or {}),
                                 headers=self.HEADERS, auth=self.auth,
                                 verify=False)

    def put(self, path, data):
        """Call the Infoblox device to post the obj for the data passed in

        :param str obj: The object type
        :param dict data: The data for the post
        :rtype: requests.Response

        """
        LOGGER.debug('Putting data: %r', data)
        return self.session.put(self._request_url(path),
                                data=json.dumps(data or {}),
                                headers=self.HEADERS, auth=self.auth,
                                verify=False)
