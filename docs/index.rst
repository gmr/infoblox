infoblox
========
A python library for interfacing with Infoblox NIOS.

This library is not official, nor is it affiliated with `Infoblox, Inc. <http://www.infoblox.com>`_ in any way.

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

Usage
-----
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

Contents
--------
.. toctree::
   :maxdepth: 4

   infoblox

License
-------
Copyright (c) 2013 Gavin M. Roy
All rights reserved. All registered trademarks are property of their respective owners.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

 * Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
 * Neither the name of the infoblox library nor the names of its
   contributors may be used to endorse or promote products derived from this
   software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

