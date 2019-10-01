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


def set_as_client():
    " ASUS to NVIDIA"
    
    HOST = "192.168.1.3" # Nvidia'nın IP adresi
    PORT = 8089 # Nvidia frameleri bu porttan alacak

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    connection = client_socket.makefile('wb')

    cap = cv2.VideoCapture(0)
    cap.set(3, 320); # 3. CV_CAP_PROP_FRAME_WIDTH: Width of the frames in the video stream.
    cap.set(4, 240); # 4. CV_CAP_PROP_FRAME_HEIGHT: Height of the frames in the video stream.

    img_counter = 0
    
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    while True:
        retval, frame = cap.read()
        result, frame = cv2.imencode('.jpg', frame, encode_param)
        #data = zlib.compress(pickle.dumps(frame, 0))
        data = pickle.dumps(frame, 0)
        size = len(data)
    
        print("{}: {}".format(img_counter, size))
        client_socket.sendall(struct.pack(">L", size) + data)
        img_counter += 1
    
    cap.release()

if __name__ == '__main__':
    set_as_client()