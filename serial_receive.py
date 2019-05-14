import json
import serial
import time

PACKET_SIZE = 64
RIGHT_OPTIONS = (
        "turn-slight-right", "turn-sharp-right", "uturn-right",
        "turn-right", "ramp-right", "fork-right", "roundabout-right",
        )


if __name__ == "__main__":
    """(TO-DO): Add a check for arriving """
    iter_count = 0
    while True:
        iter_count += 1
        ser = serial.Serial("/dev/ttyUSB0") # default baud rate 9600
        print("Serial Port Initialized...")
        time.sleep(1)
        payload_size = ser.read(4)
        print("Payload Size: {}".format(payload_size))
        # payload_size = int(ser.read(4))
        payload_size = int(payload_size)
        primary_chunk_size = payload_size // PACKET_SIZE
        remaining_chunk_size = payload_size - primary_chunk_size

        data = b""
        data += ser.read(primary_chunk_size + remaining_chunk_size)
        print("Size of data: {}".format(len(data)))

        try:
            dataAsDict = json.loads(data)
        except:
            print("Trouble parsing string as JSON.")

        stepsArray = []
        try:
            stepsArray = dataAsDict["routes"][0]["legs"][0]["steps"]
            # print("Steps Array: {}".format(stepsArray))
        except:
            print("Encountered error searching for keys.")

        distance = 0
        direction = ""
        if not isinstance(stepsArray, list):
            stepsArray = [stepsArray] # convert to iterable
        
        for step in stepsArray:
            dist = step["distance"]["text"]
            distance += int(dist[: len(dist) - 2 ]) # expecting distance in ft
            if "maneuver" in step:
                direction = "R" if any(right_word in step["maneuver"] for right_word in RIGHT_OPTIONS) else "L" 
                break

        print("{}.) Direction: {} - Distance: {} ft".format(iter_count, direction, distance))

        

