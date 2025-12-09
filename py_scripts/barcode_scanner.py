import cv2 # read image/camera/video input
from pyzbar.pyzbar import decode
import time

cap = cv2.VideoCapture(0)
cap.set(3, 640) # width
cap.set(4, 480) # height