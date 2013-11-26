"""
Base Record Object

"""
import logging

from infoblox import exceptions
from infoblox import mapping

LOGGER = logging.getLogger(__name__)


class Record(mapping.Mapping):
    """This object is extended by specific Infoblox record types and implements
    the core API behavior of a record class. Attributes that map to other
    infoblox records will be instances of those record types.

    :param infoblox.Session session: The infoblox session object
    :param str reference_id: The infoblox _ref value for the record
    :param dict kwargs: Key-value pairs that when passed in, if the a key
        matches an attribute of the record, the value will be assigned.

    """
    view = 'default'

    _ref = None
    _repr_keys = ['_ref']
    _return_ignore = ['view']
    _save_ignore = []
    _search_by = []
    _session = None
    _supports = []
    _wapi_type = 'record'

    def __init__(self, session, reference_id=None, **kwargs):
        """Create a new instance of the Record passing in the Infoblox
        session object and the reference id for the record.

        """
        super(Record, self).__init__(**kwargs)
        self._session = session
        self._ref = reference_id
        self._search_values = self._build_search_values(kwargs)
        if self._ref or self._search_values:
            self.fetch()

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__,
                            ' '.join(['%s=%s' % (key, getattr(self, key))
                                      for key in self._repr_keys]))
    def delete(self):
        """Remove the item from the infoblox server.

        :rtype: bool
        :raises: AssertionError
        :raises: ValueError
        :raises: infoblox.exceptions.ProtocolError

        """
        if not self._ref:
            raise ValueError('Object has no reference id for deletion')
        if 'save' not in self._supports:
            raise AssertionError('Can not save this object type')
        response = self._session.delete(self._path)
        if response.status_code == 200:
            self._ref = None
            self.clear()
            return True
        try:
            error = response.json()
            raise exceptions.ProtocolError(error['text'])
        except ValueError:
            raise exceptions.ProtocolError(response.content)

    def fetch(self):
        """Attempt to fetch the object from the Infoblox device. If successful
        the object will be updated and the method will return True.

        :rtype: bool
        :raises: infoblox.exceptions.ProtocolError

        """
        LOGGER.debug('Fetching %s, %s', self._path, self._search_values)
        response = self._session.get(self._path, self._search_values,
                                     {'_return_fields': self._return_fields})
        if response.status_code == 200:
            values = response.json()
            self._assign(values)
            return bool(values)
        elif response.status_code >= 400:
            try:
                error = response.json()
                raise exceptions.ProtocolError(error['text'])
            except ValueError:
                raise exceptions.ProtocolError(response.content)
        return False

    def reference_id(self):
        """Return a read-only handle for the reference_id of this object.

        """
        return str(self._ref)

    def save(self):
        """Update the infoblox with new values for the specified object, or add
        the values if it's a new object all together.

        :raises: AssertionError
        :raises: infoblox.exceptions.ProtocolError

        """
        if 'save' not in self._supports:
            raise AssertionError('Can not save this object type')

        values = {}
        for key in [key for key in self.keys() if key not in self._save_ignore]:
            if not getattr(self, key) and getattr(self, key) != False:
                continue

            if isinstance(getattr(self, key, None), list):
                value = list()
                for item in getattr(self, key):
                    if isinstance(item, dict):
                        value.append(item)
                    elif hasattr(item, '_save_as'):
                        value.append(item._save_as())
                    elif hasattr(item, '_ref') and getattr(item, '_ref'):
                        value.append(getattr(item, '_ref'))
                    else:
                        LOGGER.warning('Cant assign %r', item)
                values[key] = value
            elif getattr(self, key, None):
                values[key] = getattr(self, key)
        if not self._ref:
            response = self._session.post(self._path, values)
        else:
            values['_ref'] = self._ref
            response = self._session.put(self._path, values)
        LOGGER.debug('Response: %r, %r', response.status_code, response.content)
        if 200 <= response.status_code <= 201:
            self.fetch()
            return True
        else:
            try:
                error = response.json()
                raise exceptions.ProtocolError(error['text'])
            except ValueError:
                raise exceptions.ProtocolError(response.content)

    def _assign(self, values):
        """Assign the values passed as either a dict or list to the object if
        the key for each value matches an available attribute on the object.

        :param dict values: The values to assign

        """
        LOGGER.debug('Assigning values: %r', values)
        if not values:
            return
        keys = self.keys()
        if not self._ref:
            keys.append('_ref')
        if isinstance(values, dict):
            for key in keys:
                if values.get(key):
                    if isinstance(values.get(key), list):
                        items = list()
                        for item in values[key]:
                            if isinstance(item, dict):
                                if '_ref' in item:
                                    obj_class = get_class(item['_ref'])
                                    if obj_class:
                                        items.append(obj_class(self._session,
                                                               **item))
                            else:
                                items.append(item)
                        setattr(self, key, items)
                    else:
                        setattr(self, key, values[key])
        elif isinstance(values, list):
            self._assign(values[0])
        else:
            LOGGER.critical('Unhandled return type: %r', values)

    def _build_search_values(self, kwargs):
        """Build the search criteria dictionary. It will first try and build
        the values from already set attributes on the object, falling back
        to the passed in kwargs.

        :param dict kwargs: Values to build the dict from
        :rtype: dict

        """
        criteria = {}
        for key in self._search_by:
            if getattr(self, key, None):
                criteria[key] = getattr(self, key)
            elif key in kwargs and kwargs.get(key):
                criteria[key] = kwargs.get(key)
        return criteria

    @property
    def _path(self):
        return self._ref if self._ref else self._wapi_type

    @property
    def _return_fields(self):
        return ','.join([key for key in self.keys()
                         if key not in self._return_ignore])


