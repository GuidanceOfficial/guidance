# add code to vibrate motors on system boot
import RPi.GPIO as GPIO
import time

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(27, GPIO.OUT)

    p = GPIO.PWM(27,100)
    p.start(100)

    time.sleep(3)
    p.stop()
    GPIO.cleanup()

