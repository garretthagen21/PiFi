wpa_pyfi, a Python Interface for Wifi Control on Linux Devices
==============================================================


Wpa_pyfi provides a set of tools for configuring and connecting to Wifi networks on Linux systems.
Using this library, you can discover networks, connect to them, save your configurations, and much, much more.

The original impetus for creating this library was my frustration with with connecting to the Internet using NetworkManager and wicd.
It is very much for computer programmers, not so much for normal computer users.
Wpa_pyfi is built on top the old technologies of the /etc/wpa_supplicant/wpa_supplicant.conf file and the corresponse wpa_cli
command line tool

The library also comes with an executable that you can use to manage your Wifi connections.
Wpa_pyfi currently supports the following encryption types:

-  No encryption
-  WPA2

If you need support for other network types, please file a bug on GitHub and we'll definitely try to get to it.
Patches, of course, are always welcome.


Installation
------------

Wpa_pyfi is available for installation on PyPI::

    $ pip install wpa_pyfi

This will install the `the wpa_pyfi command <wpa_pyfi_command>`, a Python library for discovering and connecting to wpa_pyfi networks, and a bash completion file for the wpa_pyfi command.

On some systems, the wpa_pyfi command name is already used, and installing wpa_pyfi will cause issues with the system.
In those cases you can override the command name that is installed::

    $ WPA_PYFI_CLI_NAME=cool-wpa_pyfi pip install wpa_pyfi

`The wpa_pyfi executable <wpa_pyfi_command>` will instead be named `cool-wpa_pyfi`.

If you only want the Python library and don't care about the CLI, you can also disable it::

    $ WPA_PYFI_INSTALL_CLI=False pip install wpa_pyfi

There will be no extra executable installed, but the wpa_pyfi CLI will still be available using this invocation style::

    $ python -m wpa_pyfi


Documentation
-------------

.. toctree::::
    :maxdepth: 2

    wpa_pyfi_command
    scanning
    changelog

Contributing
------------

The (very little) development for wpa_pyfi happens on GitHub.
If you ever run into issues with wpa_pyfi, please don't hesitate to open an issue.
Pull requests are welcome.
