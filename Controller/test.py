import os ,sys
import glob
import serial
import msvcrt
from api.controller import controller
from pynput import keyboard

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

def keyboard_fun():
    
    def on_press(key):
        try:
            data_key_event(key.char,'keyboard')
            # print('alphanumeric key {0} pressed'.format(key.char))
        
        except AttributeError:
            print('special key {0} pressed'.format(
            key))
        pass

    def on_release(key):
        data_key_event('k','keyboard')
        
        if key == keyboard.Key.esc:
            # Stop listener
            return False
        pass

    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

    pass


if __name__ == "__main__":
    keyboard_fun()
    pass

    #while True:
        # getch = _Getch()
        # print ("Please enter something: ")
        # x = getch()
        # print(x)
        
        # print ("Please enter a value.")
        # char = msvcrt.getch()
        # print(char)
    # print(serial_ports())
