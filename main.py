import subprocess as proc
import sys
import os
import requests

from pynrfjprog import HighLevel

import argparse

# setup command-line arguments
parser = argparse.ArgumentParser("Flash and print label for NRF52 device")
parser.add_argument('--text', type=str, help="Text")
parser.add_argument('--print', type=str, help="Print label from template file. 'xx:xx:xx:xx:xx:xx' is replaced with MAC address and 'SENSOR' is replaced with text argument" )
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

if len(probes) is not 1:
  print("Error, expected 1 nRF device to be connected, found: " + str(len(probes)))
  sys.exit(1)
snr = probes[0]
# To program J-Link probe at snr <snr>:
probe = HighLevel.DebugProbe(api, snr)
# Read MAC Address
addr0 = probe.read(FICR_BASE + DEVICEADDR0)
addr1 = probe.read(FICR_BASE + DEVICEADDR1)
mac = ficr2mac(addr0, addr1)
mac_str = mac2str(mac)
print('DeviceAddr: ', mac_str)

if args.print:
  labelXml = ""
  with open(args.print, 'r') as myfile:
    labelXml = myfile.read()

  labelXml = labelXml.replace("xx:xx:xx:xx:xx:xx", mac_str)

  if args.text:
    labelXml = labelXml.replace("SENSOR", args.text)
  else:
    labelXml = labelXml.replace("SENSOR", "")

  print(labelXml)

  url = "https://127.0.0.1:41951/DYMO/DLS/Printing/PrintLabel"
  labelData = {
    "printerName": "DYMO LabelWriter 450",
    "labelXml": labelXml,
    "labelSetXml": ""
  }
  x = requests.post(url, data = labelData, verify = False)

  print(x.text)

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

