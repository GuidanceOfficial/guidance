"""
Serves as the primary controller for setting up a device for bluetooth communication with
neighboring devices
"""
from guidance.bluetoothctl import Bluetoothctl
from guidance.device import Device
from guidance.motor import Motor

MOTOR_PIN = 27
BLUETOOTH_PORT = 1
PAYLOAD = 1024
END_TRANSMISSION = b"-1"

if __name__ == "__main__":
    btctl = Bluetoothctl()
    device = Device(btctl.get_address(), BLUETOOTH_PORT)
    motor = Motor(MOTOR_PIN)
    
    while device.is_active():
        print("Waiting for connection on port {}".format(BLUETOOTH_PORT))
        client_sock, client_info = Device.listen()
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



