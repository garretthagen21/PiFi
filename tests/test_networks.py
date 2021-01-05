from unittest import TestCase
import tempfile
import os

from wpa_pyfi import Cell
from wpa_pyfi.network import Network
from wpa_pyfi.exceptions import ConnectionError

# TODO: Implement these tests
WPA_SUPP_CONFIG_CONTENTS = """

    # This is a comment as a header
    
    country=US
    update_config=1
    ctrl_interface=/var/run/wpa_supplicant
    
    network={
     ssid="TestSSID1"
     psk="TestPass1"
     key_mgmt=WPA-PSK
     priority=1
     id_str="SSID_BASIC"
    }
    
    network={
     ssid="TestSSID2"
     psk="TestPass2"
     priority=5
     id_str="SSID_NO_KEY_MGMT"
    }
    
    network={
     ssid="TestSSID3"
     key_mgmt=NONE
     id_str="SSID_NO_PSK"
    }
    
    network={
     ssid="TestSSID4"
     psk="TestPass4"
     key_mgmt=WPA-PSK
     id_str="SID_NO_PRIORITY"
    }
    
    network={
     ssid="Test-SSID5"
     psk="TestPass1"
     key_mgmt=WPA-PSK
     priority=3
     proto=wpa2
     id_str="SID_PROTO"
    }
    
    network={
     ssid="Test SSID6"
     
     psk="TestPass6"
     key_mgmt=WPA-PSK
     
     priority=4
     proto=wpa2
     id_str="SSID_SPACES"
    
    }
"""


# TODO: This needs more extensive test cases

class TestNetworks(TestCase):
    def setUp(self):
        self.tempfile, self.file_path = tempfile.mkstemp()
        self.NetworkClass = Network.for_file(self.file_path)

        with open(self.NetworkClass.WPA_SUPPLICANT_CONFIG, 'w') as f:
            f.write(WPA_SUPP_CONFIG_CONTENTS)

    def tearDown(self):
        os.remove(self.NetworkClass.WPA_SUPPLICANT_CONFIG)

    def test_network_extraction(self):
        all_networks = self.NetworkClass.all()
        assert len(all_networks) == 6
        for network in all_networks:
            self.assertIsNotNone(network)

    def test_with_hyphen(self):
        network_with_hyphen = self.NetworkClass.find("Test-SSID5")
        self.assertIsNotNone(network_with_hyphen)
        self.assertEqual(network_with_hyphen.ssid, "Test-SSID5")

    def test_with_space(self):
        network_with_space = self.NetworkClass.find("Test SSID6")
        self.assertIsNotNone(network_with_space)
        self.assertEqual(network_with_space.ssid, "Test SSID6", )

    def test_delete(self):
        delete_net = self.NetworkClass.find("TestSSID1")
        delete_net.delete(disconnect_immediately=False)
        self.assertIsNone(self.NetworkClass.find("TestSSID1"))

    def test_save(self):
        new_network = self.NetworkClass.new_network(ssid='test_save', passkey="passkeypasskey", id_str='test_save_name')
        new_network.save()
        self.assertIsNotNone(new_network)


