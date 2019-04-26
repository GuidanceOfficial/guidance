"""
Serves as the primary controller for setting up a device for bluetooth communication with
neighboring devices.

This file needs to be tailored towards your device specific mac address
"""
import csv

from guidance.bluetoothctl import Bluetoothctl
from guidance.device import Device
from guidance.motor import Motor

from bluetooth import *

MOTOR_PIN = 27
BLUETOOTH_PORT = 1
PAYLOAD = 1024
END_TRANSMISSION = b""
PI_ZERO_ADDRESS1 = "B8:27:EB:2D:D7:36"
PI_ZERO_ADDRESS2 = "B8:27:EB:D2:45:EF"
SLEEP_TIME = 5 # seconds


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


def receive_data(sock, data, default=True):
    if default:
        return sock.recv(PAYLOAD)
    else:
        from time import sleep
        sleep(SLEEP_TIME)
        return bytes("{},{}".format(data[0], data[1]), "utf-8")



if __name__ == "__main__":
    btctl = Bluetoothctl()
    device = Device(btctl.get_address(), BLUETOOTH_PORT)
    dummy_data_reader = csv.reader( open("dummy_travel_data.csv") )
    dummy_data = list(dummy_data_reader)[1:] # Ignores header
    cur_row = 0
    
    while device.is_active():
        print("Waiting for connection on port {}".format(BLUETOOTH_PORT))
        client_sock, client_info = device.accept()
        with client_sock:
            print("Accepted connection from {}".format(client_info))
            device.connect(PI_ZERO_ADDRESS1)
            while True:
                # data = client_sock.recv(PAYLOAD)
                data = receive_data(client_sock, dummy_data[cur_row], False)
                cur_row += 1
                if not data: break
                print("Data received: [{}]".format(data))
                # Send data to next device
                device.send(PI_ZERO_ADDRESS1, data)
            device.close_connection_to_peer()
        client_sock.close()



