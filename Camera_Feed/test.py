import cv2
import numpy as np

cap = cv2.VideoCapture('rtsp://root:360CameraRobot@192.168.1.57:554/live.sdp')

while(True):
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()