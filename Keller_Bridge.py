import http.server
import socketserver
import json

import threading
from functools import partial
from socketserver import ThreadingMixIn
from http.server import SimpleHTTPRequestHandler, HTTPServer

import threading
import time
import socket

from Logger import Logwriter

class KellerBridge():



    def __init__(self, data):
        """
        :return:
        """
        self.data = data

        self.logger = Logwriter()

    def connect(self):

        receiver = threading.Thread(target=self.receiver_thread)
        receiver.start()

        # sender = threading.Thread(target=self.sender_thread)
        # sender.start()

    def sender_thread(self):
        self.logger.log_print("Started KellerBridge sender")
        HOST = "192.168.0.30"  # The server's hostname or IP address
        PORT = 9100  # The port used by the server
        while True:
            try:

                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((HOST, PORT))
                bytestr = ""
                while True:
                    bytestr = json.dumps(self.data.data["Sensors"]).encode("utf-8")
                    # self.logger.log_print("sender thread sent: {}".format(bytestr))
                    client.sendall(bytestr)

                    recv_data = client.recv(1024)
                    # self.logger.log_print("sender thread received: {}".format(recv_data))
                    time.sleep(1)

            except Exception as e:
                print("Sender_thread: {}".format(e))
                client.close()
            time.sleep(1)

    def receiver_thread(self):
        self.logger.log_print("Started KellerBridge receiver")
        HOST = "192.168.0.31"  # Standard loopback interface address (localhost)
        PORT = 9100  # Port to listen on (non-privileged ports are > 1023)
        while True:

            try:
                receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                receiver.bind((HOST, PORT))
                receiver.listen()

                while True:
                    conn, addr = receiver.accept()

                    while True:
                        recv_data = conn.recv(4096)
                        self.logger.log_print("receiverThread got: {}".format(recv_data))
                        data_str = recv_data.decode('utf-8')
                        data = json.loads(data_str)
                        self.data.data["Beleuchtung"] = data
                        # print("receiverThread got: {}".format(data))

                        conn.send(b"received")

                        time.sleep(1)

            except Exception as e:

                self.logger.log_print("Receiver_thread error: {}".format(e))
                receiver.close()
                conn.close()

            time.sleep(1)