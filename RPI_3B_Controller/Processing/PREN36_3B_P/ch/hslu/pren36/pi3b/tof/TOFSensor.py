import time
import RPi.GPIO as GPIO
import ch.hslu.pren36.pi3b.tof.VL53L0X as VL53L0X


class TOFSensor:
    # GPIO for Sensor 1 shutdown pin
    sensor1_shutdown = 20
    tof = None
    timing = None

    def __init__(self):
        # GPIO.setwarnings(False)
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(TOFSensor.sensor1_shutdown, GPIO.OUT)
        #
        # # Set all shutdown pins low to turn off each VL53L0X
        # GPIO.output(TOFSensor.sensor1_shutdown, GPIO.LOW)
        #
        # # Keep all low for 500 ms or so to make sure they reset
        # time.sleep(0.50)

        # Create one object per VL53L0X passing the address to give to
        # each.
        self.tof = VL53L0X.VL53L0X(address=0x29)

        # Set shutdown pin high for the first VL53L0X then
        # call to start ranging
        # GPIO.output(TOFSensor.sensor1_shutdown, GPIO.HIGH)
        # time.sleep(0.50)
        self.tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

        self.timing = self.tof.get_timing()
        if self.timing < 20000:
            self.timing = 20000
        print("Timing %d ms" % (self.timing / 1000))

    def distance(self):
        distance = self.tof.get_distance()
        time.sleep(self.timing / 1000000.00)
        return distance / 10

    def stop(self):
        self.tof.stop_ranging()
        # GPIO.output(TOFSensor.sensor1_shutdown, GPIO.LOW)
        # GPIO.cleanup()
