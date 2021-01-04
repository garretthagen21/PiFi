PiFi, a Python Interface for Wifi Control on Linux Devices
===========================================================


Pifi provides a set of tools for configuring and connecting to Wifi networks on Linux systems.
Using this library, you can discover networks, connect to them, save your configurations, and much, much more.

The original impetus for creating this library was my frustration with with connecting to the Internet using NetworkManager and wicd.
It is very much for computer programmers, not so much for normal computer users.
Pifi is built on top the old technologies of the /etc/wpa_supplicant/wpa_supplicant.conf file and the corresponse wpa_cli
command line tool

The library also comes with an executable that you can use to manage your Wifi connections.
Pifi currently supports the following encryption types:

-  No encryption
-  WPA2

If you need support for other network types, please file a bug on GitHub and we'll definitely try to get to it.
Patches, of course, are always welcome.


Installation
------------

Pifi is available for installation on PyPI::

    $ pip install pifi

This will install the :doc:`the pifi command <pifi_command>`, a Python library for discovering and connecting to pifi networks, and a bash completion file for the pifi command.

On some systems, the pifi command name is already used, and installing pifi will cause issues with the system.
In those cases you can override the command name that is installed::

    $ PIFI_CLI_NAME=cool-pifi pip install pifi

`The pifi executable <pifi_command>` will instead be named `cool-pifi`.

If you only want the Python library and don't care about the CLI, you can also disable it::

    $ PIFI_INSTALL_CLI=False pip install pifi

There will be no extra executable installed, but the pifi CLI will still be available using this invocation style::

    $ python -m pifi


Documentation
-------------

.. toctree::
    :maxdepth: 2

    pifi_command
    scanning
    changelog

Contributing
------------

The (very little) development for pifi happens on GitHub.
If you ever run into issues with pifi, please don't hesitate to open an issue.
Pull requests are welcome.
