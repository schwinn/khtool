#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyssc as ssc
import os
import json
import argparse
import time
import signal
import re


__author__ = "Thorsten Schwinn"
__version__ = "0.192"
__license__ = "MIT"


signal.signal(signal.SIGINT, lambda x, y: exit(1))
interface = ""


def send_command(device, str):
    x = get_interface(device)
    ssc_transaction = device.send_ssc(str, interface=x)
    if hasattr(ssc_transaction, "RX"):
        return ssc_transaction.RX.replace("\r\n", "")

    return


def send_print(device, str):
    print(send_command(device, str))


def send_add_array(device, str, y):
    x = get_interface(device)
    ssc_transaction = device.send_ssc(str, interface=x)

    if hasattr(ssc_transaction, "RX"):
        y.append(ssc_transaction.RX.replace("\r\n", ""))

    return y


def get_interface(device):
    pattern = "^fe80::"
    result = re.match(pattern, str(device.ip))
    if result:
        return interface
    else:
        return ""


def restore_device(device, db):
    if get_product(device) != db["product"]:
        print("Product name does not match.")
        exit(1)

    if get_serial(device) != db["serial"]:
        print("Serial number does not match.")
        exit(1)

    if get_version(device) != db["version"]:
        print("Version does not match.")
        exit(1)

    for i in db["commands"]:
        send_print(device, i)


def is_speaker(product):

    if product == "KH 80" or product == "KH 150" or product == "KH 120 II":
        return True

    return False


