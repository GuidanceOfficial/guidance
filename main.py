"""
Serves as the primary controller for setting up a device for bluetooth communication with
neighboring devices.

This file needs to be tailored towards your device specific mac address
"""
import csv
import subprocess

from guidance.bluetoothctl import Bluetoothctl
from guidance.device import Device
# from guidance.monitor import Monitor
# from guidance.monitor import *

from bluetooth import *
from time import sleep

MOTOR_PIN = 27
BLUETOOTH_PORT = 1
BLUETOOTH_PORT2 = 2
PAYLOAD = 1024
END_TRANSMISSION = b""
PI_ZERO_ADDRESS1 = "B8:27:EB:2D:D7:36"
PI_ZERO_ADDRESS2 = "B8:27:EB:D2:45:EF"
QUERY_TIME_DELTA = 3 # seconds
API_IS_WORKING = False
PATH_TO_FIFO = "/home/pi/Development/guidance/log_fifo"

def get_direction(sock):
    """Queries API every QUERY_TIME_DELTA seconds"""
    if not sock:
        with open("./data/dummy_travel_data.csv") as directions:
            for direction in csv.reader(directions):
                yield direction
    else:
        yield sock.recv(PAYLOAD) # infomation received from hm-10 serial device


def get_recipient(direction):
    """Returns the address of the motor to receive some signal.
    
    :param: direction - should be a single character indicating left or right motor
    """
    return PI_ZERO_ADDRESS1 if direction.upper() == "L" else PI_ZERO_ADDRESS2


def process_data(data):
    """When the data is received from the iPhone, process it before sending to pi zeros."""
    if isinstance(data, list):
        # Get data from dummy data source
        return bytes(" ".join(data), "utf-8")
    else:
        # Data is coming in from some api
        # Do some processing
        return data


def execute(action, path_to_fifo):
    """Sends the action to the fifo at <path_to_fifo>."""
    cmd = 'echo "{}" > {}'.format(action, path_to_fifo)
    subprocess.check_output(cmd, shell=True)


if __name__ == "__main__":
    btctl = Bluetoothctl()
    device = Device(btctl.get_address(), BLUETOOTH_PORT)
    device2 = Device(btctl.get_address(), BLUETOOTH_PORT2)
    iter_direction = iter(get_direction(None))
    next(iter_direction) # skip header
    
    while device.is_active():
        try:
            # Listen for data
            client_sock, client_info = device.accept() if API_IS_WORKING else None, None
            sleep(QUERY_TIME_DELTA)
            data = next(iter_direction)
            if API_IS_WORKING:
                client_sock.close()

            # Process data    
            direction, distance = process_data(data).split(b" ")
            direction = direction.decode("utf-8")
            distance = distance.decode("utf-8")
            execute("{},{}".format(direction, distance), PATH_TO_FIFO)

            # Send data
            recipient = get_recipient(direction)
            if recipient == PI_ZERO_ADDRESS1:
                device.connect(recipient)
                device.send(distance)
                device.close_connection_to_peer()
            else:
                device2.connect(recipient)
                device2.send(distance)
                device2.close_connection_to_peer()
        except:
            # Send the error message to the TFT and retry
            execute("There was an error...", PATH_TO_FIFO)