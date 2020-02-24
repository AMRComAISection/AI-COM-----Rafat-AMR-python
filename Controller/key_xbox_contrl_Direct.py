import os, sys
import time
import pygame
import socket
import json
import sys
import os
import cv2
import cv2
import base64
import numpy as nm
import PIL
import io
from PIL import Image
import time

from api.controller import controller

joysticks = []
pygame.init()
key_stack = [] 


HOST = '192.168.123.100'  
PORT = 28280 
def dataSend(char) :
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        sendData = char
        s.sendall(sendData.encode('utf-8'))
        data = s.recv(2048)
        print(data)
        pass

    pass

def data_key_event(value,key_type):
    
    val = ''
    if key_stack:
        val = key_stack.pop()
        pass
    if val == value:
        
        key_stack.append(val)
        pass
    else :
        print("send = ", value," , type = ",key_type)
        key_stack.append(value)
        response = controller(value)
        print(response.RESPONSE)
        # dataSend(value)
    # print(key_stack)
    pass

def Event() :
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                exit()
        elif event.type == pygame.KEYDOWN:
                value = chr(event.key)
                # response = controller(value)
                data_key_event(value,'keyboard')
                # print("key down = "+value)

        elif event.type == pygame.KEYUP:
                value = chr(event.key)
                # response = controller(value)
                data_key_event('k', 'keyboard')
                # print("key up = "+value)

        elif event.type == pygame.JOYAXISMOTION:
            XBOXControll(joysticks[event.joy],'axis',event) 
            # print("Joystick '",joysticks[event.joy].get_name(),"' axis",event.axis,"motion.")
            pass
        elif event.type == pygame.JOYBALLMOTION:
            # print("Joystick '",joysticks[event.joy].get_name(),"' ball",event.axis,"motion.")  
            pass   
        elif event.type == pygame.JOYHATMOTION:
            # print("Joystick '",joysticks[event.joy].get_name(),"' hat",event.hat," moved.")
            pass

        elif event.type == pygame.JOYBUTTONDOWN:
            # print("Joystick '",joysticks[event.joy].get_name(),"' button",event.button,"down.")
            pass
        elif event.type == pygame.JOYBUTTONUP:
            # print("Joystick '",joysticks[event.joy].get_name(),"' button",event.button,"up.")
            pass
       
        # print(event)
        
    pass

def XBOXCount() :
     # for al the connected joysticks
    for i in range(0, pygame.joystick.get_count()):
        # create an Joystick object in our list
        joysticks.append(pygame.joystick.Joystick(i))
        # initialize them all (-1 means loop forever)
        joysticks[-1].init()
        # print a statement telling what the name of the controller is
        print("Detected joystick '",joysticks[-1].get_name(),"'")
    pass

def XBOXControll(joy,type,event) :
    XBOX_axis_type(joy,event)
    pass

'''
left side axis wheel 
&
right side axis wheel
'''
def XBOX_axis_type(joy,event):
    if event.axis == 0: #left side axis wheel right & left
        value = int(event.value * 1000)
        if value > 10 :
            data_key_event('r','xbox')
            # print("RIGHT " , value)
        if value < -10 :
            data_key_event('e','xbox')
            # print("LEFT " , value)
        if value == 0 :
            data_key_event('k','xbox')
            # print(" STABLE " , value)
        pass
    elif event.axis == 1: #left side axis wheel up & down
        value = int(event.value * 1000)
        if value > 10 :
            data_key_event('w','xbox')
            # print("BACK " , value)
        if value < -10 :
            data_key_event('q','xbox')
            # print("FORWARD " , value)
        if value == 0 :
            data_key_event('k','xbox')
            # print(" STABLE " , value)
        pass
    elif event.axis == 3: #right side axis wheel up & down
        # print(event.value)
        pass
    elif event.axis == 4: #right side axis wheel right & left
        # print(event.value)
        pass
    pass

if __name__ == "__main__":
    screen = pygame.display.set_mode((500, 250))
    pygame.display.set_caption("Joystick Testing / XBOX360 Controller / Keyboard Testing")
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))
    clock = pygame.time.Clock()

    XBOXCount()
    running = True
    while running:
        clock.tick(60)
        Event() 
        screen.blit(background, (0, 0))
        pygame.display.flip()
        
    pygame.quit()
    pass