def query_commands(device):
    commands = []
    product = get_product(device)

    if product == "KH 750":
        version = get_version(device)
        pattern = "^1_0|^1_1"
        result = re.match(pattern, version)
        if result:
            kh750fwnew = 0
        else:
            kh750fwnew = 1
    else:
        kh750fwnew = -1

    if product == "KH 150" or product == "KH 120 II":
        version = get_version(device)
        pattern = "^1_0"
        result = re.match(pattern, version)
        if not result:
            commands += [
                '{"device":{"name":null}}',
                '{"device":{"identity":{"vendor":null}}}',
                '{"device":{"identity":{"product":null}}}',
                '{"device":{"identity":{"serial":null}}}',
                '{"device":{"identity":{"version":null}}}',
                '{"device":{"standby":{"enabled":null}}}',
                '{"device":{"standby":{"auto_standby_time":null}}}',
                '{"device":{"standby":{"level":null}}}',
                '{"device":{"standby":{"countdown":null}}}',
                '{"ui":{"logo":{"brightness":null}}}',
                '{"audio":{"in":{"interface":null}}}',
                '{"audio":{"in1":{"label":null}}}',
                '{"audio":{"in2":{"label":null}}}',
                '{"audio":{"out":{"level":null}}}',
                '{"audio":{"out":{"mute":null}}}',
                '{"audio":{"out":{"delay":null}}}',
                '{"audio":{"out":{"solo":null}}}',
                '{"audio":{"out":{"phaseinversion":null}}}',
                '{"audio":{"out":{"mixer":{"levels":null}}}}',
                '{"audio":{"out":{"mixer":{"inputs":null}}}}',
                '{"audio":{"out":{"eq2":{"enabled":null}}}}',
                '{"audio":{"out":{"eq2":{"type":null}}}}',
                '{"audio":{"out":{"eq2":{"frequency":null}}}}',
                '{"audio":{"out":{"eq2":{"q":null}}}}',
                '{"audio":{"out":{"eq2":{"gain":null}}}}',
                '{"audio":{"out":{"eq2":{"boost":null}}}}',
                '{"audio":{"out":{"eq2":{"desc":null}}}}',
                '{"audio":{"out":{"eq3":{"enabled":null}}}}',
                '{"audio":{"out":{"eq3":{"type":null}}}}',
                '{"audio":{"out":{"eq3":{"frequency":null}}}}',
                '{"audio":{"out":{"eq3":{"q":null}}}}',
                '{"audio":{"out":{"eq3":{"gain":null}}}}',
                '{"audio":{"out":{"eq3":{"boost":null}}}}',
                '{"audio":{"out":{"eq3":{"desc":null}}}}',
            ]

            return commands

    if product == "KH 750" and kh750fwnew == 1:
        commands += [
            '{"device":{"name":null}}',
            '{"device":{"identity":{"vendor":null}}}',
            '{"device":{"identity":{"product":null}}}',
            '{"device":{"identity":{"serial":null}}}',
            '{"device":{"identity":{"version":null}}}',
            '{"device":{"standby":{"enabled":null}}}',
            '{"device":{"standby":{"auto_standby_time":null}}}',
            '{"device":{"standby":{"level":null}}}',
            '{"device":{"standby":{"countdown":null}}}',
            '{"audio":{"in":{"delay":null}}}',
            '{"audio":{"in":{"interface":null}}}',
            '{"audio":{"in1":{"label":null}}}',
            '{"audio":{"in2":{"label":null}}}',
        ]

        for x in range(1, 6):
            if x != 5:
                commands += [
                    '{"audio":{"out' + str(x) + '":{"loudspeaker":null}}}',
                    '{"audio":{"out' + str(x) + '":{"label":null}}}',
                ]

            commands += [
                '{"audio":{"out' + str(x) + '":{"desc":null}}}',
                '{"audio":{"out' + str(x) + '":{"delay":null}}}',
                '{"audio":{"out' + str(x) + '":{"level":null}}}',
                '{"audio":{"out' + str(x) + '":{"mute":null}}}',
                '{"audio":{"out' + str(x) + '":{"mixer":{"levels":null}}}}',
                '{"audio":{"out' + str(x) + '":{"mixer":{"inputs":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq1":{"desc":null}}}}',
            ]

            for z in range(1, 3):
                commands += [
                    '{"audio":{"out' + str(x) + '":{"eq1":{"in' + str(z) + '":{"enabled":null}}}}}',
                    '{"audio":{"out' + str(x) + '":{"eq1":{"in' + str(z) + '":{"q":null}}}}}',
                    '{"audio":{"out' + str(x) + '":{"eq1":{"in' + str(z) + '":{"frequency":null}}}}}',
                    '{"audio":{"out' + str(x) + '":{"eq1":{"in' + str(z) + '":{"gain":null}}}}}',
                    '{"audio":{"out' + str(x) + '":{"eq1":{"in' + str(z) + '":{"type":null}}}}}',
                    '{"audio":{"out' + str(x) + '":{"eq1":{"in' + str(z) + '":{"input":null}}}}}',
                ]

            commands += [
                '{"audio":{"out' + str(x) + '":{"eq2":{"enabled":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq2":{"type":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq2":{"frequency":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq2":{"q":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq2":{"gain":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq2":{"boost":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq2":{"desc":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq3":{"enabled":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq3":{"type":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq3":{"frequency":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq3":{"q":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq3":{"gain":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq3":{"boost":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq3":{"desc":null}}}}',
            ]

        return commands

    commands += [
        '{"device":{"name":null}}',
        '{"device":{"identity":{"vendor":null}}}',
        '{"device":{"identity":{"product":null}}}',
        '{"device":{"identity":{"serial":null}}}',
        '{"device":{"identity":{"version":null}}}',
        '{"device":{"standby":{"enabled":null}}}',
        '{"device":{"standby":{"auto_standby_time":null}}}',
        '{"device":{"standby":{"level":null}}}',
    ]

    if is_speaker(product):
        commands += [
            '{"ui":{"logo":{"brightness":null}}}',
            '{"audio":{"in":{"gain":null}}}',
            '{"audio":{"in":{"phase_invert":null}}}',
        ]

    commands += [
        '{"audio":{"out":{"level":null}}}',
        '{"audio":{"out":{"dimm":null}}}',
        '{"audio":{"out":{"mute":null}}}',
    ]

    if is_speaker(product):
        commands += [
            '{"audio":{"out":{"delay":null}}}',
            '{"audio":{"out":{"solo":null}}}',
            '{"audio":{"out":{"phase_correction":null}}}',
            '{"audio":{"out":{"limiter_mode":null}}}',
            '{"audio":{"out":{"equalizer":{"enabled":null}}}}',
            '{"audio":{"out":{"equalizer":{"type":null}}}}',
            '{"audio":{"out":{"equalizer":{"frequency":null}}}}',
            '{"audio":{"out":{"equalizer":{"q":null}}}}',
            '{"audio":{"out":{"equalizer":{"gain":null}}}}',
            '{"audio":{"out":{"equalizer":{"boost":null}}}}',
        ]

    if product == "KH 750":
        commands += [
            '{"audio":{"in":{"analog":null}}}',
            '{"audio":{"in":{"delay":null}}}',
            '{"audio":{"in":{"interface":null}}}',
            '{"audio":{"in1":{"label":null}}}',
            '{"audio":{"in2":{"label":null}}}',
        ]

        for x in range(1, 6):
            if x != 5:
                commands += [
                    '{"audio":{"out' + str(x) + '":{"loudspeaker":null}}}',
                    '{"audio":{"out' + str(x) + '":{"on":null}}}',
                    '{"audio":{"out' + str(x) + '":{"label":null}}}',
                ]
            commands += [
                '{"audio":{"out' + str(x) + '":{"gain":null}}}',
                '{"audio":{"out' + str(x) + '":{"desc":null}}}',
                '{"audio":{"out' + str(x) + '":{"delay":null}}}',
                '{"audio":{"out' + str(x) + '":{"control":null}}}',
                '{"audio":{"out' + str(x) + '":{"mixer":{"levels":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq1":{"desc":null}}}}',
            ]

            for z in range(1, 3):
                commands += [
                    '{"audio":{"out' + str(x) + '":{"eq1":{"in' + str(z) + '":{"enabled":null}}}}}',
                    '{"audio":{"out' + str(x) + '":{"eq1":{"in' + str(z) + '":{"q":null}}}}}',
                    '{"audio":{"out' + str(x) + '":{"eq1":{"in' + str(z) + '":{"frequency":null}}}}}',
                    '{"audio":{"out' + str(x) + '":{"eq1":{"in' + str(z) + '":{"gain":null}}}}}',
                    '{"audio":{"out' + str(x) + '":{"eq1":{"in' + str(z) + '":{"type":null}}}}}',
                ]

            commands += [
                '{"audio":{"out' + str(x) + '":{"eq2":{"enabled":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq2":{"type":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq2":{"frequency":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq2":{"q":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq2":{"gain":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq2":{"boost":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq2":{"desc":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq3":{"enabled":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq3":{"type":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq3":{"frequency":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq3":{"q":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq3":{"gain":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq3":{"boost":null}}}}',
                '{"audio":{"out' + str(x) + '":{"eq3":{"desc":null}}}}',
            ]

    return commands


