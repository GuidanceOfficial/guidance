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
            data_as_dict = json.loads(data)
        except:
            print("Trouble parsing string as JSON.")

        stepsArray = []
        remaining_distance = 0
        try:
            stepsArray = data_as_dict["routes"][0]["legs"][0]["steps"]
            remaining_distance = data_as_dict["routes"][0]["legs"][0]["distance"]["text"]
            
            metric = remaining_distance[-2:]
            if metric == "mi":
                remaining_distance = float(remaining_distance[: len(remaining_distance) - 2] ) * 5280
            else:
                remaining_distance = float(remaining_distance[: len(remaining_distance) - 2 ])

            # print("Remaining Distance: {}ft".format(remaining_distance))
            # print("Steps Array: {}".format(stepsArray))
        except:
            print("Encountered error searching for keys.")

        if remaining_distance < 100:
            data = ["A", "0"]

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

        

