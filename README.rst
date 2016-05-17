infoblox
========
An unofficial python library for interfacing with Infoblox NIOS. This library is not affiliated with _`Infoblox, Inc. <http://www.infoblox.com>` in any way.

:boom:**Important**:boom: This project is deprecated and no longer maintained. If you'd like to take it over, please contact me.

|PyPI version| |Downloads| |Build Status|

Documentation
-------------
http://infoblox.readthedocs.org

Requirements
------------
- Python 2.6, 2.7, 3.2, 3.3
- _`argparse <http://pypi.python.org/pypi/argparse>` (Python 2.6 only)
- _`requests <http://docs.python-requests.org/en/latest/>`

CLI Usage
---------
.. code:: bash

    usage: infoblox-host [-h] [--version] [--debug] [-u USERNAME] [-p PASSWORD]
              <Infoblox Address> {add,remove} <FQDN> [IPv4 Address] [COMMENT]

    Add or remove a host from the Infoblox appliance

    positional arguments:
      <Infoblox Address>    The Infoblox hostname
      {add,remove}          Specify if you are adding or removing a host
      <FQDN>                The FQDN for the host
      [IPv4 Address]        The IPv4 address for the host
      [COMMENT]             A comment set on the host when adding.

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      --debug               Enable debug output
      -u USERNAME, --username USERNAME
                            The username to perform the work as. Default: admin
      -p PASSWORD, --password PASSWORD
                            The password to authenticate with. Default: infoblox

Library Usage
-------------
.. code:: python

    import infoblox

    session = infoblox.Session('127.0.0.1', 'admin', 'infoblox')
    host = infoblox.Host(session)
    host.name = 'foo.bar.net'
    host.add_ipv4addr('10.0.0.1')
    if host.save():
        print('Host saved')


.. |PyPI version| image:: https://badge.fury.io/py/infoblox.png
   :target: http://badge.fury.io/py/infoblox
.. |Downloads| image:: https://pypip.in/d/infoblox/badge.png
   :target: https://crate.io/packages/infoblox
.. |Build Status| image:: https://travis-ci.org/gmr/infoblox.png?branch=master
   :target: https://travis-ci.org/gmr/infoblox
