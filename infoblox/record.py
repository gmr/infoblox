"""
Base Record Object

"""
import logging

LOGGER = logging.getLogger(__name__)


class Record(object):
    """This object is extended by specific Infoblox record types

    """
    obj = 'record'

    def __init__(self, session, _ref=None, *args, **kwargs):
        """Create a new instance of the Record passing in the Infoblox
        session object and the ref for the record.

        """
        self._ref = _ref
        self.session = session
        self._raw = None
        if _ref and (not any(args) and not kwargs):
            self._raw = self._fetch(_ref)
            self._assign()

    def _assign(self):
        raise NotImplementedError

    def _fetch(self, ref):
        response = self.session.get(ref)
        if response.status_code == 200:
            return response.json()
        return {}


class Host(Record):

    obj = 'record:host'

    def __init__(self, session, _ref=None, name=None, ipv4addrs=None, view=None):
        """Create a new instance of the Host Record passing in the Infoblox
        session object and the ref for the record.

        """
        self.name = name
        self.view = view
        self.ipv4addrs = [HostIPv4(session, **addr)
                          for addr in ipv4addrs or list()]
        super(Host, self).__init__(session, _ref, name, ipv4addrs, view)

    def _assign(self):
        self.name = self._raw.get('name')
        self.view = self._raw.get('view')
        self.ipv4addrs = [HostIPv4(self.session, **addr)
                          for addr in self._raw.get('ipv4addrs')]

    def __repr__(self):
        return '<Host %s>' % self.name


class HostIPv4(Record):

    obj = 'record:host_ipv4'

    def __init__(self, session, _ref=None, configure_for_dhcp=None,
                 ipv4addr=None, host=None):
        """Create a new instance of the HostIPv4 Record passing in the Infoblox
        session object and the ref for the record.

        """
        self.configure_for_dhcp = configure_for_dhcp
        self.ipv4addr = str(ipv4addr)
        self.host = host
        super(HostIPv4, self).__init__(session, _ref,
                                       configure_for_dhcp, ipv4addr, host)

    def __repr__(self):
        return '<HostIPv4 %s (%s)>' % (self.host, self.ipv4addr)

    def _assign(self):
        self.configure_fo_dhcp = self._raw.get('configure_for_dhcp')
        self.ipv4addr = str(self._raw.get('ipv4addr'))
        self.host = self._raw.get('host')
