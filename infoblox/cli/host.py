"""
API and command line app for working with Infoblox NIOS

"""
import argparse
import requests
import json
import logging
import sys

LOGGER = logging.getLogger(__name__)

__cli_description__ = 'Add or remove a host from the Infoblox appliance'
__version__ = '1.0.0'

USERNAME = 'admin'
PASSWORD = 'infoblox'
COMMENT = 'Created by python with love'


class Infoblox(object):
    """The Infoblox class is an interface for interfacing with the Infoblox
    appliance and contains pre-defined functionality for adding and removing
    hosts and the relevant records for those hosts.

    """
    HEADERS = {'Content-type': 'application/json'}

    def __init__(self, host, username=None, password=None):
        """Create a new instance of the Infoblox class

        :param str host: The Infoblox host to communicate with
        :param str username: The user to authenticate with
        :param str password: The password to authenticate with

        """
        self.auth = (username or USERNAME, password or PASSWORD)
        self.url = 'https://%s/wapi/v1.0/' % host
        self.session = requests.session()

    def _delete(self, ref):
        """Call the Infoblox device to delete the ref

        :param str ref: The reference id
        :rtype: requests.Response

        """
        return self.session.delete(self.url + ref,
                                   auth=self.auth, verify=False)

    def _get(self, obj, data=None):
        """Call the Infoblox device to get the obj for the data passed in

        :param str obj: The object type
        :param dict data: The data for the get request
        :rtype: requests.Response

        """
        return self.session.get(self.url + obj, data=json.dumps(data or {}),
                                auth=self.auth, verify=False)

    def _post(self, obj, data):
        """Call the Infoblox device to post the obj for the data passed in

        :param str obj: The object type
        :param dict data: The data for the post
        :rtype: requests.Response

        """
        return self.session.post(self.url + obj, data=json.dumps(data),
                                 headers=self.HEADERS, auth=self.auth,
                                 verify=False)

    def create_host_record(self, hostname, ipv4addr, comment=None):
        """Create a host record for the given hostname, ip address and optional
        comment.

        :param str hostname: The hostname for the record
        :param str ipv4addr: The ip address for the record
        :param str comment: The comment for the record
        :rtype: bool

        """
        LOGGER.info('Creating host record for %s: %s', ipv4addr, hostname)
        response = self._post('record%3ahost',
                              {'ipv4addrs': [{'ipv4addr': ipv4addr}],
                              'name': hostname,
                              'comment': comment or self.comment})
        if response.status_code == 201:
            LOGGER.info('Ref: %s', response.json())
            return True
        LOGGER.error('Error creating host record: %s', response.content)
        return False

    def create_ptr_record(self, hostname, ipv4addr, comment=None):
        """Create a PTR record for the given hostname, ip address and optional
        comment.

        :param str hostname: The hostname for the record
        :param str ipv4addr: The ip address for the record
        :param str comment: The comment for the record
        :rtype: bool

        """
        LOGGER.info('Creating PTR record for %s: %s', ipv4addr, hostname)
        response = self._post('record%3aptr',
                              {'ipv4addr': ipv4addr,
                               'ptrdname': hostname,
                               'name': hostname,
                               'comment': comment or self.comment})
        if response.status_code == 201:
            return True
        LOGGER.error('Error creating ptr record: %s', response.content)
        return False

    def delete_by_ref(self, ref):
        """Delete a record by reference.

        :param str ref: The object reference id
        :rtype: bool

        """
        response = self._delete(ref)
        import pprint
        pprint.pprint(response.status_code)
        pprint.pprint(response.json())

        if response.status_code == 200:
            return True
        LOGGER.error('Error deleting by reference: %s', response.content)
        return False


    def get_host_from_name(self, hostname):
        """Fetch a host record for a given hostname.

        :param str hostname: The hostname to look up
        :rtype: dict

        """
        response = self._get('record%3ahost', {'name': hostname})
        if response.status_code == 200:
            data = response.json()
            if len(data) == 1:
                return data[0]
            return data
        LOGGER.error('Error getting host from hostname: %s', response.content)
        return None

    def get_host_from_ipv4(self, ipv4addr):
        """Fetch a host record for a given IPv4 address.

        :param str ipv4addr: The address to lookup
        :rtype: dict

        """
        response = self._get('record%3ahost_ipv4addr', {'ipv4addr': ipv4addr})
        if response.status_code == 200:
            data = response.json()
            if len(data) == 1:
                return data[0]
            return data
        LOGGER.error('Error getting host from ipv4: %s', response.content)
        return None

    def get_host_ptr(self, hostname):
        """Fetch a PTR record for a given hostname.

        :param str hostname: The hostname to lookup
        :rtype: dict

        """
        response = self._get('record%3aptr?_return_fields%2B=ipv4addr',
                             {'ptrdname': hostname})
        if response.status_code == 200:
            data = response.json()
            if len(data) == 1:
                return data[0]
            return data
        LOGGER.error('Error getting ptr record from hostname: %s',
                     response.content)
        return None

    def get_ipv4_ptr(self, ipv4addr):
        """Fetch a PTR record for a given IPv4 address.

        :param str ipv4addr: The address to lookup
        :rtype: dict

        """
        response = self._get('record%3aptr?_return_fields%2B=ipv4addr',
                             {'ipv4addr': ipv4addr})
        if response.status_code == 200:
            data = response.json()
            if len(data) == 1:
                return data[0]
            return data
        LOGGER.error('Error getting ptr record from ipv4: %s', response.content)
        return None

    def _first_ipv4addr(self, host_record):
        """Return the first IP address for a host record.

        :param dict host_record: The host record to get the IP address from
        :rtype: str

        """
        return host_record['ipv4addrs'][0]['ipv4addr']

    def delete_old_host(self, hostname, ipaddress):
        """Remove all records for the host and ip address

        :param str hostname: Hostname to remove
        :param str ipaddress: IP Address to remove
        :rtype: bool

        """
        performed_delete = False

        # Search for a host record
        record = self.get_host_from_name(hostname)
        if record:
            LOGGER.info('Deleting host record for %s', hostname)
            if self.delete_by_ref(record['_ref']):
                performed_delete = True

        # Search for a PTR by host
        record = self.get_host_ptr(hostname)
        if record:
            LOGGER.info('Deleting host record for %s ptr', hostname)
            if self.delete_by_ref(record['_ref']):
                performed_delete = True

        # Search for a PTR by ipaddr
        record = self.get_ipv4_ptr(ipaddress)
        if record:
            LOGGER.info('Deleting ipaddr record for %s ptr', ipaddress)
            if self.delete_by_ref(record['_ref']):
                performed_delete = True
        return performed_delete

    def add_new_host(self, hostname, ipaddress, comment=None):
        """Add a new host to the infoblox, clearing out any previous conflicting
        entries for the same host and ip address for both host records and
        ptr records.

        :param str hostname: Hostname to add/set
        :param str ipaddress: IP Address to add/set
        :param str comment: The comment for the record

        """
        if not comment:
            comment = COMMENT

        # Check if it already exists
        host_record = self.get_host_from_name(hostname)
        if host_record:
            LOGGER.debug('Host %s has ip address %s',
                         hostname, self._first_ipv4addr(host_record))

        # Search for the ipaddr
        ipv4_record = self.get_host_from_ipv4(ipaddress)
        if ipv4_record:
            LOGGER.debug('IP address %s has host %s',
                         ipaddress, ipv4_record['host'])

        # Search for PTR records by host
        host_ptr = self.get_host_ptr(hostname)
        if host_ptr:
            LOGGER.debug('PTR for %s is %s',host_ptr['ipv4addr'], hostname)

        # Search for PTR records by IP addr
        ipv4_ptr = self.get_ipv4_ptr(ipaddress)
        if ipv4_ptr:
            LOGGER.debug('PTR for %s is %s', ipaddress, ipv4_ptr['ptrdname'])

        need_to_make_host = True
        if host_record:
            if not ipv4_record:
                LOGGER.info('Host has a record, but ipv4addr does not: %s, %s',
                            hostname, ipaddress)
                self.delete_by_ref(host_record['_ref'])
            else:
                LOGGER.info('Host and ipv4 have a record: %s, %s',
                            hostname, ipaddress)
                if self._first_ipv4addr(host_record) != ipv4_record['ipv4addr']:
                    LOGGER.info('Host ipv4 & ipv4 record dont match: %s, %s',
                                self._first_ipv4addr(host_record), ipaddress)
                    self.delete_by_ref(host_record['_ref'])
                    self.delete_by_ref(ipv4_record['_ref'])
                else:
                    need_to_make_host = False

        need_to_make_ptr = True
        if host_ptr:
            if host_ptr['ipv4addr'] != ipaddress:
                    LOGGER.info('ipv4 & ptr ipv4 record dont match: %s, %s',
                                hostname,  host_ptr['ipv4addr'])
                    self.delete_by_ref(host_ptr['_ref'])
            else:
                need_to_make_ptr = False

        if ipv4_ptr:
            if ipv4_ptr['ptrdname'] != hostname:
                LOGGER.info('hostname & ptr hostname record dont match: %s, %s',
                            ipaddress,  host_ptr['ipv4addr'])
                self.delete_by_ref(ipv4_ptr['_ref'])
            else:
                need_to_make_ptr = False

        LOGGER.debug('Need to create host: %s, ptr: %s',
                     need_to_make_host, need_to_make_ptr)
        created = False
        if need_to_make_host and self.create_host_record(hostname,
                                                         ipaddress,
                                                         comment):
            created = True
        if need_to_make_ptr and self.create_ptr_record(hostname,
                                                       ipaddress,
                                                       comment):
            created = True
        return created


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description=__cli_description__)
    parser.add_argument('action', choices=['add', 'remove'],
                        action='store',
                        help='The action to take for the host')

    parser.add_argument('-u', '--username', default=USERNAME, action='store',
                        help='The username to perform the work as. '
                             'Default: %s' % USERNAME)
    parser.add_argument('-p', '--password', default=PASSWORD, action='store',
                        help='The password to authenticate with. '
                             'Default: %s' % PASSWORD)
    parser.add_argument('-c', '--comment', default=COMMENT, action='store',
                        help='A comment to use when performing the action. '
                             'Default: %s' % COMMENT)
    parser.add_argument('infobox', action='store',
                        help='The Infoblox hostname')
    parser.add_argument('host', action='store',
                        help='The FQDN for the host')
    parser.add_argument('address', action='store',
                        help='The IPv4 address for the host')
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + __version__)
    args = parser.parse_args()

    infoblox = Infoblox(args.infobox, args.username, args.password)
    if args.action == 'add':
        if infoblox.add_new_host(args.host, args.address, args.comment):
            LOGGER.info('Records added')
        else:
            sys.exit(1)

    if args.action == 'remove':
        if infoblox.delete_old_host(args.host, args.address):
            LOGGER.info('Records removed')
        else:
            sys.exit(1)


if __name__ == '__main__':
    main()
__author__ = 'gmr'
