import RPi.GPIO as GPIO
import time

led = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)

try:
    while True:
        GPIO.output(led, 1)  # 1/0, True/False, GPIO.HIGH/GPIO.LOW accepted
        time.sleep(5)  # 5 seconds light on
        GPIO.output(led, False)
        time.sleep(5)  # 5 seconds light off

except KeyboardInterrupt:
    print ("Quit")
    GPIO.output(led, GPIO.LOW)
    GPIO.cleanup()