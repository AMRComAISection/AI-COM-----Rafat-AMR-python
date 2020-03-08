# AMR

this pip depends on python version like (pip and pip3)

### pyfiglet
pip install pyfiglet
### pyserial 
pip install pyserial
### pygame 
pip install pygame
### pynput 
pip install pynput

### opencv setup :
https://www.youtube.com/watch?v=xlmJsTeZL3w

https://www.pyimagesearch.com/2019/09/16/install-opencv-4-on-raspberry-pi-4-and-raspbian-buster/

pip install opencv-python


# RUN PROGRAMME FILE
 
### CONTROLLERS
1. server.py 
2. client.py
3. key_xbox_contrl_Client.py
4. controller.py
5. cntrl.json
6. https://github.com/martinohanlon/XboxController

### CAMERA
 
 
# HOW TO RUN SSH CONNECTION 

if you want please contact AMR Communication & AI team

# SOME PROBLEMS

1. AUTO PORT SELECTION LOGIC `getresponse()` - this function location is `/AMR/Controller/api/controller.py` 


# HOW TO WORK

1. Install all the required package

2. In `raspberry pi` run `Controller\server.py` after running you can see this type of window -

```
pygame 1.9.6
Hello from the pygame community. https://www.pygame.org/contribute.html
pygame 1.9.6
Hello from the pygame community. https://www.pygame.org/contribute.html
pygame 1.9.6
Hello from the pygame community. https://www.pygame.org/contribute.html
    _    __  __ ____
   / \  |  \/  |  _ \
  / _ \ | |\/| | |_) |
 / ___ \| |  | |  _ <
/_/   \_\_|  |_|_| \_\

  ____ ___  _   _ _____ ____   ___  _     _     _____ ____
 / ___/ _ \| \ | |_   _|  _ \ / _ \| |   | |   | ____|  _ \
| |  | | | |  \| | | | | |_) | | | | |   | |   |  _| | |_) |
| |__| |_| | |\  | | | |  _ <| |_| | |___| |___| |___|  _ <
 \____\___/|_| \_| |_| |_| \_\\___/|_____|_____|_____|_| \_\

 ____  _____ ______     _______ ____
/ ___|| ____|  _ \ \   / / ____|  _ \
\___ \|  _| | |_) \ \ / /|  _| | |_) |
 ___) | |___|  _ < \ V / | |___|  _ <
|____/|_____|_| \_\ \_/  |_____|_| \_\


PC Name :  ROOT10
host :  192.168.123.103
port :  28280
buffer size :  1024
log path :  c:\Users\rafat\My_Github\AMR\AMR\Controller/log/_SERVER_LOG_08-03-2020__16-22-58.log
```

3. Clone project in your computer

4. Then goto project path and open `Controller\key_xbox_contrl_Client.py` file .Then change HOST variable which show after runing `server.py` in `raspberry pi` for example - ` HOST = '192.168.123.103'  `

5. Then save the file and run `Controller\key_xbox_contrl_Client.py` with python 

