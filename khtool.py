import pyssc as ssc
import os
import json
import argparse

def ssccommand( str ):
   ssc_transaction = device.send_ssc(str)
   print (ssc_transaction['RX'].replace("\r\n",""))
   return

parser = argparse.ArgumentParser()
parser.add_argument('--scan', action="store_true", help="scan for devices and ignore the setup.json file")
parser.add_argument('--save', action="store_true", help="performs a save_settings command to the devices")
parser.add_argument('--brightness', action="store", type=int, help="set logo brightness [0-100]")
parser.add_argument('-i', '--interface', action="store", required=True, help='network interface to use (e.g. en0)')

args = parser.parse_args()

if args.brightness:
  if args.brightness<0 or args.brightness>100:
    print ("Error: brightness out of range [0-100]")

    exit(1)

if os.path.exists('setup.json') and not args.scan:
    found_setup = ssc.Ssc_device_setup()
    found_setup.from_json('setup.json')
else:
    found_setup = ssc.scan()
    if found_setup is not None:
        found_setup.to_json('setup.json')
    else:
        raise Exception("No SSC device setup found.")
found_setup.connect_all(interface='%'+args.interface)

for ssc_device in found_setup.ssc_devices:

  device = ssc_device

  ssc_transaction = device.send_ssc('{"device":{"name":null}}')
  y = json.loads(ssc_transaction['RX'])
  print("*** Device: " +str(y['device']['name'])+" ***")

  if args.brightness:
    ssccommand('{"ui":{"logo":{"brightness":'+str(args.brightness)+'}}}')

  if args.save:
    ssccommand('{"device":{"save_settings":true}}')

  if args.save or args.brightness:
    print("")
    continue

  print("IPv6 address: " + device.ip)
 
  ssccommand('{"device":{"identity":{"vendor":null}}}')
  ssccommand('{"device":{"identity":{"product":null}}}')
  ssccommand('{"device":{"identity":{"serial":null}}}')
  ssccommand('{"device":{"identity":{"version":null}}}')
  ssccommand('{"ui":{"logo":{"brightness":null}}}')
  ssccommand('{"audio":{"in":{"gain":null}}}')
  ssccommand('{"audio":{"in":{"phase_invert":null}}}')
  ssccommand('{"audio":{"out":{"level":null}}}')
  ssccommand('{"audio":{"out":{"dimm":null}}}')
  ssccommand('{"audio":{"out":{"delay":null}}}')
  ssccommand('{"audio":{"out":{"mute":null}}}')
  ssccommand('{"audio":{"out":{"solo":null}}}')
  ssccommand('{"audio":{"out":{"phase_correction":null}}}')
  ssccommand('{"audio":{"out":{"limiter_mode":null}}}')
  ssccommand('{"audio":{"out":{"equalizer":{"enabled":null}}}}')
  ssccommand('{"audio":{"out":{"equalizer":{"type":null}}}}')
  ssccommand('{"audio":{"out":{"equalizer":{"frequency":null}}}}')
  ssccommand('{"audio":{"out":{"equalizer":{"q":null}}}}')
  ssccommand('{"audio":{"out":{"equalizer":{"gain":null}}}}')
  ssccommand('{"audio":{"out":{"equalizer":{"boost":null}}}}')

  print("")

