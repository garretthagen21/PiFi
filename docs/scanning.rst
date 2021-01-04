Managing WiFi networks
======================

.. currentmodule:: pifi

Discovering networks
--------------------

You can use this library to scan for networks that are available in the air.
To get a list of the different cells in the area, you can do ::

    >>> from pifi import Cell, Network
    >>> Cell.all('wlan0')

This returns a list of :class:`Cell` objects.  Under the hood, this calls `iwlist scan` and parses the unfriendly output.

Each cell object should have the following attributes:

- :attr:`ssid`
- :attr:`signal`
- :attr:`quality`
- :attr:`frequency`
- :attr:`bitrates`
- :attr:`encrypted`
- :attr:`channel`
- :attr:`address`
- :attr:`mode`

For cells that have :attr:`encrypted` as `True`, there will also be the following attributes:

- :attr:`encryption_type`

.. note::

    Scanning requires root permission to see all the networks.
    If you are not root, iwlist only returns the network you are currently connected to.


Connecting to a network
-----------------------

In order to connect to a network, you need to set up a configureation for it in the wpa_supplicant.conf file. ::

    >>> cell = Cell.all('wlan0')[0]
    >>> network = Network.for_cell(cell, passkey, interface='wlan0')
    >>> network.save()
    >>> network.activate()

Once you have a network saved, you can retrieve it using :meth:`Network.find`. ::

    >>> network = Network.find('home')
    >>> network.activate()

.. note::

    Activating a network will disconnect from any other network before connecting.

    You must be root to connect to a network.
    PiFi uses `wpa_cli reconfigure' and ifconfig up/down to connect/disconnect to the networks specified
    in the wpa_supplicant.conf file

.. autoclass:: Cell
    :members:

.. autoclass:: Network
    :members:
