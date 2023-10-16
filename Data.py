import os
import json


class DataStorage:

    def __init__(self):
        """
        :return:
        """
        self.data = {
            "States": {
                "Veranda": "Aus",
                "Vordach": "Aus",
                "Licht_oben": "Aus",
                "Licht_unten": "Aus",
                "Steckdosen": "Aus"
            },
            "random_changeTime": 5,
            "Time_Settings":{
                "setting_1": {"on": "16:30",
                              "off": "21:00"},
                "setting_2": {"on": "06:30",
                              "off": "07:30"}
            }
        }
        self.shutdown_event = False
        self.get_default_values()

    def get_default_values(self):

        if os.path.exists("default_values.json"):
            with open('default_values.json', 'r') as datafile:
                self.data = json.load(datafile)
        else:

            with open('default_values.json', 'w') as datafile:
                json.dump(self.data, datafile)

        return self.data

    def set_default_values(self):
        with open('default_values.json', 'w') as datafile:
            json.dump(self.data, datafile)