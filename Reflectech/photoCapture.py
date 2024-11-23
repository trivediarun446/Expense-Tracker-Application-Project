import cv2

camera = cv2.VideoCapture(0)
def nameInput():
    name = input("Enter the name of photo :")
    return name 

def clickPhoto():
    if not camera.isOpened():
       print("Error")

    else:
        while True:
           ret, frame = camera.read()

           if not ret:
            print("Fault")
            break 
           cv2.imshow('camera',frame)

           key = cv2.waitKey(10)

           if camera.isOpened():
            photoName = f"{nameInput()}.jpg"
            cv2.imwrite(photoName,frame)
            print("Captured")
            break 
    camera.release()
    cv2.destroyAllWindows()





