from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy
import time
import cv2

face_cascade = cv2.CascadeClassifier('xmls/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('xmls/haarcascade_eye.xml')

##camera = PiCamera()
##camera.resolution = (640, 480)
##camera.framerate = 32
##rawCapture = PiRGBArray(camera, size = (640, 480))

# usb camera
cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
##rawCapture = PiRGBArray(camera, size = (1920, 1080))

time.sleep(0.1)

## for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
while(True):
    ##image = frame.array
    
    # ref : frame captrue result (boolean)
    # frame : Captrue frame
    ref, frame = cap.read()
    if (ref):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle (frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            roi_gray = gray [y: y+h, x: x+w]
            roi_color = frame[y: y+h, x: x+w]

            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle (roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    # show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    #rawCapture.truncate(0)

    # if the 'q' key was pressed, break from the loop
    if key == ord("q"):
        cap.release()
        break
