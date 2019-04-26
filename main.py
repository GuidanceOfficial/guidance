"""
Serves as the primary controller for setting up a device for bluetooth communication with
neighboring devices.

This file needs to be tailored
"""
from guidance.bluetoothctl import Bluetoothctl
from guidance.device import Device
from guidance.motor import Motor

from bluetooth import *

MOTOR_PIN = 27
BLUETOOTH_PORT = 1
PAYLOAD = 1024
END_TRANSMISSION = b"-1"
PI_ZERO_ADDRESS1 = ""
PI_ZERO_ADDRESS2 = ""


def connect_to(addr):
    btctl = Bluetoothctl()
    device = Device(btctl.get_address(), BLUETOOTH_PORT)

    while device.is_active():
        print("Attempting to connect to {}".format(addr))
        service_match = device.find(addr)
        
        if len(service_match) == 0:
            print("Couldn't find the service at {}".format(addr))
            sys.exit(0)

        match = service_match[0]
        port, name, host = match["port"], mathc["name"], match["host"]

        sock = BluetoothSocket(RFCOMM)
        sock.connect((host, port))
        print("Connected to {}".format(addr))




if __name__ == "__main__":
    btctl = Bluetoothctl()
    device = Device(btctl.get_address(), BLUETOOTH_PORT)
    
    while device.is_active():
        print("Waiting for connection on port {}".format(BLUETOOTH_PORT))
        client_sock, client_info = device.listen()
        print("Accepted connection from {}".format(client_info))
        try:
            is_receiving_data = True
            while is_receiving_data:
                data = client_sock.recv(PAYLOAD)
                is_receiving_data = data == END_TRANSMISSION
                print("Data received: [{}]".format(data))
        except IOError:
            pass
        client_sock.close()



