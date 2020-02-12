import json
import os ,sys
import glob
import logging
import serial
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

    def SerialInput(self, cod=""):
        try:
            # print(self.CODE_SEND.encode('utf-8'))
            # print(self.serial_ports())
            # print(serial.tools.list_ports.comports())
            # ser = serial.Serial('COM4', 9600, timeout=1)
            # ser.write(self.CODE_SEND.encode('utf-8')) 
            # ser.close() 
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
                output = self.OutputGood(message="Data is accepted")
                self.SerialInput()
            
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
                "Message": message
            }
        }
        json_string = json.dumps(data)
        return json_string
        

if __name__ == "__main__":
    response = controller("s")
     
    print(response.RESPONSE)
    pass