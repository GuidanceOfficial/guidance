import RPi.GPIO as GPIO

class Motor:
    """Controls the mini vibrating motor."""

    def __init__(self, gpio_pin):
        self.pin = gpio_pin
        self.freq = 1
        self._setup()
        self.duty_cycle = 100
        self.pwm = GPIO.PWM(self.pin, self.freq)

    
    def _setup(self):
        """Setup PWM connection to motor"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, self.freq)
        self.pwm.start(0)


    def vibrate(self, duty_cycle):
        self.pwm.ChangeDutyCycle(duty_cycle)
        return self


    def stop(self):
        self.pwm.ChangeDutyCycle(0)
        return self


    def change_freq(freq):
        """Change the motors frequency."""
        self.pwm.ChangeFrequency(freq)
        return self