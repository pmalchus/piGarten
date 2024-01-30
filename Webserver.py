import http.server
import socketserver
import json
from DigitalOut import DigitalIO
from Data import DataStorage
import threading
from functools import partial
from socketserver import ThreadingMixIn
from http.server import SimpleHTTPRequestHandler, HTTPServer


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):


    def __init__(self, digitalOut, datastorage, *args, **kwargs):
        self.digitalOut = digitalOut
        self.datastorage = datastorage
        super().__init__(*args, **kwargs)


    def do_GET(self):
        if self.path == '/':
            self.path = 'PiGarten.html'
        print("Get")

        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        print("Post")
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        body = post_data.decode('utf-8')
        response = json.loads(body)

        if response["Mode"] == "read_values":

            inital_data = self.datastorage.get_default_values()

            print(response["Mode"])
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            jsontest = json.dumps(inital_data)
            self.wfile.write((jsontest).encode('utf-8'))


        if response["Mode"] == "SwitchIO":
            self.digitalOut.ligth_groups[response["Channel"]]["Mode"] = response["Value"]

            channel = response["Channel"]
            self.datastorage.data["States"][channel] = response["Value"]
            self.datastorage.set_default_values()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(("OK").encode('utf-8'))


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


class WebServer:



    def __init__(self, digitalOut):
        """
        :return:
        """
        self.data = DataStorage()
        self.digitalOut = digitalOut



    def open_webserver(self):
        # handler_object = MyHttpRequestHandler
        handler_object = partial(MyHttpRequestHandler, self.digitalOut, self.data)
        # handler_object = MyHttpRequestHandler

        PORT = 8080
        my_server = socketserver.TCPServer(("piGarten", PORT), handler_object)
        my_server.digitalIO = self.digitalOut

        # Star the server
        my_server.serve_forever()
        print("after serve_forever")


