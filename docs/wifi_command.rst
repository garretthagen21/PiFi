The pifi Command
================

This library comes with a command line program for managing and saving your Pifi connections.

Tutorial
^^^^^^^^

This tutorial assumes you are comfortable on the command line.
(If you aren't, perhaps pifi is not quite the right tool for you.)

First, if you haven't already, install pifi.

.. code-block:: sh

    $ pip install pifi

Now, you want to see what networks are available.
You can run the ``scan`` command to do that.

.. note::
    All of these commands need to run as a superuser.

.. code-block:: sh

    # pifi scan
    -61  SomeNet                  protected
    -62  SomeOtherNet             unprotected
    -78  zxy-12345                protected
    -86  TP-LINK_CB1676           protected
    -86  TP-LINK_PocketAP_D8B616  unprotected
    -82  TP-LINK_C1DBE8           protected
    -86  XXYYYYZZZ                protected
    -87  Made Up Name             protected

.. note::

    The pifi command is also accessible through the python argument as::

        # python -m pifi

The scan command returns three bits of data: the signal quality, the SSID and if the network is protected or not.
If you want to order the networks by quality, you can pipe the output into sort.

.. code-block:: sh

    # pifi scan | sort -rn
    -61  SomeNet                  protected
    -62  SomeOtherNet             unprotected
    -78  zxy-12345                protected
    -82  TP-LINK_C1DBE8           protected
    -86  XXYYYYZZZ                protected
    -86  TP-LINK_PocketAP_D8B616  unprotected
    -86  TP-LINK_CB1676           protected
    -87  Made Up Name             protected

The greater the number, the better the signal.

We decide to use the ``SomeNet`` network because that's the closest one (plus we know the password).
We can connect to it directly using the ``connect`` command.

.. code-block:: sh

    # pifi connect --ad-hoc SomeNet
    passkey>

The ``--ad-hoc`` or ``-a`` option allows us to connect to a network that we haven't configured before.
The pifi asks you for a passkey if the network is protected and then it will connect.

If you want to actually save the configuration instead of just connecting once, you can use the ``add`` command.

.. code-block:: sh

    # pifi add some SomeNet
    passkey>

``some`` here is a nickname for the network you can use when you want to connect to the network again.
Now we can connect to the saved network if you want using the ``connect`` command.

.. code-block:: sh

    # pifi connect some
    ...

If you wish to see all the saved networks, you can use the ``list`` command.


.. code-block:: sh

    # pifi list
    some

Usage
^^^^^

::

    usage: pifi {scan,list,config,add,connect,init} ...

scan
----

Shows a list of available networks. ::

    usage: pifi scan

list
----

Shows a list of networks already configured. ::

    usage: pifi list

add, config
-----------

Prints or adds the configuration to connect to a new network. ::

    usage: pifi config NETWORK [SSID]
    usage: pifi add NETWORK [SSID]

    positional arguments:
      NETWORK     A memorable nickname for a wireless network. If SSID is not
                  provided, the network will be guessed using NETWORK.
      SSID        The SSID for the network to which you wish to connect. This is
                  fuzzy matched, so you don't have to be precise.

connect
-------

Connects to the network corresponding to NETWORK. ::

    usage: pifi connect [-a] NETWORK

    positional arguments:
      NETWORK        The nickname of the network to which you wish to connect.

    optional arguments:
      -a, --ad-hoc  Connect to a network without storing it in the config file

autoconnect
-----------

Searches for saved networks that are currently available and connects to the
first one it finds. ::

    usage: pifi autoconnect


Completion
^^^^^^^^^^

The pifi command also comes packaged with completion for bash.
If you want to write completion for your own shell, pifi provides an interface for extracting completion information.
Please see the ``pifi-completion.bash`` and ``bin/pifi`` files for more information.