def backup_device(device, db):

    if hasattr(device, "connected"):
        if not device.connected:
            print("device " + str(device.ip) + " is not online")
            exit(1)

    product = get_product(device)

    commands = []
    for c in query_commands(device):
        send_add_array(device, c, commands)

    db[device.ip] = {"commands": []}
    db[device.ip]["commands"] = commands
    db[device.ip]["serial"] = get_serial(device)
    db[device.ip]["product"] = product
    db[device.ip]["vendor"] = get_vendor(device)
    db[device.ip]["version"] = get_version(device)

    return db


def query_device(device):
    print("*** query device settings ***")
    for c in query_commands(device):
        send_print(device, c)


def print_header(device):
    x = get_interface(device)
    ssc_transaction = device.send_ssc('{"device":{"name":null}}', interface=x)

    if hasattr(ssc_transaction, "RX"):
        y = json.loads(ssc_transaction.RX)
        print("Used Device:  " + str(y["device"]["name"]))
        print("IPv6 address: " + device.ip)


def get_product(device):
    x = get_interface(device)
    ssc_transaction = device.send_ssc(
        '{"device":{"identity":{"product":null}}}', interface=x
    )

    if hasattr(ssc_transaction, "RX"):
        y = json.loads(ssc_transaction.RX)
        return str(y["device"]["identity"]["product"])

    return ""