class Host(Record):
    """Implements the host record type.

    Example::

        session = infoblox.Session(infoblox_host,
                                   infoblox_user,
                                   infoblox_password)
        host = infoblox.Host(session, name='foo.bar.net')

    """
    aliases = []
    comment = None
    configure_for_dns = True
    disable = False
    dns_aliases = []
    dns_name = None
    extattrs = None
    ipv4addrs = []
    ipv6addrs = []
    name = None
    rrset_order = 'cyclic'
    ttl = None
    use_ttl = False
    zone = None

    _repr_keys = ['name', 'ipv4addrs', 'ipv6addrs']
    _save_ignore = ['dns_name', 'host', 'zone']
    _search_by = ['name', 'ipv4addr', 'ipv6addr', 'mac']
    _supports = ['delete', 'save']
    _wapi_type = 'record:host'

    def __init__(self, session, reference_id=None, name=None, **kwargs):
        """Create a new instance of a Host object. If a reference_id or valid
        search criteria are passed in, the object will attempt to load the
        values for the host from the Infoblox device.

        When creating a new host or adding an ip address, use the
        Host.add_ipv4_address and Host.add_ipv6_address methods::

            host.add_ipv4addr('1.2.3.4')

        Valid search criteria: name, ipv4addr, ipv6addr, mac

        :param infobox.Session session: The established session object
        :param str reference_id: The Infoblox reference id for the host
        :param str host: The host's FQDN
        :param dict kwargs: Optional keyword arguments

        """
        self.name = name
        super(Host, self).__init__(session, reference_id, **kwargs)

    def add_ipv4addr(self, ipv4addr):
        """Add an IPv4 address to the host.

        :param str ipv4addr: The IP address to add.
        :raises: ValueError

        """
        for addr in self.ipv4addrs:
            if ((isinstance(addr, dict) and addr['ipv4addr'] == ipv4addr) or
                (isinstance(addr, HostIPv4) and addr.ipv4addr == ipv4addr)):
                raise ValueError('Already exists')
        self.ipv4addrs.append({'ipv4addr': ipv4addr})

    def remove_ipv4addr(self, ipv4addr):
        """Remove an IPv4 address from the host.

        :param str ipv4addr: The IP address to remove

        """
        for addr in self.ipv4addrs:
            if ((isinstance(addr, dict) and addr['ipv4addr'] == ipv4addr) or
                (isinstance(addr, HostIPv4) and addr.ipv4addr == ipv4addr)):
                self.ipv4addrs.remove(addr)
                break

    def add_ipv6addr(self, ipv6addr):
        """Add an IPv6 address to the host.

        :param str ipv6addr: The IP address to add.
        :raises: ValueError

        """
        for addr in self.ipv6addrs:
            if ((isinstance(addr, dict) and addr['ipv6addr'] == ipv6addr) or
                (isinstance(addr, HostIPv4) and addr.ipv6addr == ipv6addr)):
                raise ValueError('Already exists')
        self.ipv6addrs.append({'ipv6addr': ipv6addr})

    def remove_ipv6addr(self, ipv6addr):
        """Remove an IPv6 address from the host.

        :param str ipv6addr: The IP address to remove

        """
        for addr in self.ipv6addrs:
            if ((isinstance(addr, dict) and addr['ipv6addr'] == ipv6addr) or
                (isinstance(addr, HostIPv4) and addr.ipv6addr == ipv6addr)):
                self.ipv6addrs.remove(addr)
                break


