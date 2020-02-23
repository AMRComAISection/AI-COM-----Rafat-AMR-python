import os, sys
import time
import pygame


joysticks = []
pygame.init()

def Event() :
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                exit()
        elif event.type == pygame.KEYDOWN:
                value = chr(event.key)
                # response = controller(value)
                print("key down = "+value)
        elif event.type == pygame.KEYUP:
                value = chr(event.key)
                # response = controller(value)
                print("key up = "+value)
        elif event.type == pygame.JOYAXISMOTION:
            print("Joystick '",joysticks[event.joy].get_name(),"' axis",event.axis,"motion.")
        elif event.type == pygame.JOYBALLMOTION:
            print("Joystick '",joysticks[event.joy].get_name(),"' ball",event.axis,"motion.")     
        elif event.type == pygame.JOYHATMOTION:
            print("Joystick '",joysticks[event.joy].get_name(),"' hat",event.hat," moved.")

        elif event.type == pygame.JOYBUTTONDOWN:
            print("Joystick '",joysticks[event.joy].get_name(),"' button",event.button,"down.")
        elif event.type == pygame.JOYBUTTONUP:
             print("Joystick '",joysticks[event.joy].get_name(),"' button",event.button,"up.")
       
        
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


if __name__ == "__main__":
    screen = pygame.display.set_mode((500, 500))
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


