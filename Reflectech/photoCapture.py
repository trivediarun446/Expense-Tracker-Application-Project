import cv2
import time 


def nameInput():
    name = input("Enter the name of photo :")
    return name 

camera = cv2.VideoCapture(0)

def click_photo():
    
    if not camera.isOpened():
        print("camera is not opened ")
        return None
    
    time.sleep(2)

    ret,frame= camera.read()

    if not ret:
        print("Frame is not create")
        camera.release()
        cv2.destroyAllWindows()
        return None

    photo_name = f"{nameInput()}.jpeg"

    if cv2.imwrite(photo_name, frame):
        print("successfully captured image")
    
    else:
        print("There is some error")

    camera.release()
    cv2.destroyAllWindows()
    return frame 