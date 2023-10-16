import threading
import os
import time
import json
from Webserver import WebServer
from DigitalOut import DigitalIO


def main():
    print("started")


    digitalOut = DigitalIO()
    digitalOut.start()

    webserver = WebServer(digitalOut)
    webserver.open_webserver()

    shutdown_event = False

    print("Webserver started")

    while not shutdown_event:
        time.sleep(0.001)





if __name__ == "__main__":
    main()




