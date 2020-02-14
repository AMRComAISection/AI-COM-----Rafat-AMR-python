import socket
import json
import pyautogui
import sys
import os
import cv2
import cv2
import base64
import matplotlib.pyplot as plt
import numpy as nm
import PIL
import io
from PIL import Image
import time


HOST = '192.168.123.106'  # The server's hostname or IP address
PORT = 28280        # The port used by the server
# a Python object (dict):
x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}


jsonToString = json.dumps(x)

sendData = jsonToString
print(type(sendData.encode('utf-8')))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    for x in range(100000):
        # g = input ("Enter your name : ") 

        seconds = time.time() 
        # sendData = jsonToString
        # sendData = g
        sendData = "w"
        s.sendall(sendData.encode('utf-8'))
        data = s.recv(2048)
        seconds = time.time() - seconds 
        print(seconds)
        # time.sleep(1)
        pass

print('Received', repr(data))