import RPi.GPIO as GPIO
import time
import sys

led = sys.argv[0]

GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)

try:
    while True:
        GPIO.output(led, 1)  # 1/0, True/False, GPIO.HIGH/GPIO.LOW accepted
        time.sleep(1)  # 5 seconds light on
        GPIO.output(led, False)
        time.sleep(1)  # 5 seconds light off

except KeyboardInterrupt:
    print ("Quit")
    GPIO.output(led, GPIO.LOW)
    GPIO.cleanup()