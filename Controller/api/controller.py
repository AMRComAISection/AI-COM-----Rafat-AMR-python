import json
import os ,sys
import glob
import logging
import serial
import pygame
import time
import multiprocessing
import threading
from datetime import datetime

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
                
                # this line will change different OS in different logic 
                if len(self.serial_ports()) > 1:
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


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import sys, tty, termios

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()
       

class MyThread(threading.Thread): 
  
    # Thread class with a _stop() method.  
    # The thread itself has to check 
    # regularly for the stopped() condition. 
    START_TIME = None
    HOST = '192.168.123.101'  
    PORT = 28280 
    BREAK_CODE = "k"
    BREAK_EXECTION_TIME = 10
    
  
    def __init__(self, *args, **kwargs): 
        super(MyThread, self).__init__(*args, **kwargs) 
        self._stop = threading.Event() 
  
    # function using _stop function 
    def stop(self): 
        self._stop.set() 
  
    def stopped(self): 
        return self._stop.isSet() 

    def run(self): 
        self.START_TIME = time.time()
        while True: 
            later = time.time()
            difference = int(later - self.START_TIME)
            if self.stopped(): 
                return
            if difference >= 1 and difference % self.BREAK_EXECTION_TIME == 0 :
                response = controller(self.BREAK_CODE)
                now = datetime.now()
                print(str(now.strftime("%d-%m-%Y__%H:%M:%S"))+"---Auto Break Execute every "+str(difference)+" s") 
                print(response.RESPONSE)
                pass    
            time.sleep(1)
 

def main_pygame():
    pygame.init()
    screen = pygame.display.set_mode((100, 100))

    last_input = time.time()
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

key_stack = [] 
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

def main_normal():
    while True:
        # getch = _Getch()
        # t1 = MyThread() 
        # t1.start()
        print ("Please enter a word: ")
        # x = getch()
        x = input()
        response = controller(x)
        print(response.RESPONSE)
        # t1.stop()
           
    pass


if __name__ == "__main__":
    # main_pygame()
    main_normal()
    pass