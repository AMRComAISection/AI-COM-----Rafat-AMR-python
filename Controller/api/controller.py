import json
import os ,sys
import glob
import logging
import serial
import pygame
import time

import serial.tools.list_ports

class controller(object):

    ALL_CONTROLLER = None
    RESPONSE = ""
    CURRENT_DIR = None
    CODE_SEND = None
    LOG_FILE_NAME = os.path.dirname(os.path.realpath(__file__))+"/uno_serial_class.log"
    LOGGER = None

    def __init__(self,send) : 
        try:
            self.CODE_SEND = str(send)
            self.CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

            with open(self.CURRENT_DIR + '/cntrl.json', 'r') as json_file:
                self.ALL_CONTROLLER = json.load(json_file)

            self.RESPONSE = self.getresponse()
            pass

        except Exception as  e:
            self.log(str(e))
            pass
       
    
    ### log file genarate ###
    def log(self,message="Log is added with default message"):
        logging.basicConfig(filename= self.LOG_FILE_NAME, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    filemode='a'
                    )
        logger=logging.getLogger() 
        
        logger.setLevel(logging.DEBUG) 
        logger.info(message)
        self.LOGGER = logger
        pass


    def serial_ports(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result



    def validate(self):
        isOk = True
        try:
            self.ALL_CONTROLLER[self.CODE_SEND]
        except Exception:
            isOk = False
        return isOk

    def SerialInput(self):
        try:
            # print(self.CODE_SEND.encode('utf-8'))
            ports = self.serial_ports()
            ser = serial.Serial(ports[0], 9600, timeout=1)
            ser.write(self.CODE_SEND.encode('utf-8')) 
            # arduinoData = ser.readline()
            # print(arduinoData)
            # time.sleep(1)   
            ser.close() 
            pass
        except Exception :
            pass

        pass

    ### All the response of every code in controller.json file ###
    def getresponse(self, cod=""):
        output = ""
        try:
            if self.validate():
                cod = self.CODE_SEND
                # print(len(self.serial_ports()))
                if len(self.serial_ports()) >= 1:
                    self.SerialInput()
                    output = self.OutputGood(message="Data is accepted")
                else :
                     output = self.OutputError(message="Not found arduino")
                
            
            else:
                output = self.OutputError(message="Not find data into "+self.CURRENT_DIR + '/cntrl.json')
                # print(self.OutputError(message="Not find data into "+self.CURRENT_DIR + '/controller.json'))
                # self.log(message="Not find data into "+self.CURRENT_DIR + '/controller.json')

            return output
        except Exception as e:
            self.LOGGER.error("Error", exc_info=True)

            self.log(str(e) )
            pass
        

    ### occur any exception or error ###
    def OutputError(self,message="Something wrong occurred"):
        data = {
            "result": {
                "status": "error",
                "data": self.CODE_SEND,
                "Message": message
            }
        }
        json_string = json.dumps(data)
        return json_string

    ### Not occur any exception or error ###
    def OutputGood(self,message=""):

        data = {
            "result": {
                "status": "success",
                "data": self.CODE_SEND,
                "Message": message
            }
        }
        json_string = json.dumps(data)
        return json_string
        

def main():
    pass

if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((100, 100))

    last_input = time.time();
    running = True
    while running:
        later = time.time()
        difference = int(later - last_input)
        # print(difference)
        if difference > 10:
            response = controller("b")
            # print(response.RESPONSE)
            last_input = time.time()
            pass
        
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                last_input =  time.time()
                value = chr(event.key)
                response = controller(value)
                print(response.RESPONSE)
               
    pass