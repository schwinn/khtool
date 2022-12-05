import pyssc as ssc
import os
import json
import argparse

def ssccommand(device, str ):
   ssc_transaction = device.send_ssc(str)
   print (ssc_transaction['RX'].replace("\r\n",""))


def query(device):
  print ("*** query device settings ***")
  ssccommand(device, '{"device":{"name":null}}')
  ssccommand(device, '{"device":{"identity":{"vendor":null}}}')
  ssccommand(device, '{"device":{"identity":{"product":null}}}')
  ssccommand(device, '{"device":{"identity":{"serial":null}}}')
  ssccommand(device, '{"device":{"identity":{"version":null}}}')
  ssccommand(device, '{"ui":{"logo":{"brightness":null}}}')
  ssccommand(device, '{"audio":{"in":{"gain":null}}}')
  ssccommand(device, '{"audio":{"in":{"phase_invert":null}}}')
  ssccommand(device, '{"audio":{"out":{"level":null}}}')
  ssccommand(device, '{"audio":{"out":{"dimm":null}}}')
  ssccommand(device, '{"audio":{"out":{"delay":null}}}')
  ssccommand(device, '{"audio":{"out":{"mute":null}}}')
  ssccommand(device, '{"audio":{"out":{"solo":null}}}')
  ssccommand(device, '{"audio":{"out":{"phase_correction":null}}}')
  ssccommand(device, '{"audio":{"out":{"limiter_mode":null}}}')
  ssccommand(device, '{"audio":{"out":{"equalizer":{"enabled":null}}}}')
  ssccommand(device, '{"audio":{"out":{"equalizer":{"type":null}}}}')
  ssccommand(device, '{"audio":{"out":{"equalizer":{"frequency":null}}}}')
  ssccommand(device, '{"audio":{"out":{"equalizer":{"q":null}}}}')
  ssccommand(device, '{"audio":{"out":{"equalizer":{"gain":null}}}}')
  ssccommand(device, '{"audio":{"out":{"equalizer":{"boost":null}}}}')


def printheader(device):
  ssc_transaction = device.send_ssc('{"device":{"name":null}}')
  y = json.loads(ssc_transaction['RX'])
  print("Used Device:  " + str(y['device']['name']))
  print("IPv6 address: " + device.ip)


def handledevice(args, device):
  if args.brightness!=None:
    ssccommand(device, '{"ui":{"logo":{"brightness":'+str(args.brightness)+'}}}')

  if args.delay!=None:
    ssccommand(device, '{"audio":{"out":{"delay":'+str(args.delay)+'}}}')

  if args.save:
    ssccommand('{"device":{"save_settings":true}}')

  if args.query:
    query(device)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--scan', action="store_true", help="scan for devices and ignore the khtool.json file")
  parser.add_argument('-q','--query', action="store_true", help="query loudspeaker(s)")
  parser.add_argument('--save', action="store_true", help="performs a save_settings command to the devices")
  parser.add_argument('--brightness', action="store", type=int, help="set logo brightness [0-100]")
  parser.add_argument('--delay', action="store", type=int, help="set delay in 1/48khz samples [0-3360]")
  parser.add_argument('-i', '--interface', action="store", required=True, help='network interface to use (e.g. en0)')
  parser.add_argument('-t', '--target', action='store', default='all', choices=['all','0','1','2','3','4','5','6','7','8'], help='use all speakers or only the selected one')

  args = parser.parse_args()

  if args.brightness:
    if args.brightness<0 or args.brightness>100:
      print ("Error: brightness out of range [0-100]")
      exit(1)

  if args.delay:
    if args.delay<0 or args.delay>3360:
      print ("Error: delay out of range [0-3360]")
      exit(1)

  if os.path.exists('khtool.json') and not args.scan:
    found_setup = ssc.Ssc_device_setup()
    found_setup.from_json('khtool.json')
  else:
    found_setup = ssc.scan()
    if found_setup is not None:
        found_setup.to_json('khtool.json')
    else:
        raise Exception("No SSC device setup found.")

  if args.target != 'all':
	
    if int(args.target) >= len(found_setup.ssc_devices):
        print("Target out of range. There are "+str(len(found_setup.ssc_devices))+" speaker(s) in khtool.json.")
        exit(1)

    device=found_setup.ssc_devices[int(args.target)]
    device.connect(interface='%'+args.interface)

    printheader(device)
    handledevice(args, device)
    print("")

  else:
    found_setup.connect_all(interface='%'+args.interface)
    for ssc_device in found_setup.ssc_devices:
      printheader(ssc_device)
      handledevice(args, ssc_device)
      print("")


if __name__ == "__main__":
  main()
