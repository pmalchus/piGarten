from Data import DataStorage
import RPi.GPIO as GPIO
import threading
from threading import Timer
import time
from time import localtime, strftime, strptime, sleep
from datetime import date
import random
from Logger import Logwriter





class DigitalIO(threading.Thread):

    def __init__(self, data):
        """
        :return:
        """
        threading.Thread.__init__(self)
        self.data = data.data


        self.logger = Logwriter()

        self.Beleuchtung = {
            "Veranda": {
                "state": 1,
                "GPIO" : [17]
            },
            "Vordach" : {
                "state": 1,
                "GPIO" : [18]
            },
            "Licht_oben" : {
                "state": 1,
                "GPIO" : [22]
            },
            "Licht_unten": {
                "state": 1,
                "GPIO" : [27]
            },
            "Steckdosen": {
                "state": "1",
                "GPIO" : [23]
            }
        }
    def set_gpio_state(self, group):
        if self.data["Beleuchtung"][group] != self.Beleuchtung[group]["state"]:
            self.Beleuchtung[group]["state"] = self.data["Beleuchtung"][group]
            self.logger.log_print("switch {0} to state {1}".format(group, self.data["Beleuchtung"][group]))
            for gpio in self.Beleuchtung[group]["GPIO"]:
                GPIO.output(gpio, self.Beleuchtung[group]["state"])


    def prepareIO(self):
        GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD
        GPIO.setwarnings(False)

        for group in self.Beleuchtung:
            GPIO.setup(self.Beleuchtung[group]["GPIO"], GPIO.OUT)
            GPIO.output(self.Beleuchtung[group]["GPIO"], GPIO.HIGH)

    def run(self):
        self.prepareIO()
        self.logger.log_print("IO Started")

        while True:
            for group in self.Beleuchtung:
                self.set_gpio_state(group)
            time.sleep(1)


