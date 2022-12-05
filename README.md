# khtool
This is a simple tool for querying or changing the settings of Neumann KH loudspeakers via the Sennheiser Sound Control Protocol. 

## Libraries Required

1. pyssc `pip3 install pyssc`

## Usage

You must specify the name of the network interface to which the speakers are connected.
```shell
python3 ./khtool.py -i [interface name]
```

## Examples

Query speakers

```shell
python3 ./khtool.py -i en0 -q
*** Device: Right ***
IPv6 address: fe80::2a36:38ff:fexx:xxxx
{"device":{"identity":{"vendor":"Georg Neumann GmbH"}}}
{"device":{"identity":{"product":"KH 80"}}}
{"device":{"identity":{"serial":"6372436xxx000000"}}}
{"device":{"identity":{"version":"1_3_1"}}}
{"ui":{"logo":{"brightness":50}}}
{"audio":{"in":{"gain":0.0}}}
{"audio":{"in":{"phase_invert":false}}}
{"audio":{"out":{"level":90.0}}}
{"audio":{"out":{"dimm":0.0}}}
{"audio":{"out":{"delay":0}}}
{"audio":{"out":{"mute":false}}}
{"audio":{"out":{"solo":false}}}
{"audio":{"out":{"phase_correction":true}}}
{"audio":{"out":{"limiter_mode":1}}}
{"audio":{"out":{"equalizer":{"enabled":[true,true,true,true,true,true,true,true,true,true]}}}}
{"audio":{"out":{"equalizer":{"type":["PARAMETRIC","PARAMETRIC","PARAMETRIC","PARAMETRIC","PARAMETRIC","PARAMETRIC","PARAMETRIC","PARAMETRIC","PARAMETRIC","PARAMETRIC"]}}}}
{"audio":{"out":{"equalizer":{"frequency":[134.243,166.792,67.255,111.412,78.469,1224.043,643.824,93.657,17999.688,51.878]}}}}
{"audio":{"out":{"equalizer":{"q":[8.428,2.800,7.905,10.234,9.120,3.191,2.952,12.886,0.370,6.385]}}}}
{"audio":{"out":{"equalizer":{"gain":[0.752,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000]}}}}
{"audio":{"out":{"equalizer":{"boost":[-9.776,-8.757,-9.036,4.752,3.933,-2.062,1.176,3.494,-0.523,1.308]}}}}

*** Device: Left ***
IPv6 address: fe80::2a36:38ff:fexx:xxxx
{"device":{"identity":{"vendor":"Georg Neumann GmbH"}}}
{"device":{"identity":{"product":"KH 80"}}}
{"device":{"identity":{"serial":"6382437xxx000000"}}}
{"device":{"identity":{"version":"1_3_1"}}}
{"ui":{"logo":{"brightness":50}}}
{"audio":{"in":{"gain":0.0}}}
{"audio":{"in":{"phase_invert":false}}}
{"audio":{"out":{"level":90.0}}}
{"audio":{"out":{"dimm":0.0}}}
{"audio":{"out":{"delay":0}}}
{"audio":{"out":{"mute":false}}}
{"audio":{"out":{"solo":false}}}
{"audio":{"out":{"phase_correction":true}}}
{"audio":{"out":{"limiter_mode":1}}}
{"audio":{"out":{"equalizer":{"enabled":[true,true,true,true,true,true,true,true,true,true]}}}}
{"audio":{"out":{"equalizer":{"type":["PARAMETRIC","PARAMETRIC","PARAMETRIC","PARAMETRIC","PARAMETRIC","PARAMETRIC","PARAMETRIC","PARAMETRIC","PARAMETRIC","PARAMETRIC"]}}}}
{"audio":{"out":{"equalizer":{"frequency":[64.476,106.976,98.223,134.101,167.905,49.531,1186.596,78.141,17998.848,198.220]}}}}
{"audio":{"out":{"equalizer":{"q":[16.000,0.394,16.000,12.241,9.646,2.097,3.225,9.464,0.381,15.957]}}}}
{"audio":{"out":{"equalizer":{"gain":[0.737,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000]}}}}
{"audio":{"out":{"equalizer":{"boost":[-3.625,-3.019,-3.020,-6.370,-7.147,2.581,-2.239,3.464,-0.529,-4.120]}}}}
```

Set logo brightness
```shell
python3 ./khtool.py -i en0 --brightness 50
*** Device: Right ***
{"ui":{"logo":{"brightness":50}}}

*** Device: Left ***
{"ui":{"logo":{"brightness":50}}}
```

Mute speakers
```shell
python3 ./khtool.py -i en0 --mute
Used Device:  Right
IPv6 address: fe80::2a36:38ff:fexx:xxxx
{"audio":{"out":{"mute":true}}}
```

Unmute speakers
```shell
python3 ./khtool.py -i en0 --unmute
Used Device:  Right
IPv6 address: fe80::2a36:38ff:fexx:xxxx
{"audio":{"out":{"mute":false}}}
```

Save settings
```shell
python3 ./khtool.py -i en0 --save         
*** Device: Right ***
{"device":{"save_settings":true}}

*** Device: Left ***
{"device":{"save_settings":true}}
```

Print help
```shell
python3 ./khtool.py -h           
usage: khtool.py [-h] [--scan] [-q] [--save] [--brightness BRIGHTNESS] [--delay DELAY] [--mute] [--unmute] -i INTERFACE [-t {all,0,1,2,3,4,5,6,7,8}]

options:
  -h, --help            show this help message and exit
  --scan                scan for devices and ignore the khtool.json file
  -q, --query           query loudspeaker(s)
  --save                performs a save_settings command to the devices
  --brightness BRIGHTNESS
                        set logo brightness [0-100]
  --delay DELAY         set delay in 1/48khz samples [0-3360]
  --mute                mute speaker(s)
  --unmute              unmute speaker(s)
  -i INTERFACE, --interface INTERFACE
                        network interface to use (e.g. en0)
  -t {all,0,1,2,3,4,5,6,7,8}, --target {all,0,1,2,3,4,5,6,7,8}
                        use all speakers or only the selected one
``` 


## Note

The tool was only tested with a pair of Neumann KH 80 DSP speakers under macOS Monterey. Python3 must be installed on macOS to use the tool. Communication with the speakers is exclusively via IPv6. Therefore, it must be activated in the operating system.

Use at your own risk. 