"""
class TestActivation(TestCase):
    def test_successful_connection(self):
        network = Network('wlan0', 'test')
        connection = network.parse_ifup_output(SUCCESSFUL_IFUP_OUTPUT)
        self.assertEqual(connection.network, network)
        self.assertEqual(connection.ip_address, '192.168.1.113')

    def test_failed_connection(self):
        network = Network('wlan0', 'test')
        self.assertRaises(ConnectionError, network.parse_ifup_output, FAILED_IFUP_OUTPUT)


class TestForCell(TestCase):
    def test_unencrypted(self):
        cell = Cell()
        cell.ssid = 'SSID'
        cell.encrypted = False

        network = Network.for_cell('wlan0', 'test', cell)

        self.assertEqual(network.options, {
            'wireless-essid': 'SSID',
            'wireless-channel': 'auto',
        })

    def test_wep_hex(self):
        cell = Cell()
        cell.ssid = 'SSID'
        cell.encrypted = True
        cell.encryption_type = 'wep'

        # hex key lengths: 10, 26, 32, 58
        hex_keys = ("01234567ab", "0123456789abc" * 2, "0123456789abcdef" * 2, "0123456789abc" * 2 + "0123456789abcdef" * 2)
        for key in hex_keys:
            network = Network.for_cell('wlan0', 'test', cell, key)

            self.assertEqual(network.options, {
                'wireless-essid': 'SSID',
                'wireless-key': key
            })

    def test_wep_ascii(self):
        cell = Cell()
        cell.ssid = 'SSID'
        cell.encrypted = True
        cell.encryption_type = 'wep'

        # ascii key lengths: 5, 13, 16, 29
        ascii_keys = ('a' * 5, 'a' * 13, 'a' * 16, 'a' * 29)
        for key in ascii_keys:
            network = Network.for_cell('wlan0', 'test', cell, key)

            self.assertEqual(network.options, {
                'wireless-essid': 'SSID',
                'wireless-key': 's:' + key
            })

    def test_wpa2(self):
        cell = Cell()
        cell.ssid = 'SSID'
        cell.encrypted = True
        cell.encryption_type = 'wpa2'

        network = Network.for_cell('wlan0', 'test', cell, b'passkey')

        self.assertEqual(network.options, {
            'wpa-ssid': 'SSID',
            'wpa-psk': 'ea1548d4e8850c8d94c5ef9ed6fe483981b64c1436952cb1bf80c08a68cdc763',
            'wireless-channel': 'auto',
        })

    def test_wpa(self):
        cell = Cell()
        cell.ssid = 'SSID'
        cell.encrypted = True
        cell.encryption_type = 'wpa'

        network = Network.for_cell('wlan0', 'test', cell, 'passkey')

        self.assertEqual(network.options, {
            'wpa-ssid': 'SSID',
            'wpa-psk': 'ea1548d4e8850c8d94c5ef9ed6fe483981b64c1436952cb1bf80c08a68cdc763',
            'wireless-channel': 'auto',
        })
"""

SUCCESSFUL_IFDOWN_OUTPUT = """Internet Systems Consortium DHCP Client 4.2.4
Copyright 2004-2012 Internet Systems Consortium.
All rights reserved.
For info, please visit https://www.isc.org/software/dhcp/

Listening on LPF/wlan0/9c:4e:36:5d:2c:64
Sending on   LPF/wlan0/9c:4e:36:5d:2c:64
Sending on   Socket/fallback
DHCPRELEASE on wlan0 to 192.168.1.1 port 67
"""

SUCCESSFUL_IFUP_OUTPUT = """Internet Systems Consortium DHCP Client 4.2.4
Copyright 2004-2012 Internet Systems Consortium.
All rights reserved.
For info, please visit https://www.isc.org/software/dhcp/

Listening on LPF/wlan0/9c:4e:36:5d:2c:64
Sending on   LPF/wlan0/9c:4e:36:5d:2c:64
Sending on   Socket/fallback
DHCPDISCOVER on wlan0 to 255.255.255.255 port 67 interval 4
DHCPDISCOVER on wlan0 to 255.255.255.255 port 67 interval 8
DHCPREQUEST on wlan0 to 255.255.255.255 port 67
DHCPOFFER from 192.168.1.1
DHCPACK from 192.168.1.1
bound to 192.168.1.113 -- renewal in 2776 seconds.
"""

FAILED_IFUP_OUTPUT = """Internet Systems Consortium DHCP Client 4.2.4
Copyright 2004-2012 Internet Systems Consortium.
All rights reserved.
For info, please visit https://www.isc.org/software/dhcp/

Listening on LPF/wlan0/9c:4e:36:5d:2c:64
Sending on   LPF/wlan0/9c:4e:36:5d:2c:64
Sending on   Socket/fallback
DHCPDISCOVER on wlan0 to 255.255.255.255 port 67 interval 5
DHCPDISCOVER on wlan0 to 255.255.255.255 port 67 interval 8
DHCPDISCOVER on wlan0 to 255.255.255.255 port 67 interval 18
DHCPDISCOVER on wlan0 to 255.255.255.255 port 67 interval 18
DHCPDISCOVER on wlan0 to 255.255.255.255 port 67 interval 12
No DHCPOFFERS received.
No working leases in persistent database - sleeping.
"""
