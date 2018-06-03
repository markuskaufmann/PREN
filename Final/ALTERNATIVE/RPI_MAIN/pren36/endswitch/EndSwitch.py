import RPi.GPIO as GPIO


class EndSwitch:
    GPIO_PIN = 9

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PIN, GPIO.IN)

    def signal(self):
        return GPIO.input(EndSwitch.GPIO_PIN)

    def stop(self):
        GPIO.cleanup()
