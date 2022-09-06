#!/usr/bin/python

import socket

### configure me ###

class dns_client:
    def __init__(self, query):
        self.dns_server_ip = '127.0.0.1'
        self.dns_server_port = 50000
        #'mpapp.nobies.in' # change this to the hostname you want to lookup

        ### configure me ###

        self.size = 1024

    def run_quary(self, query: str):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.dns_server_ip,self.dns_server_port))
        s.send(('h:' + query).encode())
        data = s.recv(self.size).decode()
        s.close()
        return data,