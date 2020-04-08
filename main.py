import subprocess as proc
import sys
import os

from pynrfjprog import HighLevel

import argparse

# setup command-line arguments
parser = argparse.ArgumentParser("Flash and print label for NRF52 device")
parser.add_argument('--text', type=str, help="Text")
parser.add_argument('--icon', type=str, help="Optional png icon file")
parser.add_argument('--print', action='store_true', help="Print label")
parser.add_argument('--preview', action='store_true', help="Show a preview of the generated pdf")
parser.add_argument('--size', type=str, default='normal', help="One of ['small', 'normal']")
parser.add_argument('--font_size', type=int, default=10)
parser.add_argument('--font', type=str, default='Helvetica')
parser.add_argument('--fw', type=str, help='Firmware to flash')
args = parser.parse_args()

FICR_BASE = 0x10000000
DEVICEADDR0 = 0xA4
DEVICEADDR1 = 0xA8

def ficr2mac(addr0, addr1):
  mac = addr0
  mac += addr1<<32
  mac |= 0x0000C00000000000
  mac &= 0x0000FFFFFFFFFFFF
  return mac

def mac2str(mac):
  str = ""
  str += hex((mac>>40) & 0xFF) + ":"
  str += hex((mac>>32) & 0xFF) + ":"
  str += hex((mac>>24) & 0xFF) + ":"
  str += hex((mac>>16) & 0xFF) + ":"
  str += hex((mac>>8) & 0xFF) + ":"
  str += hex((mac>>0) & 0xFF)
  return str.upper().replace("0X", "").upper()

api = HighLevel.API()
api.open()

# Find connected probes
probes = api.get_connected_probes()
# TODO: Verify there is exactly one probe connected
snr = probes[0]
# To program J-Link probe at snr <snr>:
probe = HighLevel.DebugProbe(api, snr)
# Read MAC Address
addr0 = probe.read(FICR_BASE + DEVICEADDR0)
addr1 = probe.read(FICR_BASE + DEVICEADDR1)
mac = ficr2mac(addr0, addr1)
mac_str = mac2str(mac)
print('DeviceAddr: ', mac_str)
# Launch label printing
labelgen_path = os.path.join('dymo-labelgen', 'main.py')
runcmd = ["python3", labelgen_path]
if args.print and not args.preview:
  runcmd.append("--noconfirm")

if args.print:
  runcmd.append("--print")
  runcmd.append("--noconfirm")

if not args.print or args.preview:
  runcmd.append("--preview")

if args.font_size:
  runcmd.append("--font")
  runcmd.append(args.font)

if args.font:
  runcmd.append("--font_size")
  runcmd.append(str(args.font_size))

if args.icon:
  runcmd.append("--icon")
  runcmd.append(args.icon)

if args.text:
  runcmd.append(args.text)
else:
  runcmd.append(" ")

runcmd.append("--qr")
qr_str = "MAC: " + mac_str
if args.fw:
  qr_str += "\nFW: " + args.fw

runcmd.append(qr_str)

print("Writing label:")  
print(runcmd)
proc.run(runcmd)

# Program device
if args.fw:
  print("Flashing nRF52 device")
  probe.erase(HighLevel.EraseAction.ERASE_ALL)
  probe.program(args.fw)
  print("Verifying nRF52 device")
  probe.verify(args.fw)
  print("Done.")
  probe.reset(HighLevel.ResetAction.RESET_PIN)
api.close()

