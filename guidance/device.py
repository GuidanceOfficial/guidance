import sys

from abc import ABC, abstractmethod

from bluetooth import *


class Device:
    def __init__(self, port_num):
        self.port_num = port_num
        self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        self._setup(port_num)
        self._broadcast_service()
    

    def _setup(self, port_num):
        """Opens a port socket communication."""
        self.port_num = port_num
        self.server_sock = BluetoothSocket(RFCOMM)
        self.server_sock.bind(("", port_num))
        self.server_sock.listen(1)

    
    def _broadcast_service(self):
        """Advertises device service to enable peers to see host."""
        advertise_service(
            self.server_sock, "<ServerName>",
            service_id=self.uuid,
            service_classes=[self.uuid, SERIAL_PORT_CLASS],
            profiles=[SERIAL_PORT_PROFILE]
        )


    def listen(self):
        print(f"Waiting for connection on port {self.port_num}")
        client_sock, client_info = self.server_sock.accept()
        print(f"Accepted connection from {client_info}")
        try:
            while True:
                data = client_sock.recv(1024)
                if len(data) == 0: break
                print(f"Received: [{data}]")
        except IOError:
            pass
        client_sock.close()
        self.server_sock.close()


    def send(self, addr):
        service_match = find_service(uuid=self.uuid, address=addr) # the UUID are the same for both devices at the moment
        
        if len(service_match) == 0:
            print("Couldn't find the <ServerName> service.")
            sys.exit(0)

        match = service_match[0]
        port, name, host = match["port"], match["name"], match["host"]

        sock = BluetoothSocket(RFCOMM)
        sock.connect((host, port))
        print("Connected. Type something:")
        while True:
            data = input()
            if len(data) == 0:break
            sock.send(data)
        sock.close()


if __name__ == "__main__":
    local = Device(8000)
    local.listen()

