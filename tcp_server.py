# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 10:37:56 2019

@author: ASUS
"""
#!/usr/bin/python

import socket
import sys

HOST = ''
PORT = 8089

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket has been created')

try:
    s.bind((HOST, PORT))
except socket.error:
    print("Binding failed")
    sys.exit()
    
    
print("Socket has been bounded")


s.listen(10)
print('Socket now listening')

conn, addr = s.accept()
print("Connected with " + addr[0] + ":" + str(addr[1]))

data = conn.recv(1024)
conn.sendall(data)
print(data.encode())

conn.close()
s.close()