#!/usr/bin/python
from __future__ import print_function
import argparse
import sys
import os

from wpa_pyfi import Cell, Network
from wpa_pyfi.utils import print_table, match as fuzzy_match
from wpa_pyfi.exceptions import ConnectionError, InterfaceError


def fuzzy_find_cell(interface, query):
    match_partial = lambda cell: fuzzy_match(query, cell.ssid)

    matches = Cell.where(interface, match_partial)

    num_unique_matches = len(set(cell.ssid for cell in matches))
    assert num_unique_matches > 0, "Couldn't find a network that matches '{}'".format(query)
    assert num_unique_matches < 2, "Found more than one network that matches '{}'".format(query)

    # Several cells of the same SSID
    if len(matches) > 1:
        matches.sort(key=lambda cell: cell.signal)

    return matches[0]


def find_cell(interface, query):
    cell = Cell.where(interface, lambda cell: cell.ssid.lower() == query.lower())

    try:
        cell = cell[0]
    except IndexError:
        cell = fuzzy_find_cell(interface, query)
    return cell


def get_network_params(interface, ssid, netname=None):
    cell = find_cell(interface, ssid or netname)
    passkey = None if not cell.encrypted else input('passkey> ')

    return cell, passkey, netname, interface


def scan_command(args):
    print_table([[cell.signal, cell.ssid, 'protected' if cell.encrypted else 'unprotected'] for cell in
                 Cell.all(args.interface)])


def list_command(args):
    for network in Network.for_file(args.file).all():
        print(network)


def show_command(args):
    network = Network.for_file(args.file).for_cell(*get_network_params(args.interface, args.ssid, args.netname))
    print(network)


def add_command(args):
    network_class = Network.for_file(args.file)
    assert not network_class.find(args.ssid), "That network has already been used"

    network = network_class.for_cell(*get_network_params(args.interface, args.ssid, args.netname))
    network.save()


def connect_command(args):
    network_class = Network.for_file(args.file)
    network = network_class.find(ssid=args.ssid, name=args.netname)
    assert network, "Couldn't find a Network Named {0!r}, did you mean to use -a?".format(args.ssid)

    try:
        network.activate()
        print(network.get_connection_data())
    except ConnectionError:
        assert False, "Failed to Connect to %s." % network.ssid


def delete_command(args):
    network_class = Network.for_file(args.file)
    network = network_class.find(args.ssid)
    assert network, "Couldn't find a network named {0!r}".format(args.ssid)

    if network.delete():
        print("Successfully Deleted Network: " + str(network))
    else:
        print("Failed to Delete Network: " + str(network))


def autoconnect_command(args):
    ssids = [cell.ssid for cell in Cell.all(args.interface)]

    for network in Network.all():
        # TODO: make it easier to get the SSID off of a network.
        ssid = network.ssid
        if ssid in ssids:
            sys.stderr.write('Connecting to "%s".\n' % ssid)
            try:
                network.activate()
            except ConnectionError:
                assert False, "Failed to connect to %s." % network.ssid
            break
    else:
        assert False, "Couldn't find any networks that are currently available."


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i',
                        '--interface',
                        default='wlan0',
                        help="Specifies which interface to use (wlan0, eth0, etc.)")
    parser.add_argument('-f',
                        '--file',
                        default='/etc/wpa_supplicant/wpa_supplicant.conf',
                        help="Specifies which file for network storage.")

    subparsers = parser.add_subparsers(title='commands')

    parser_scan = subparsers.add_parser('scan', help="Shows a list of available networks.")
    parser_scan.set_defaults(func=scan_command)

    parser_list = subparsers.add_parser('list', help="Shows a list of networks already configured.")
    parser_list.set_defaults(func=list_command)

    network_help = ("A memorable nickname for a wireless network."
                    "  If SSID is not provided, the network will be guessed using NETNAME.")
    ssid_help = ("The SSID for the network to which you wish to connect."
                 "  This is fuzzy matched, so you don't have to be precise.")

    parser_show = subparsers.add_parser('config', help="Dry run print the configuration to connect to a new network.")
    parser_show.add_argument('ssid', help=ssid_help, metavar='SSID')
    parser_show.add_argument('netname', help=network_help, metavar='NETNAME', nargs='?', default=None)
    parser_show.set_defaults(func=show_command)

    parser_add = subparsers.add_parser('add',
                                       help="Adds the configuration to connect to a new network.")
    parser_add.add_argument('ssid', help=ssid_help, metavar='SSID')
    parser_add.add_argument('netname', help=network_help, metavar='NETNAME', nargs='?', default=None)
    parser_add.set_defaults(func=add_command)

    parser_delete = subparsers.add_parser('delete',
                                          help="Deletes a network that is currently configured.")
    parser_delete.add_argument('ssid', help=ssid_help, metavar='SSID')
    parser_delete.add_argument('netname', help=network_help, metavar='NETNAME', nargs='?', default=None)
    parser_delete.set_defaults(func=delete_command)

    parser_connect = subparsers.add_parser('connect',
                                           help="Connects to the network corresponding to NETWORK")
    parser_connect.add_argument('ssid',
                                help="The ssid of the network to which you wish to connect.",
                                metavar='SSID')
    parser_connect.add_argument('netname',
                                help="The nickname of the network to which you wish to connect.",
                                metavar='NETNAME', nargs='?', default=None)
    parser_connect.set_defaults(func=connect_command)

    parser_connect.get_options = lambda: [network.ssid for network in Network.all()]

    parser_autoconnect = subparsers.add_parser(
        'autoconnect',
        help="Searches for saved networks that are currently"
             " available and connects to the first one it finds."
    )
    parser_autoconnect.set_defaults(func=autoconnect_command)

    return parser, subparsers


def autocomplete(position, wordlist, subparsers):
    if position == 1:
        ret = subparsers.choices.keys()
    else:
        try:
            prev = wordlist[position - 1]
            ret = subparsers.choices[prev].get_options()
        except (IndexError, KeyError, AttributeError):
            ret = []

    print(' '.join(ret))


def main():
    parser, subparsers = arg_parser()
    argv = sys.argv[1:]
    args = parser.parse_args(argv)

    try:
        if 'WIFI_AUTOCOMPLETE' in os.environ:
            autocomplete(int(os.environ['COMP_CWORD']),
                         os.environ['COMP_WORDS'].split(), subparsers)
        else:
            command = getattr(args, 'func', scan_command)
            command(args)
    except (AssertionError, InterfaceError) as e:
        sys.stderr.write("Error: ")
        sys.exit(e)
