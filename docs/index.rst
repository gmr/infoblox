infoblox
========
An unofficial python library for interfacing with Infoblox NIOS. This library is not affiliated with `Infoblox, Inc. <http://www.infoblox.com>`_ in any way.

.. image:: https://travis-ci.org/gmr/infoblox.png?branch=master   :target: https://travis-ci.org/gmr/infoblox

Requirements
------------
Python 2.6, 2.7, 3.2, 3.3

External dependencies:
 - `argparse <http://pypi.python.org/pypi/argparse>`_ (Python 2.6 only)
 - `requests <http://docs.python-requests.org/en/latest/>`_

Installation
------------
infoblox is available on the `Python Package Index <https://pypi.python.org>`_ and can be installed with `easy_install` or `pip`::

    pip install infoblox

API Documentation
-----------------
The following classes are available for interaction with the Infoblox NIOS device:
 - :py:class:`infoblox.Session`
 - :py:class:`infoblox.Host`
 - :py:class:`infoblox.HostIPv4`
 - :py:class:`infoblox.HostIPv6`

CLI Usage
---------
::

    usage: infoblox-host     usage: infoblox-host [-h] [--version] [--debug] [-u USERNAME] [-p PASSWORD]
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


Contents
--------
.. toctree::
   :maxdepth: 4

   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

