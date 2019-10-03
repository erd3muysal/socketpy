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
import threading

def set_as_client():
    """ This function going to send camera feed from ASUS to NVIDIA"""
    
    HOST = "192.168.1.2" # Nvidia'nın IP adresi
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
        """
        burada bütün frameleri tek tek döngü içinde alması gerekirken, birinci framei aldıktan sonra biz başka bir fonksiyon
        çağırıyoruz ve frame alımı duruyor. Alınan bir frame nvidia tarafında işlenip geri buraya geliyor, fakat sürekli bir
        frame yenileme olmadığı için durgun bir resim görüyoruz"""

        set_as_server()

    cap.release()

def set_as_server():
    """ This function going to take back processed camera feed from NVIDIA to ASUS"""
    
    HOST = "" # ASUS'un IP adresi
    PORT = 12345 # ASUS  frameleri bu porttan alacak

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

        # Wait 3 mili seconds for an interaction. Check the key and do the corresponding job.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
if __name__ == '__main__':
    set_as_client()