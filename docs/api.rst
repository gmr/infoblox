infoblox API
============
To interact with an Infoblox device, you must first create a Session object instance
that will be passed to any object you create. The following example shows how to create
a host.::

    import infoblox

    session = infoblox.Session('127.0.0.1', 'admin', 'infoblox')
    host = infoblox.Host(session)
    host.name = 'foo.bar.net'
    host.add_ipv4addr('10.0.0.1')
    if host.save():
        print('Host saved')

.. autoclass:: infoblox.Session

.. autoclass:: infoblox.Host
    :members:
    :inherited-members:

.. autoclass:: infoblox.HostIPv4
    :members:
    :inherited-members:

.. autoclass:: infoblox.HostIPv6
    :members:
    :inherited-members:
