import cv2 # read image/camera/video input
from pyzbar.pyzbar import decode
import time

cap = cv2.VideoCapture(0)
cap.set(3, 640) # width
cap.set(4, 480) # height

used_codes = []

camera = True
while camera == True:
    success, frame = cap.read()

    for code in decode(frame):
        print(code.type)