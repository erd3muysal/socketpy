# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 10:37:56 2019

@author: ASUS
"""

import socket
import sys

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print("Failed to connect")
    sys.exit()
    
print("Socket has been created")

HOST = "10.1.153.132"
PORT = 8089

try:
    remote_ip = socket.gethostbyname(HOST)
except socket.gaierror:
    print("Hostname could not be resolved")
    sys.exit()
    
print("IP Adress: " + HOST)
s.connect((HOST, PORT))
print("Socket conencted to server using IP: " + HOST)

message = "Hello, Server!"

try:
    s.sendall(message.encode())
except socket.error:
    print("Did not send succesfully")
    
reply = s.recv(4096)
print(reply.decode())
s.close()