import os

from random import randint
from random import choice

if __name__ == "__main__":
    os.makedirs(os.path.dirname(os.path.realpath(__file__)) + "/data", exist_ok=True)

    turns = ["L", "R"]
    distances = [d*20 for d in range(30, 60)]

    with open("./data/dummy_travel_data.csv", "w") as f:
        f.write("Direction,Distance(feet)\n")
        for _ in range(20):
            cur_turn = choice(turns)
            cur_dist = choice(distances)
            for dist in range(cur_dist, 0, -100):
                f.write(f"{cur_turn},{dist}\n")
    
        

