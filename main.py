import subprocess as proc
import sys

from pynrfjprog import HighLevel

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
  return str.upper().replace("0X", "")

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
probe.erase(HighLevel.EraseAction.ERASE_ALL)
probe.program("ruuvi_firmware_full_2.5.9.hex")
probe.reset(HighLevel.ResetAction.RESET_PIN)
api.close()

