import RPi.GPIO as GPIO

class Motor:
    """Controls the mini vibrating motor."""

    def __init__(self, gpio_pin):
        self.pin = gpio_pin
        self._setup()

    
    def _setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)


    def vibrate(self):
        pass