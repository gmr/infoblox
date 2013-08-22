infoblox
========
A python library for interfacing with Infoblox NIOS.

Requirements
------------
Python 2.6, 2.7, 3.2, 3.3

External dependencies:
 - `argparse <http://pypi.python.org/pypi/argparse>`_ (Python 2.6 only)
 - `requests <http://docs.python-requests.org/en/latest/>`_

CLI Usage::

    usage: infoblox-host [-h] [-u USERNAME] [-p PASSWORD] [-c COMMENT] [--version]
                         {add,remove} infobox host address

    Add or remove a host from the Infoblox appliance

    positional arguments:
      {add,remove}          The action to take for the host
      infobox               The Infoblox hostname
      host                  The FQDN for the host
      address               The IPv4 address for the host

    optional arguments:
      -h, --help            show this help message and exit
      -u USERNAME, --username USERNAME
                            The username to perform the work as. Default: admin
      -p PASSWORD, --password PASSWORD
                            The password to authenticate with. Default: infoblox
      -c COMMENT, --comment COMMENT
                            A comment to use when performing the action. Default:
                            Created by python with love
      --version             show program's version number and exit

Library Example::

    import infoblox

    obj = infoblox.Infoblox('127.0.0.1', 'admin', 'infoblox')
    if obj.add_new_host('hostname', '10.0.0.1', 'Comment!'):
        print 'hostname (10.0.0.1) added'

    if obj.delete_old_host('hostname', '10.0.0.1'):
        print 'hostname (10.0.0.1) removed'

Contents:

.. toctree::
   :maxdepth: 4

   infoblox

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

