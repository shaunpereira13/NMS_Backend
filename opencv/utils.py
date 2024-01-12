import cv2
def get_info(frame):
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    return gray