from Data import DataStorage
import RPi.GPIO as GPIO
import threading
from threading import Timer
import time
from time import localtime, strftime, strptime, sleep
from datetime import date
import random






class DigitalIO(threading.Thread):

    def __init__(self):
        """
        :return:
        """
        threading.Thread.__init__(self)
        self.DataStorage = DataStorage()

        self.logger = ""


        self.gpio_states = {
            17: 1,
            18: 1,
            20: 1,
            21: 1,
            22: 1,
            23: 1,
            24: 1
        }

        self.random_states = {
            17: 0,
            18: 0,
            20: 0,
            21: 0,
            22: 0,
            23: 0,
            24: 0
        }

        self.ligth_groups = {
            "Veranda": {
                "Mode": "Aus",
                "GPIO" : [24]
            },
            "Vordach" : {
                "Mode": "Aus",
                "GPIO" : [23]
            },
            "LichtOben" : {
                "Mode": "Aus",
                "GPIO" : [18]
            },
            "LichtUnten": {
                "Mode": "Aus",
                "GPIO" : [17]
            },
            "Steckdosen": {
                "Mode": "Aus",
                "GPIO" : [20,21,22]
            }
        }


    def set_gpio_state(self, gpio, value):
        if value != self.gpio_states[gpio]:
            self.gpio_states[gpio] = value
            print("switch gpio {0} to state {1}".format(gpio, value))
            GPIO.output(gpio, value)




    def random_change(self):
        for gpio in self.random_states:
            self.random_states[gpio] = random.randint(0, 1)



    def switchIO(self, group_settings):
        for gpio in group_settings["GPIO"]:
            if group_settings["Mode"] == "Aus":
                self.set_gpio_state(gpio, 1)

            if group_settings["Mode"] == "An":
                self.set_gpio_state(gpio, 0)

            if group_settings["Mode"] == "Zeitschaltuhr_Zufall":
                self.zeitschaltuhr(gpio, random=True)

            if group_settings["Mode"] == "Zeitschaltuhr":
                self.zeitschaltuhr(gpio, random=False)

    def zeitschaltuhr(self, gpio, random=False):

        today = date.today()
        time_switch = False
        for settings in self.DataStorage.data["Time_Settings"]:
            start_str = str(today) + ":" + self.DataStorage.data["Time_Settings"][settings]["on"]
            end_str = str(today) + ":" + self.DataStorage.data["Time_Settings"][settings]["off"]
            time_obj_start = strptime(start_str, '%Y-%m-%d:%H:%M')
            time_obj_end = strptime(end_str, '%Y-%m-%d:%H:%M')
            current_time = localtime()
            if current_time > time_obj_start and current_time < time_obj_end:
                if random:
                    if self.random_states[gpio] == 0:
                        time_switch = False
                    if self.random_states[gpio] == 1:
                        time_switch = True
                        break
                else:
                    time_switch = True
                    break
            else:
                time_switch = False

        if time_switch:
            self.switchIO({"GPIO": [gpio], "Mode": "An"})
        else:
            self.switchIO({"GPIO": [gpio], "Mode": "Aus"})

    def prepareIO(self):
        GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD
        GPIO.setwarnings(False)

        for group in self.ligth_groups:
            for gpio in self.ligth_groups[group]["GPIO"]:
                GPIO.setup(gpio, GPIO.OUT)
                GPIO.output(gpio, GPIO.HIGH)

    def run(self):
        self.prepareIO()
        print("IO Started")

        random_time = self.DataStorage.data["random_changeTime"] * 60
        t = Timer(2.0, self.random_change)
        t.start()


        while True:
            for group in self.ligth_groups:
                self.switchIO(self.ligth_groups[group])
                pass
            time.sleep(1)

    def switch(self, value):
        self.ligth_groups[value["Channel"]]["Mode"] = value["Value"]



