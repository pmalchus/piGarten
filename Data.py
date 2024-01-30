


class DataStorage:

    def __init__(self):
        """
        :return:
        """
        self.data = {
            "Beleuchtung": {
                "Veranda": 0,
                "Vordach": 0,
                "Licht_oben": 0,
                "Licht_unten": 0,
                "Steckdosen": 0
            }
        }
        self.shutdown_event = False