def get_serial(device):
    x = get_interface(device)
    ssc_transaction = device.send_ssc(
        '{"device":{"identity":{"serial":null}}}', interface=x
    )

    if hasattr(ssc_transaction, "RX"):
        y = json.loads(ssc_transaction.RX)
        return str(y["device"]["identity"]["serial"])

    return ""


def get_version(device):
    x = get_interface(device)
    ssc_transaction = device.send_ssc(
        '{"device":{"identity":{"version":null}}}', interface=x
    )

    if hasattr(ssc_transaction, "RX"):
        y = json.loads(ssc_transaction.RX)
        return str(y["device"]["identity"]["version"])

    return ""


def get_vendor(device):
    x = get_interface(device)
    ssc_transaction = device.send_ssc(
        '{"device":{"identity":{"vendor":null}}}', interface=x
    )

    if hasattr(ssc_transaction, "RX"):
        y = json.loads(ssc_transaction.RX)
        return str(y["device"]["identity"]["vendor"])

    return ""


def handle_device(args, device):

    if hasattr(device, "connected"):
        if not device.connected:
            x = get_interface(device)
            print("device " + str(device.ip) + " is not online")
            print("Used interface: " + x)
            exit(1)

    product = get_product(device)

    if product == "KH 750":
        version = get_version(device)
        pattern = "^1_0|^1_1"
        result = re.match(pattern, version)
        if result:
            kh750fwnew = 0
        else:
            kh750fwnew = 1
    else:
        kh750fwnew = -1

    if args.query:
        query_device(device)
        return

    if args.brightness != None:
        send_print(
            device, '{"ui":{"logo":{"brightness":' + str(args.brightness) + "}}}"
        )

    if args.delay != None:
        send_print(device, '{"audio":{"out":{"delay":' + str(args.delay) + "}}}")

    if args.dimm != None:
        send_print(device, '{"audio":{"out":{"dimm":' + f"{args.dimm:.1f}" + "}}}")

    if args.level != None:
        if kh750fwnew == 1:
            send_print(
                device, '{"audio":{"out5":{"level":' + f"{args.level:.1f}" + "}}}"
            )
        else:
            send_print(
                device, '{"audio":{"out":{"level":' + f"{args.level:.1f}" + "}}}"
            )

    if args.mute:
        if product == "KH 750" and kh750fwnew == 1:
            send_print(device, '{"audio":{"out5":{"mute":true}}}')
        else:
            send_print(device, '{"audio":{"out":{"mute":true}}}')

    if args.unmute:
        if product == "KH 750" and kh750fwnew == 1:
            send_print(device, '{"audio":{"out5":{"mute":false}}}')
        else:
            send_print(device, '{"audio":{"out":{"mute":false}}}')

    if args.expert:
        send_print(device, args.expert)

    if args.save:
        if product != "KH 80": 
            print("Save is not supported on this device.")
        else:
            send_print(device, '{"device":{"save_settings":true}}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scan",
        action="store_true",
        help="scan for devices and ignore the khtool.json file",
    )
    parser.add_argument(
        "-q", "--query", action="store_true", help="query loudspeaker(s)"
    )
    parser.add_argument(
        "--backup",
        action="store",
        help="generate json backup of loudspeaker(s) and save it to [filename]",
    )
    parser.add_argument(
        "--restore", action="store", help="restore configuration from [filename]"
    )
    parser.add_argument("--comment", action="store", help="comment for backup file")
    parser.add_argument(
        "--save",
        action="store_true",
        help="performs a save_settings command to the devices (only for KH 80/KH 150/KH 120 II)",
    )
    parser.add_argument(
        "--brightness",
        action="store",
        type=int,
        help="set logo brightness [0-100] (only for KH 80/KH 150/KH 120 II)",
    )
    parser.add_argument(
        "--delay",
        action="store",
        type=int,
        help="set delay in 1/48khz samples [0-3360]",
    )
    parser.add_argument(
        "--dimm", action="store", type=float, help="set dimm in dB [-120-0]"
    )
    parser.add_argument(
        "--level", action="store", type=float, help="set level in dB [0-120]"
    )
    parser.add_argument("--mute", action="store_true", help="mute speaker(s)")
    parser.add_argument("--unmute", action="store_true", help="unmute speaker(s)")
    parser.add_argument("--expert", action="store", help="send a custom command")
    parser.add_argument(
        "-i",
        "--interface",
        action="store",
        required=True,
        help="network interface to use (e.g. en0)",
    )
    parser.add_argument(
        "-t",
        "--target",
        action="store",
        default="all",
        choices=["all", "0", "1", "2", "3", "4", "5", "6", "7", "8"],
        help="use all speakers or only the selected one",
    )
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + __version__
    )
    args = parser.parse_args()

    global interface
    interface = "%" + args.interface

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

    if args.level:
        if args.level < 0 or args.level > 120:
            print("Error: level out of range [0-120]")
            exit(1)

    if os.path.exists("khtool.json") and not args.scan:
        found_setup = ssc.Ssc_device_setup()
        found_setup.from_json("khtool.json")
    else:
        found_setup = ssc.scan(scan_time_seconds=10)
        if found_setup is not None:
            found_setup.to_json("khtool.json")
            print(
                "Found "
                + str(len(found_setup.ssc_devices))
                + " Device(s) and stored configuration to khtool.json."
            )
            exit(0)
        else:
            raise Exception("No SSC device setup found.")

    if args.backup:
        devicedb = {}
        if args.target != "all":

            if int(args.target) >= len(found_setup.ssc_devices):
                print(
                    "Target out of range. There are "
                    + str(len(found_setup.ssc_devices))
                    + " speaker(s) in khtool.json."
                )
                exit(1)

            device = found_setup.ssc_devices[int(args.target)]
            x = get_interface(device)
            device.connect(interface=x)
            devicedb = backup_device(device, devicedb)
        else:
            for device in found_setup.ssc_devices:
                x = get_interface(device)
                device.connect(interface=x)
                devicedb = backup_device(device, devicedb)

        backup = {"devices": devicedb}
        backup["timestamp"] = int(time.time())
        backup["timelocal"] = time.ctime(time.time())
        backup["version"] = __version__
        if args.comment is not None:
            backup["comment"] = args.comment
        else:
            backup["comment"] = ""

        json_object = json.dumps(backup, indent=4)

        if args.backup != "-":
            with open(args.backup, "w") as outfile:
                outfile.write(json_object)
        else:
            print(json_object)

        exit(0)

    if args.restore:

        f = open(args.restore)
        data = json.load(f)
        f.close()

        if args.target != "all":

            if int(args.target) >= len(found_setup.ssc_devices):
                print(
                    "Target out of range. There are "
                    + str(len(found_setup.ssc_devices))
                    + " speaker(s) in khtool.json."
                )
                exit(1)

            device = found_setup.ssc_devices[int(args.target)]
            x = get_interface(device)
            device.connect(interface=x)

            if hasattr(device, "connected"):
                if not device.connected:
                    print("device " + str(device.ip) + " is not online")
                    exit(1)

            restore_device(device, data["devices"][device.ip])
        else:
            for device in found_setup.ssc_devices:
                x = get_interface(device)
                device.connect(interface=x)

                if hasattr(device, "connected"):
                    if not device.connected:
                        print("device " + str(device.ip) + " is not online")
                        exit(1)

                if device.ip in data["devices"]:
                    restore_device(device, data["devices"][device.ip])

        exit(0)

    if args.target != "all":

        if int(args.target) >= len(found_setup.ssc_devices):
            print(
                "Target out of range. There are "
                + str(len(found_setup.ssc_devices))
                + " speaker(s) in khtool.json."
            )
            exit(1)

        device = found_setup.ssc_devices[int(args.target)]
        x = get_interface(device)
        device.connect(interface=x)

        print_header(device)
        handle_device(args, device)
        print("")

    else:
        for device in found_setup.ssc_devices:
            x = get_interface(device)
            device.connect(interface=x)
            print_header(device)
            handle_device(args, device)
            print("")


if __name__ == "__main__":
    main()
