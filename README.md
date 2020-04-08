# ruuvi.nrflabeler.py
Print QR code with MAC address of NRF52 device

# Install
Download and install [Dymo SDK](https://www.dymo.com/en-US/online-support/online-support-sdk). 

Install required Python packages by `pip3 install -r requirements.txt`.

Install submodules with `git submodule update --init`

# Usage
Run `python3 main.py --help` to show all the possible arguments.

The program reads MAC address of nRF52 and sends the address to labelwriter as a QR code.
You can additionally specify a firmware which has softdevice, bootloader and application to 
flash on RuuviTag. If you flash the firmware, the firmware filename is added to QR-code.

If you want to include a logo, you can use `--icon` + png file. 

If you don't specify `--print` only a preview is generated instead of the label. 
If you specify `--print` and `--preview` you'll get a preview before starting the print.