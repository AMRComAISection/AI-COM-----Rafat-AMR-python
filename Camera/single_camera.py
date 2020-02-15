import numpy as np
import cv2
import threading

def camera(port=0):
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

        # Display the resulting frame
        cv2.imshow('Camera '+str(port),gray)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
def camera_count():
    count = 0
    for i in range(10):
        
        cap = cv2.VideoCapture(i,cv2.CAP_DSHOW)
        ret, frame = cap.read()
        if ret == False:
            break
        cap.release()
        cv2.destroyAllWindows()
        count += 1
        pass
    return count

if __name__ == "__main__":

    count = camera_count()
    print("Number of camera : "+str(count))
    inp = input("Select A camera ")
    if int(inp) < count:
        camera(int(inp))
    else:
        print("please select number between 0 to "+str(count-1))
    pass