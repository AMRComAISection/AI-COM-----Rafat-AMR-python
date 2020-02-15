import numpy as np
import cv2
import threading

def camera(port=0):
    cap = cv2.VideoCapture(port,cv2.CAP_DSHOW)

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
    for cam_p in range(camera_count()):
        try:
            x = threading.Thread(target=camera, args=(cam_p,))
            x.start()
        except:
            print ("Error: unable to start thread")
        # camera(cam_p)
        pass
    
    pass