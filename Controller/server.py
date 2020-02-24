import os
import socket
import re
import uuid
import logging
from datetime import datetime
import pyfiglet 
import multiprocessing
import time
import threading
from api.controller import controller

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

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    def client(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            sendData = self.BREAK_CODE
            s.sendall(sendData.encode('utf-8'))
            data = s.recv(2048)

        # print('Received', repr(data))

    def run(self): 
        self.START_TIME = time.time()
        while True: 
            later = time.time()
            difference = int(later - self.START_TIME)
            if self.stopped(): 
                return
            if difference >= 1 and difference % self.BREAK_EXECTION_TIME == 0 :
                self.HOST = self.get_ip_address()
                self.client()
                now = datetime.now()
                print(str(now.strftime("%d-%m-%Y__%H:%M:%S"))+"---Auto Break Execute every "+str(difference)+" s") 
                pass    
            time.sleep(1)
            
class MyControllerServer:
    HOST = "localhost"
    PORT = 28280
    MAC = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER_NAME = "No Name Server"
    ETHERNET_HOST = ""
    BUFFER_SIZE = 1024
    LOGGER = None
    LOGGER_FILE_NAME = ""
    LAST_CLIENT_ACCEPT = time.time()

    def __init__(self,server_name="AMR CONTROLLER SERVER",  port=0, buffer=1024):
        self.BUFFER_SIZE = buffer
        self.SERVER_NAME = server_name
        self.PC_NAME = socket.gethostname()
        # self.HOST = socket.gethostbyname(self.PC_NAME)
        self.HOST = self.get_ip_address()
        
        ''' not work in linux '''
        # self.SOCKET.bind((self.HOST, 0))
        # self.PORT = self.SOCKET.getsockname()[1]

        if port != 0:
            self.PORT = port
            
        now = datetime.now()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            soc.bind((self.HOST, self.PORT))
        pass

        fileName = os.path.dirname(os.path.realpath(__file__))+"/log/_SERVER_LOG_"+str(now.strftime("%d-%m-%Y__%H-%M-%S")) + ".log"
        self.LOGGER_FILE_NAME = fileName
        logging.basicConfig(filename= fileName, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    filemode='w')
        #Creating an object 
        logger=logging.getLogger() 
        
        #Setting the threshold of logger to DEBUG 
        logger.setLevel(logging.DEBUG) 
        self.LOGGER = logger

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    def creatServer(self):
        try:
            result = pyfiglet.figlet_format(self.SERVER_NAME) 
            print(result)
            print("PC Name : ", self.PC_NAME)
            print("host : ", self.HOST)
            print("port : ", self.PORT)
            print("buffer size : ", self.BUFFER_SIZE)
            print("log path : ", self.LOGGER_FILE_NAME)
            self.LOGGER.info(result)
            self.LOGGER.info(self.PC_NAME)
            self.LOGGER.info(self.HOST)
            self.LOGGER.info(self.PORT)
            self.LOGGER.info(self.BUFFER_SIZE)
            self.LOGGER.info(self.LOGGER_FILE_NAME)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:

                soc.bind((self.HOST, self.PORT))
                
                while True:
                    
                    soc.listen()
                    t1 = MyThread() 
                    t1.start()
                   
                    conn, addr = soc.accept()
                    t1.stop()
                    with conn:
                        now = datetime.now()
                        print(str(now.strftime("%d-%m-%Y__%H-%M-%S")) +"---"+str(addr))
                        self.LOGGER.info("***Start Connection***")
                        self.LOGGER.info(addr)
                        while True:
                            data = conn.recv(self.BUFFER_SIZE)
                            if not data:
                                self.LOGGER.info("***Close Connection***")
                                self.LOGGER.info(addr)
                                break

                            self.LOGGER.info(data)
                            #print(data)
                            #print(data.decode("utf-8"))
                            response = controller( data.decode("utf-8") )
                            #print(response.RESPONSE)
                            self.LOGGER.info(response.RESPONSE)
                            conn.sendall(response.RESPONSE.encode('utf-8'))
            pass

        except Exception:
            self.LOGGER.error("Error", exc_info=True)
            raise
        pass


def main():
    controller = MyControllerServer(port=28280, buffer=1024)
    controller.creatServer()
    pass


if __name__ == "__main__":
    # print (get_ip_address())
    # print (socket.gethostbyname(socket.gethostname()))
    while True:
        manager = multiprocessing.Manager()
        timer_return = manager.list()
        timer = multiprocessing.Process(target=main)
        timer.start()    
        timer.join() 


       
        
