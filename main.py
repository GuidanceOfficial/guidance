"""
Serves as the primary controller for setting up a device for bluetooth communication with
neighboring devices.

This file needs to be tailored towards your device specific mac address
"""
import csv

from guidance.bluetoothctl import Bluetoothctl
from guidance.device import Device

from bluetooth import *

MOTOR_PIN = 27
BLUETOOTH_PORT = 1
PAYLOAD = 1024
END_TRANSMISSION = b""
PI_ZERO_ADDRESS1 = "B8:27:EB:2D:D7:36"
PI_ZERO_ADDRESS2 = "B8:27:EB:D2:45:EF"
SLEEP_TIME = 5 # seconds

def receive_data(sock, data, default=True):
    if default:
        return sock.recv(PAYLOAD)
    else:
        from time import sleep
        # sleep(SLEEP_TIME)
        return bytes("{},{}".format(data[0], data[1]), "utf-8")

def process_data(data):
    """When the data is received from the iPhone, process it before sending to pi zeros."""
    return data

if __name__ == "__main__":
    btctl = Bluetoothctl()
    device = Device(btctl.get_address(), BLUETOOTH_PORT)
    dummy_data_reader, cur_row = csv.reader(open("./data/dummy_travel_data.csv")), 0
    dummy_data = list(dummy_data_reader)[1:]
    
    while device.is_active():
        # Listen for data
        data = b""
        client_sock, client_info = device.accept()
        while True:
            incoming_data = client_sock.recv(PAYLOAD)
            if not incoming_data: break
            data += incoming_data
        client_sock.close()

        # Process data    
        data = process_data(data)

        # Send data
        recipient = PI_ZERO_ADDRESS1 if data[0] == b"L" else PI_ZERO_ADDRESS2
        device.connect(recipient)
        device.send(data)
        device.close_connection_to_peer()