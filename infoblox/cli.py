"""
API and command line app for working with Infoblox NIOS

"""
import argparse
import logging
import sys

from infoblox import Host, Session

LOGGER = logging.getLogger(__name__)

__cli_description__ = 'Add or remove a host from the Infoblox appliance'
__version__ = '1.0.0'

USERNAME = 'admin'
PASSWORD = 'infoblox'
COMMENT = ('Added by the Python infoblox library at '
           'https://crate.io/packages/infoblox')


class InfobloxHost(object):
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

        self.session = Session(host, username, password)

    def delete_old_host(self, hostname):
        """Remove all records for the host.

        :param str hostname: Hostname to remove
        :rtype: bool

        """
        host = Host(self.session, name=hostname)
        return host.delete()

    def add_new_host(self, hostname, ipv4addr, comment=None):
        """Add or update a host in the infoblox, overwriting any IP address
        entries.

        :param str hostname: Hostname to add/set
        :param str ipv4addr: IP Address to add/set
        :param str comment: The comment for the record

        """
        host = Host(self.session, name=hostname)
        if host.ipv4addrs:
            host.ipv4addrs = []
        host.add_ipv4addr(ipv4addr)
        host.comment = comment
        return host.save()


def main():
    parser = argparse.ArgumentParser(description=__cli_description__)
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + __version__)
    parser.add_argument('--debug',
                        action='store_true',
                        help='Enable debug output')
    parser.add_argument('infoblox',
                        metavar='<Infoblox Address>',
                        action='store',
                        help='The Infoblox hostname')
    parser.add_argument('-u', '--username',
                        default=USERNAME,
                        action='store',
                        help='The username to perform the work as. '
                             'Default: %s' % USERNAME)
    parser.add_argument('-p', '--password',
                        default=PASSWORD,
                        action='store',
                        help='The password to authenticate with. '
                             'Default: %s' % PASSWORD)
    parser.add_argument('action',
                        choices=['add', 'remove'],
                        help='Specify if you are adding or removing a host')
    parser.add_argument('host',
                        metavar='<FQDN>',
                        action='store',
                        help='The FQDN for the host')
    parser.add_argument('address',
                        metavar='[IPv4 Address]',
                        action='store',
                        help='The IPv4 address for the host')
    parser.add_argument('comment',
                        metavar='[COMMENT]',
                        default='',
                        action='store',
                        help='A comment set on the host when adding.')
    args = vars(parser.parse_args())
    if args['debug']:
        logging.basicConfig(level=logging.DEBUG)
    infoblox = InfobloxHost(args['infoblox'],
                            args['username'],
                            args['password'])
    if args['action'] == 'add':
        if infoblox.add_new_host(args['host'], args['address'],
                                 args['comment']):
            sys.stdout.write('Host added\n')
        else:  # Exit with an error status
            sys.exit(1)
    elif args['action'] == 'remove':
        if infoblox.delete_old_host(args['host']):
            sys.stdout.write('Host removed\n')
        else:  # Exit with an error status
            sys.exit(1)


if __name__ == '__main__':
    main()
