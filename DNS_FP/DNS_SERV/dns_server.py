#!/usr/bin/python

import socket

dns_names = {"mpapp.nobies.in" : "172.16.45.84"}

def resolve(name):
    global dns_names
    if name in dns_names:
        return dns_names[name]
    else :
        # you ought to add some basic checking of name here
        dns_names[name] = socket.gethostbyname(name)
        return dns_names[name]

host = ''
port = 50000
backlog = 5
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)
while 1:
    client, address = s.accept()
    data = client.recv(size).decode()
    if data:
        bits = data.split(":")
        if bits[0] == 'h':
            client.send(resolve(bits[1]).encode())
    client.close()