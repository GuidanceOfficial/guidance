"""
Serves as the primary controller for setting up a device for bluetooth communication with
neighboring devices.

This file needs to be tailored towards your device specific mac address
"""
import csv

from guidance.bluetoothctl import Bluetoothctl
from guidance.device import Device

from bluetooth import *
from time import sleep

MOTOR_PIN = 27
BLUETOOTH_PORT = 1
PAYLOAD = 1024
END_TRANSMISSION = b""
PI_ZERO_ADDRESS1 = "B8:27:EB:2D:D7:36"
PI_ZERO_ADDRESS2 = "B8:27:EB:D2:45:EF"
QUERY_TIME_DELTA = 5 # seconds
API_IS_WORKING = False


def get_direction(sock):
    """Queries API every QUERY_TIME_DELTA seconds"""
    if not sock:
        with open("./data/dummy_travel_data.csv") as directions:
            for direction in csv.reader(directions):
                yield direction
    else:
        yield sock.recv(PAYLOAD)


def get_recipient(data):
    if API_IS_WORKING:
        return PI_ZERO_ADDRESS1 if data[0] == b"L" and else PI_ZERO_ADDRESS2
    return PI_ZERO_ADDRESS1


def process_data(data):
    """When the data is received from the iPhone, process it before sending to pi zeros."""
    if isinstance(data, list):
        # Get data from dummy data source
        return data
    else:
        # Data is coming in from some api
        # Do some processing
        return data

if __name__ == "__main__":
    btctl = Bluetoothctl()
    device = Device(btctl.get_address(), BLUETOOTH_PORT)
    iter_direction = iter(get_direction(None))
    next(iter_direction) # skip header

    
    while device.is_active():
        # Listen for data
        client_sock, client_info = device.accept() if API_IS_WORKING else None, None
        sleep(QUERY_TIME_DELTA)
        data = next(iter_direction)
        if API_IS_WORKING:
            client_sock.close()

        # Process data    
        data = process_data(data)
        print("Data: {}".format(data))

        # Send data
        recipient = get_recipient(data)
        device.connect(recipient)
        device.send(data)
        device.close_connection_to_peer()