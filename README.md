infoblox
========
A python library for interfacing with Infoblox NIOS.

This library is not official, nor is it affiliated with [Infoblox, Inc.](http://www.infoblox.com) in any way.

[![PyPI version](https://badge.fury.io/py/infoblox.png)](http://badge.fury.io/py/infoblox) [![Downloads](https://pypip.in/d/infoblox/badge.png)](https://crate.io/packages/pamqp) [![Build Status](https://travis-ci.org/gmr/infoblox.png?branch=master)](https://travis-ci.org/gmr/infoblox)

Documentation
-------------
http://infoblox.readthedocs.org

Requirements
------------
Python 2.6, 2.7, 3.2, 3.3

### External dependencies
- [argparse](http://pypi.python.org/pypi/argparse) (Python 2.6 only)
- [requests](http://docs.python-requests.org/en/latest/)

CLI Usage
---------

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

    import infoblox

    session = infoblox.Session('127.0.0.1', 'admin', 'infoblox')
    host = infoblox.Host(session)
    host.name = 'foo.bar.net'
    host.add_ipv4addr('10.0.0.1')
    if host.save():
        print('Host saved')
