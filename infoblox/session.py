"""The Infoblox Session object is responsible for coordinating communication
with the Infoblox NIOS device.

"""
import json
import logging
import requests

LOGGER = logging.getLogger(__name__)

USERNAME = 'admin'
PASSWORD = 'infoblox'


class Session(object):
    """Central object for managing HTTP requests to the Infoblox appliance."""
    HEADERS = {'Content-type': 'application/json'}

    def __init__(self, host, username=None, password=None):
        """Create a new instance of the Infoblox Session object

        :param str host: The Infoblox host to communicate with
        :param str username: The user to authenticate with
        :param str password: The password to authenticate with

        """
        self.auth = (username or USERNAME, password or PASSWORD)
        self.url = 'https://%s/wapi/v1.0/' % host
        self.session = requests.session()

    def delete(self, ref):
        """Call the Infoblox device to delete the ref

        :param str ref: The reference id
        :rtype: requests.Response

        """
        return self.session.delete(self.url + ref,
                                   auth=self.auth, verify=False)

    def get(self, obj, data=None):
        """Call the Infoblox device to get the obj for the data passed in

        :param str obj: The object type
        :param dict data: The data for the get request
        :rtype: requests.Response

        """
        return self.session.get(self.url + obj, data=json.dumps(data or {}),
                                auth=self.auth, verify=False)

    def post(self, obj, data):
        """Call the Infoblox device to post the obj for the data passed in

        :param str obj: The object type
        :param dict data: The data for the post
        :rtype: requests.Response

        """
        return self.session.post(self.url + obj, data=json.dumps(data),
                                 headers=self.HEADERS, auth=self.auth,
                                 verify=False)
