# Battery Cycle

This application will drain the battery on your MacBook for one battery cycle.
The MacBook must be linked to a power source, and the power source must be connected to a Smart Plug Socket.

During normal operation, the application will charge the computer to 100% before sending a command to switch off the smart plug.

The application will prevent the computer from sleeping and will wait until the battery is down to 5% before turning on the smart plug.

Tasmota Smart Plug was used for testing.

DECLAIMER: Do not run it every day!

Note: The application will not put any stress on the CPU, so you can continue working normally while it is running. 

## Installation

Clone the repo:
git clone https://github.com/oferpaster/cycle_battery.git

Get inside the new directory:
cd cycle_battery/

Install requirements:
pip install -r requirements.txt

```bash
git clone https://github.com/oferpaster/cycle_battery.git
cd cycle_battery/
pip install -r requirements.txt
```

## Usage

```
usage: run.py [-h] [--address_on ADDRESS_ON] [--address_off ADDRESS_OFF] [--ip_address IP_ADDRESS] [--only_drain] {HTTP,Tasmota}

Process arguments for HTTP/Tasmota

positional arguments:
  {HTTP,Tasmota}        Select state (HTTP or Tasmota)

optional arguments:
  -h, --help            show this help message and exit
  --address_on ADDRESS_ON
                        Address for turning on the device (HTTP state only)
  --address_off ADDRESS_OFF
                        Address for turning off the device (HTTP state only)
  --ip_address IP_ADDRESS
                        IP address of the device (Tasmota state only)
  --only_drain          Only drain battery
```
Example:

Using Tasmota:
```
python run.py Tasmota --ip_address 192.168.31.158
```

Using HTTP:
```
python run.py HTTP --address_on http://XXXXXX/plug_on --address_off http://XXXXXX/plug_on
```

Drain Only Mode:
In this mode computer won’t charge to 100% it will only cut the power source and wait for 5 %
```
python run.py Tasmota --ip_address 192.168.31.158 --only_drain
```

Note: Every 5 minutes, the battery level will be displayed on the screen; if you quit the terminal while the application is running, the drain process will be stopped and the power supply will be restored to on.
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)