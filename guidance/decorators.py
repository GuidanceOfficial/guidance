import datetime
import functools
import logging


logging.basicConfig(
    filename=datetime.datetime.now().strftime("%b_%d_%Y_log"),
    format="%(asctime)s: [%(threadName)s, %(thread)d] %(levelname)s => %(message)s",
    filemode="a",
    level=logging.DEBUG,
)





if __name__ == "__main__":
    logging.basicConfig(
        filename=datetime.datetime.now().strftime("%b_%d_%Y_log"),
        format="%(asctime)s: [%(threadName)s, %(thread)d] %(levelname)s => %(message)s",
        filemode="a",
        level=logging.DEBUG,
    )
