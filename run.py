import argparse

from app.cycle_battery import CycleBattery


def main(state, address_on, address_off, ip_address=None, only_drain=False):
    if state == CycleBattery.HTTP:
        if address_on and address_off:
            print(f"HTTP state selected with address_on: {address_on}, address_off: {address_off}")
        else:
            print("Error: address os and off are required for the 'HTTP' method")
            return
    elif state == CycleBattery.TASMOTA:
        if ip_address is None:
            print("Error: IP address is required for the 'Tasmota' method.")
            return
        print(f"Tasmota method selected with IP address: {ip_address}")
    else:
        print("Invalid state. State must be 'HTTP' or 'Tasmota'.")
        return

    cycle_battery = CycleBattery(state, address_on, address_off, ip_address, only_drain)
    cycle_battery.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process arguments for HTTP/Tasmota")

    parser.add_argument("state", choices=CycleBattery.STATES, help="Select state (HTTP or Tasmota)")
    parser.add_argument("--address_on", help="Address for turning on the device (HTTP state only)")
    parser.add_argument("--address_off", help="Address for turning off the device (HTTP state only)")
    parser.add_argument("--ip_address", help="IP address of the device (Tasmota state only)")
    parser.add_argument("--only_drain", help="Only drain battery", action="store_true")

    args = parser.parse_args()

    main(args.state, args.address_on, args.address_off, args.ip_address, args.only_drain)
