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
SLEEP_TIME_DELTA = 3


if __name__ == "__main__":
    btctl = Bluetoothctl()
    device = Device(btctl.get_address(), BLUETOOTH_PORT)
    motor = Motor(MOTOR_PIN, SLEEP_TIME_DELTA)
    
    while device.is_active():
        try:
            print("Waiting for connection...")
            # Listen for data
            client_sock, client_info = device.accept()
            data = client_sock.recv(PAYLOAD)
            client_sock.close()

            # Translate data to motor command
            distance = int(data)
            if distance < 0:
                device.active = False
                motor.stop_vibrating()
                motor.stop()
            else:
                motor.vibrate(distance)

        except:
            print("Something bad happened. Trying again.")
