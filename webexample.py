#!/usr/bin/python

import time
import codecs
import threading
import socket
import binascii






class SMASocket:
    """demonstration class only
      - coded for clarity, not efficiency
    """
    HOST = '192.168.0.72'
    PORT = 9522
    cmd_1 = '534d4100000402a00000000100260010606509a0ffffffffffff00007800ddc8b53a000000000000028000020000000000000000000000000000'
    cmd_2 = '534d4100000402a00000000100220010606508a0ffffffffffff00037800ddc8b53a00030000000003800e01fdffffffffff00000000'
    cmd_3 = '534d4100000402a00000000100260010606509a0ffffffffffff00007800ddc8b53a00000000000001800002806100482100ff4a410000000000'
    cmd_4 = '534d4100000402a000000001003a001060650ea0ffffffffffff00017800ddc8b53a00010000000004800c04fdff0700000084030000fec2d45300000000b8b8b8b8888888888888888800000000'
    cmd_5 = '534d4100000402a00000000100260010606509a0ffffffffffff00007800ddc8b53a0000000000000c800002005100002000ffff5f0000000000'
    cmd_6 = '534d4100000402a00000000100260010606509a0ffffffffffff00007800ddc8b53a0000000000000e800002005400002000ffff5f0000000000'
    cmd_7 = '534d4100000402a00000000100260010606509a0ffffffffffff00007800ddc8b53a0000000000000f800002805300002000ffff5f0000000000'
    code_total_today = b'01020054'
    code_spot_ac_power = b'0102005100'


    def __init__(self):
        print("Started")

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        ia = socket.gethostbyname("192.168.0.72")
        self.s.connect((ia, 9522))


        sender = threading.Thread(target=self.sender_thread)
        sender.start()

        receiver = threading.Thread(target=self.receiver_thread)
        # receiver = threading.Thread(target=self.receiver_thread, args=(self,))
        receiver.start()


    def get_long_value_at(self, data, index):

        value = data[index:index +8]
        byte = codecs.decode(value, 'hex')
        reversed_data = byte[::-1]
        converted = int.from_bytes(reversed_data, 'big')
        return converted

    def prepare_sending(self, cmd, sendersocket):

        data = codecs.decode(cmd, 'hex')
        sendersocket.send(data)
        # print("send data    : {0}".format(data))

    def sender_thread(self):
        print("Started sender")

        self.prepare_sending(self.cmd_1, self.s)
        time.sleep(0.5)
        self.prepare_sending(self.cmd_2, self.s)
        time.sleep(0.5)
        self.prepare_sending(self.cmd_3, self.s)
        time.sleep(0.5)
        self.prepare_sending(self.cmd_4, self.s)
        time.sleep(0.5)
        while True:
            # print("cmd5")
            self.prepare_sending(self.cmd_5, self.s)
            time.sleep(10)
            # print("cmd6")
            # self.prepare_sending(self.cmd_6, self.s)
            # time.sleep(2)
            # self.prepare_sending(self.cmd_7, self.s)
            # time.sleep(2)


    def receiver_thread(self):
        print("Started receiver")
        while True:

            rec_data = self.s.recv(1024)
            rec_data_byte = binascii.hexlify(rec_data)
            # print("received data: {0} ".format(rec_data_byte))
            code = rec_data_byte[84:94]
            # print(code)


            if code == self.code_total_today:
                total = self.get_long_value_at(rec_data_byte, 124)
                print("total: {0}".format(total))
                today = self.get_long_value_at(rec_data_byte, 156)
                print("today: {0}".format(today))
            if code == self.code_spot_ac_power:
                value = self.get_long_value_at(rec_data_byte, 124)
                print("powervalue: {0}".format(value))


SMASocket = SMASocket()



