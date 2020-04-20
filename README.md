# ruuvi.nrflabeler.py
Print QR code with MAC address of NRF52 device

# Install
Download and install [Dymo SDK](https://www.dymo.com/en-US/online-support/online-support-sdk). 

Install required Python packages by `pip3 install -r requirements.txt`.

# Usage
Generate a DYMO XML label with Dymo Connect software. Be sure to save the file with UTF-8 encoding
and convert the encoding if necessary. If you enter "xx:xx:xx:xx:xx:xx" to the label template,
it will get replaced by the MAC address of the tag. This also works on text inside QR code.
String "SENSOR" will get replaced by text argument provided in commandline. 

The program reads MAC address of nRF52 and sends the address to labelwriter as a QR code.
You can additionally specify a firmware which has softdevice, bootloader and application to 
flash on RuuviTag.

Run `python3 main.py --help` to show all the possible arguments.

A full example: `python3 main.py --text "RuuviTag" --fw ruuvi_firmware_full_2.5.9.hex --print sample.dymo`
__note__ on Windows machines, use `python` instead of `python3`
