"""
Serves as the primary controller for setting up a device for bluetooth communication with
neighboring devices.

This file needs to be tailored
"""
from guidance.bluetoothctl import Bluetoothctl
from guidance.device import Device
from guidance.motor import Motor

MOTOR_PIN = 27
BLUETOOTH_PORT = 1
PAYLOAD = 1024
END_TRANSMISSION = b"-1"
QUERY_TIME_DELTA = 5

if __name__ == "__main__":
    btctl = Bluetoothctl()
    device = Device(btctl.get_address(), BLUETOOTH_PORT)
    motor = Motor(MOTOR_PIN, QUERY_TIME_DELTA)
    
    while device.is_active():
        # Listen for data
        client_sock, client_info = device.accept()
        data = client_sock.recv(PAYLOAD)
        client_sock.close()

        # Translate data to motor command
        distance = int(data)
        motor.vibrate(distance)