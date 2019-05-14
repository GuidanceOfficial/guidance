import json
import serial


PACKET_SIZE = 64


if __name__ == "__main__":
    while True:
        ser = serial.Serial("/dev/ttyUSB0") # default baud rate 9600
        print("Serial Port Initialized...")
        payload_size = int(ser.read(4))
        primary_chunk_size = payload_size // PACKET_SIZE
        remaining_chunk_size = payload_size - primary_chunk_size

        data = b""
        data += ser.read(primary_chunk_size + remaining_chunk_size)

        ser.close()

        try:
            dataAsDict = json.loads(data)
        except:
            print("Trouble parsing string as JSON.")

        try:
            stepsArray = dataAsDict["routes"][0]["legs"][0]["steps"]
            print("Steps Array: {}".format(stepsArray))
        except:
            print("Encountered error searching for keys.")