class HostIPv4(Record):
    """Implements the host_ipv4addr record type.

    """
    bootfile = None
    bootserver = None
    configure_for_dhcp = None
    deny_bootp = None
    discovered_data = None
    enable_pxe_lease_time = None
    host = None
    ignore_client_requested_options = None
    ipv4addr = None
    last_queried = None
    mac = None
    match_client = None
    network = None
    nextserver = None
    options = None
    pxe_lease_time = None
    use_bootfile = None
    use_bootserver = None
    use_deny_bootp = None
    use_for_ea_inheritance = None
    use_ignore_client_requested_options = None
    use_nextserver = None
    use_options = None
    use_pxe_lease_time = None

    _repr_keys = ['ipv4addr']
    _search_by = ['ipv4addr']
    _wapi_type = 'record:host_ipv4addr'

    def __init__(self, session, reference_id=None, ipv4addr=None, **kwargs):
        """Create a new instance of a HostIPv4 object. If a reference_id or
        valid search criteria are passed in, the object will attempt to load
        the values for the host_ipv4addr from the Infoblox device.

        Valid search criteria: ipv4addr

        :param infobox.Session session: The established session object
        :param str reference_id: The Infoblox reference id for the host
        :param str ipv4addr: The ipv4 address
        :param dict kwargs: Optional keyword arguments

        """
        self.ipv4addr = str(ipv4addr)
        super(HostIPv4, self).__init__(session, reference_id, **kwargs)

    def _save_as(self):
        return {'ipv4addr': self.ipv4addr}


class HostIPv6(Record):
    """Implements the host_ipv6addr record type.

    """
    address_type = None
    configure_for_dhcp = True
    discovered_data = None
    domain_name = None
    domain_name_servers = []
    duid = None
    host = None
    ipv6addr = None
    ipv6bits = None
    ipv6prefix_bits = None
    match_client = None
    options = None
    preferred_lifetime = 27000
    use_domain_name = False
    use_domain_name_servers = False
    use_for_ea_inheritance = False
    use_options = False
    use_valid_lifetime = False
    valid_lifetime = 43200

    _repr_keys = ['ipv6addr', 'ipv6bits', 'ipv6prefix_bits']
    _save_ignore = ['host']
    _search_by = ['ipv6addr']
    _wapi_type = 'record:host_ipv6addr'

    def __init__(self, session, reference_id=None, ipv6addr=None,
                 ipv6bits=None, ipv6prefix_bits=None, **kwargs):
        """Create a new instance of a HostIPv6 object. If a reference_id or
        valid search criteria are passed in, the object will attempt to load
        the values for the host_ipv6addr from the Infoblox device.

        Valid search criteria: ipv6addr

        :param infobox.Session session: The established session object
        :param str reference_id: The Infoblox reference id for the host
        :param str ipv6addr: The ipv6 address
        :param str ipv6bits: The ipv6 address bit count
        :param str ipv6prefix_bits: The ipv6 address prefix bit count
        :param dict kwargs: Optional keyword arguments

        """
        self.ipv6addr = str(ipv6addr)
        self.ipv6bits = str(ipv6bits)
        self.ipv6prefix_bits = str(ipv6prefix_bits)
        super(HostIPv6, self).__init__(session, reference_id, **kwargs)

    def _save_as(self):
        return {'ipv6addr': self.ipv6addr,
                'ipv6bits': self.ipv6bits,
                'ipv6prefix_bits': self.ipv6prefix_bits}


class IPv4Address(Record):
    """Implements the ipv4address record type.


    """
    dhcp_client_identifier = None

    extattrs = None
    fingerprint = None
    ip_address = None
    is_conflict = None
    lease_state = None
    mac_address = None
    names = None
    network = None
    network_view = None
    objects = None
    status = None
    types = None
    usage = None
    username = None

    _repr_keys = ['ip_address']
    _search_by = ['ip_address']
    _supports = ['fetch', 'put']
    _wapi_type = 'record:host_ipv4addr'

    def __init__(self, session, reference_id=None, ipv4addr=None, **kwargs):
        """Create a new instance of a HostIPv4 object. If a reference_id or
        valid search criteria are passed in, the object will attempt to load
        the values for the host_ipv4addr from the Infoblox device.

        Valid search criteria: ipv4addr

        :param infobox.Session session: The established session object
        :param str reference_id: The Infoblox reference id for the host
        :param str ipv4addr: The ipv4 address
        :param dict kwargs: Optional keyword arguments

        """
        self.ipv4addr = str(ipv4addr)
        super(IPv4Address, self).__init__(session, reference_id, **kwargs)


def get_class(reference):
    class_name = reference.split('/')[0].split(':')[1]
    LOGGER.debug('Class: %s', class_name)
    return CLASS_MAP.get(class_name)


CLASS_MAP = {'host': Host,
             'host_ipv4addr': HostIPv4,
             'host_ipv6addr': HostIPv6,
             'ipv4address': IPv4Address}
