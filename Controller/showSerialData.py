import serial
import time
import sys
import os
import glob

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
    
def serial_read(port_input = 0):
    ports = serial_ports()
    ser = serial.Serial(ports[port_input], 9600)
    while True:
        b = ser.readline()
        str_rn = b.decode()
        str = str_rn.rstrip()
        print(str)
        pass
  
    
    pass

if __name__ == "__main__":
    ports = serial_ports()
    print("All Ports in list : ",ports)
    for port in ports:
        print(ports.index(port),"=>",port)
        pass
    if len(ports) >= 1:
        x = input("select one port and press enter : ")
        selectedPort = int(x)
        if selectedPort < len(ports):
            serial_read(0)
        else:
            print("Select correct port")        
        
    else:
        print("NO SERIAL PORT FOUND")
    pass
