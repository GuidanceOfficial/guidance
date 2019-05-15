import RPi.GPIO as GPIO

from time import sleep

class Motor:
    """Controls the mini vibrating motor."""
    avg_bike_rate = 15 # ft/sec
    vibration_levels = 4

    def __init__(self, gpio_pin, time_delta):
        self.pin = gpio_pin
        self.freq = 1
        self.time_delta = time_delta
        self._setup()
        self.duty_cycle = 50

    
    def _setup(self):
        """Setup PWM connection to motor"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, self.freq)
        self.pwm.start(1)


    def vibrate(self, dist):
        """Adjust the vibration based on the user's distance from next turn.
        
        TODO: Consider using a loop and making this method more general.
        
        The values chosen for the conditional checks are rather arbitrary.
        """
        bound = self.time_delta * Motor.avg_bike_rate
        duty_cycle = 0
        if dist < bound:        duty_cycle = 90
        elif dist <= 3 * bound: duty_cycle = 70
        elif dist <= 6 * bound: duty_cycle = 40
        elif dist <= 9 * bound: duty_cycle = 20
        else:                   duty_cycle = 0
        self.pwm.ChangeDutyCycle(duty_cycle)
        sleep(self.time_delta)
        self.stop_vibrating()
        return self


    def stop_vibrating(self):
        self.pwm.ChangeDutyCycle(0)
        return self


    def stop(self):
        self.pwm.stop()


    def change_freq(freq):
        """Change the motors frequency."""
        self.pwm.ChangeFrequency(freq)
        return self
