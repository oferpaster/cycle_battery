import asyncio
import argparse
import subprocess
from time import sleep, time
from tasmotadevicecontroller import TasmotaDevice
from tasmotadevicecontroller import tasmota_types as t

import psutil
import requests


class TasmotaControll(object):

    def __init__(self, device_ip):
        self.device_ip = device_ip
        self.loop = None

    async def _set_power(self, state):
        device = await TasmotaDevice.connect(self.device_ip)
        await device.setPower(state)

    def power_on(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self._set_power(t.PowerType.ON))

    def power_off(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self._set_power(t.PowerType.OFF))


class CycleBattery(object):

    HTTP = "HTTP"
    TASMOTA = "Tasmota"
    STATES = [HTTP, TASMOTA]

    def __init__(self, state, address_on=None, address_off=None, ip_address=None, only_drain=False):
        self.state = state
        self.only_drain = only_drain
        self.address_on = address_on
        self.address_off = address_off
        self.ip_address = ip_address
        self.percent = None
        self.power_plugged = None
        self.caffeinate_process = None
        self.has_power_source = True
        self.tasmota = None
        if self.state == 'Tasmota' and ip_address:
            self.tasmota = TasmotaControll(ip_address)

    def turn_device_on(self):
        print('Turning on Power Source')
        if self.state == self.HTTP:
            requests.get(self.address_on)
        else:
            self.tasmota.power_on()

    def turn_device_off(self):
        print('Turning off Power Source')
        if self.state == self.HTTP:
            requests.get(self.address_off)
        else:
            self.tasmota.power_off()

    def get_battery_info(self):
        battery = psutil.sensors_battery()
        if battery:
            self.percent = battery.percent
            self.power_plugged = battery.power_plugged
            return self.percent, self.power_plugged
        else:
            return None, None

    def loop_battery_info(self, count, msg=None):
        self.percent, self.power_plugged = self.get_battery_info()
        if self.percent is not None:
            if count == 5:
                print(f'Macbook battery level: {self.percent}{", " + msg if msg else ""}')
                count = 0
            else:
                count += 1
            sleep(60)
        else:
            print("Unable to retrieve battery information.")
        return self.percent, count

    def do_battery_drain(self):
        print('Start Drain Battery')
        self.turn_device_off()
        percent = 100
        count = 0
        print('Starting battery cycle...')
        while percent > 5:
            percent, count = self.loop_battery_info(count)

    def wait_for_full_battery(self):
        percent, power_plugged = self.get_battery_info()
        if percent != 100:
            print('Force OSX to fully charge the computer')
            self.turn_device_off()
            sleep(10)
            self.turn_device_on()
        else:
            print('Fully charged')
            return

        count = 0
        while percent != 100:
            percent, count = self.loop_battery_info(count, msg='Waiting For Full Charge')

    def check_precondition(self):
        percent, power_plugged = self.get_battery_info()
        if not power_plugged:
            self.turn_device_on()
            sleep(10)
            percent, power_plugged = self.get_battery_info()
            if not power_plugged:
                self.has_power_source = False
        return self.has_power_source

    def run(self):
        try:
            if self.check_precondition():
                self.caffeinate_process = subprocess.Popen(["caffeinate", "-d"])
                if not self.only_drain:
                    self.wait_for_full_battery()
                else:
                    print('Only Daring battery mode')
                start_time = time()
                self.do_battery_drain()
                elapsed_time = time() - start_time
                print(f"Drain(drain part only) took {elapsed_time / 60} minutes to run.")
            else:
                print('Skipping, Please connect power source')
        finally:
            if self.has_power_source:
                self.turn_device_on()
            print('Stop preventing sleep')
            self.caffeinate_process.terminate()
