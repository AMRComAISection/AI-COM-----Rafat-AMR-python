import serial
import os ,sys,time
import glob
import threading

class SerialMonitor(object):

    SERIAL_SELECTED_OPEN = None
    __instance = None

    def __init__(self):
        if SerialMonitor.__instance != None:
            raise Exception("This is already created")

        else:
            ports = SerialMonitor.serial_ports()
            if len(ports) >= 1:
                if SerialMonitor.SERIAL_SELECTED_OPEN == None:
                    SerialMonitor.SERIAL_SELECTED_OPEN = serial.Serial(ports[0], 9600)
                    SerialMonitor.__instance = self
            else:
                print("Sorry ! Can not find any controller arduino")
                exit()
            
    @staticmethod
    def serial_ports():
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

    @staticmethod
    def getInstance():
        if SerialMonitor.__instance == None:
            SerialMonitor()
        return SerialMonitor.__instance


    def read_write(self,data="w"):
        ser = SerialMonitor.SERIAL_SELECTED_OPEN
        ser.write(data.encode('utf-8'))
        while True:
            b = ser.readline()
            str_rn = b.decode()
            str = str_rn.rstrip()
            print(str)
            pass

    def write(self,data="w"):
        ser = SerialMonitor.SERIAL_SELECTED_OPEN
        ser.write(data.encode('utf-8'))
        # ser.write(data.encode('utf-8'))

    def read(self):
        ser = SerialMonitor.SERIAL_SELECTED_OPEN
        while True:
            b = ser.readline()
            str_rn = b.decode()
            str = str_rn.rstrip()
            print(str)
            pass
        
    
def thread_function_read():
    s = SerialMonitor.getInstance()
    s.read()
    pass


def thread_function_write():
    s = SerialMonitor.getInstance()
    s.write("s")

    
if __name__ == "__main__":
    # y = threading.Thread(target=thread_function_write)
    # y.start()


    # x = threading.Thread(target=thread_function_read)
    # x.start()

    
    s = SerialMonitor.getInstance()
    print(s)
    print(s.SERIAL_SELECTED_OPEN)
    # s = SerialMonitor.getInstance()
    

    while True:
        s.write("w")
        print(s.SERIAL_SELECTED_OPEN)
        time.sleep(0.1) 
        pass
   

    # s = SerialMonitor()
    # print(s)
    # print(s.SERIAL_SELECTED_OPEN)

    
    # SerialMonitor.getInstance()
    # print(SerialMonitor.SERIAL_SELECTED_OPEN)
    # SerialMonitor.write('W')
   
    pass