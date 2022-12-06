#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyssc as ssc
import os
import json
import argparse


__author__ = "Thorsten Schwinn"
__version__ = '0.1'
__license__ = "MIT"


def send_command(device, str):
    ssc_transaction = device.send_ssc(str, buffersize=256)
    print(ssc_transaction.RX.replace("\r\n", ""))


def query_device(device):
    print("*** query device settings ***")
    send_command(device, '{"device":{"name":null}}')
    send_command(device, '{"device":{"identity":{"vendor":null}}}')
    send_command(device, '{"device":{"identity":{"product":null}}}')
    send_command(device, '{"device":{"identity":{"serial":null}}}')
    send_command(device, '{"device":{"identity":{"version":null}}}')
    send_command(device, '{"ui":{"logo":{"brightness":null}}}')
    send_command(device, '{"audio":{"in":{"gain":null}}}')
    send_command(device, '{"audio":{"in":{"phase_invert":null}}}')
    send_command(device, '{"audio":{"out":{"level":null}}}')
    send_command(device, '{"audio":{"out":{"dimm":null}}}')
    send_command(device, '{"audio":{"out":{"delay":null}}}')
    send_command(device, '{"audio":{"out":{"mute":null}}}')
    send_command(device, '{"audio":{"out":{"solo":null}}}')
    send_command(device, '{"audio":{"out":{"phase_correction":null}}}')
    send_command(device, '{"audio":{"out":{"limiter_mode":null}}}')
    send_command(device, '{"audio":{"out":{"equalizer":{"enabled":null}}}}')
    send_command(device, '{"audio":{"out":{"equalizer":{"type":null}}}}')
    send_command(device, '{"audio":{"out":{"equalizer":{"frequency":null}}}}')
    send_command(device, '{"audio":{"out":{"equalizer":{"q":null}}}}')
    send_command(device, '{"audio":{"out":{"equalizer":{"gain":null}}}}')
    send_command(device, '{"audio":{"out":{"equalizer":{"boost":null}}}}')


def print_header(device):
    ssc_transaction = device.send_ssc('{"device":{"name":null}}')
    y = json.loads(ssc_transaction.RX)
    print("Used Device:  " + str(y['device']['name']))
    print("IPv6 address: " + device.ip)


def handle_device(args, device):
    if args.brightness != None:
        send_command(
            device, '{"ui":{"logo":{"brightness":'+str(args.brightness)+'}}}')

    if args.delay != None:
        send_command(device, '{"audio":{"out":{"delay":'+str(args.delay)+'}}}')

    if args.dimm != None:
        send_command(device, '{"audio":{"out":{"dimm":'+f'{args.dimm:.1f}'+'}}}')

    if args.mute:
        send_command(device, '{"audio":{"out":{"mute":true}}}')

    if args.unmute:
        send_command(device, '{"audio":{"out":{"mute":false}}}')

    if args.save:
        send_command(device, '{"device":{"save_settings":true}}')

    if args.query:
        query_device(device)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scan', action="store_true",
                        help="scan for devices and ignore the khtool.json file")
    parser.add_argument('-q', '--query', action="store_true",
                        help="query loudspeaker(s)")
    parser.add_argument('--save', action="store_true",
                        help="performs a save_settings command to the devices")
    parser.add_argument('--brightness', action="store",
                        type=int, help="set logo brightness [0-100]")
    parser.add_argument('--delay', action="store", type=int,
                        help="set delay in 1/48khz samples [0-3360]")
    parser.add_argument('--dimm', action="store", type=float,
                        help="set dimm in dB [-120-0]")
    parser.add_argument('--mute', action="store_true", help="mute speaker(s)")
    parser.add_argument('--unmute', action="store_true",
                        help="unmute speaker(s)")
    parser.add_argument('-i', '--interface', action="store",
                        required=True, help='network interface to use (e.g. en0)')
    parser.add_argument('-t', '--target', action='store', default='all', choices=[
                        'all', '0', '1', '2', '3', '4', '5', '6', '7', '8'], help='use all speakers or only the selected one')

    args = parser.parse_args()

    if args.brightness:
        if args.brightness < 0 or args.brightness > 100:
            print("Error: brightness out of range [0-100]")
            exit(1)

    if args.delay:
        if args.delay < 0 or args.delay > 3360:
            print("Error: delay out of range [0-3360]")
            exit(1)

    if args.dimm:
        if args.dimm < -120 or args.dimm > 0:
            print("Error: dimm out of range [-120-0]")
            exit(1)

    if os.path.exists('khtool.json') and not args.scan:
        found_setup = ssc.Ssc_device_setup()
        found_setup.from_json('khtool.json')
    else:
        found_setup = ssc.scan()
        if found_setup is not None:
            found_setup.to_json('khtool.json')
            print("Found "+str(len(found_setup.ssc_devices)) +
                  " Device(s) and stored configuration to khtool.json.")
            exit(0)
        else:
            raise Exception("No SSC device setup found.")

    if args.target != 'all':

        if int(args.target) >= len(found_setup.ssc_devices):
            print("Target out of range. There are " +
                  str(len(found_setup.ssc_devices))+" speaker(s) in khtool.json.")
            exit(1)

        device = found_setup.ssc_devices[int(args.target)]
        device.connect(interface='%'+args.interface)

        print_header(device)
        handle_device(args, device)
        print("")

    else:
        found_setup.connect_all(interface='%'+args.interface)
        for ssc_device in found_setup.ssc_devices:
            print_header(ssc_device)
            handle_device(args, ssc_device)
            print("")


if __name__ == "__main__":
    main()
