import threading
import os
import time
import json
from Webserver import WebServer
from DigitalOut import DigitalIO
from Data import DataStorage
from Keller_Bridge import KellerBridge
from Logger import Logwriter


def main():


    logger = Logwriter()
    logger.log_print("started")

    data = DataStorage()
    digitalOut = DigitalIO(data)
    digitalOut.start()
    gartenbridge = KellerBridge(data)
    gartenbridge.connect()

    shutdown_event = False

    while not shutdown_event:
        time.sleep(0.1)





if __name__ == "__main__":
    main()




