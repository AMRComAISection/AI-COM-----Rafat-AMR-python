import os
import socket
import re
import uuid
import logging
from datetime import datetime
import pyfiglet 
import multiprocessing

from api.controller import controller


class MyControllerServer:
    HOST = "localhost"
    PORT = 2564
    MAC = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER_NAME = "No Name Server"
    ETHERNET_HOST = ""
    BUFFER_SIZE = 1024
    LOGGER = None
    LOGGER_FILE_NAME = ""

    def __init__(self,server_name="AMR CONTROLLER SERVER",  port=0, buffer=1024):
        self.BUFFER_SIZE = buffer
        self.SERVER_NAME = server_name
        self.PC_NAME = socket.gethostname()
        self.HOST = socket.gethostbyname(self.PC_NAME)
        
        self.SOCKET.bind((self.HOST, 0))
        self.PORT = self.SOCKET.getsockname()[1]

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
                    conn, addr = soc.accept()
                    with conn:
                        print(addr)
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
    while True:
        manager = multiprocessing.Manager()
        timer_return = manager.list()
        timer = multiprocessing.Process(target=main)
        timer.start()
        timer.join() 
