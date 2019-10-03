# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 10:28:28 2019

@author: ASUS
"""

import socket
import struct
import pickle
import zlib
import io
import sys
import time
import numpy as np
import cv2

def set_as_server():
    """ This function going to take back processed camera feed from NVIDIA to ASUS"""
    
    HOST = "" # NVIDIA'un IP adresi
    PORT = 8089 # ASUS  frameleri bu porttan alacak

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Set communication based IP v4 and TCP
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    conn, addr = server_socket.accept()
    data = b''
    payload_size = struct.calcsize('>L')
    print("payload_size: {}".format(payload_size))

    while True:
        while len(data) < payload_size:
            print("Recv: {}".format(len(data)))
            data += conn.recv(4096)
    
        print("Done Recv: {}".format(len(data)))
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        print("msg_size: {}".format(msg_size))
        
        while len(data) < msg_size:
            data += conn.recv(4096)
            
        frame_data = data[:msg_size]
        data = data[msg_size:]
    
        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        
        # Display the resulting frame
        cv2.imshow('ImageWindow',frame)
        
        overlay = frame.copy()
        set_as_client(overlay)
        
        # Wait 3 mili seconds for an interaction. Check the key and do the corresponding job.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
def set_as_client(overlay):
    """ This function going to send camera feed from ASUS to NVIDIA"""
    
    HOST = "192.168.1.4" # ASUS'un IP adresi
    PORT = 12345 # Nvidia frameleri bu porttan alacak

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    connection = client_socket.makefile('wb')

    img_counter = 0
    
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    while True:
        frame = overlay
        result, frame = cv2.imencode('.jpg', frame, encode_param)
        #data = zlib.compress(pickle.dumps(frame, 0))
        data = pickle.dumps(frame, 0)
        size = len(data)
        cv2.putText(overlay, str(image_counter), (225, 225), cv2.FONT_HERSHEY_SIMPLEX, 1, (50,225,250), 5)

        print("{}: {}".format(img_counter, size))
        client_socket.sendall(struct.pack(">L", size) + data)
        img_counter += 1
    
if __name__ == '__main__':
    set_as_server()