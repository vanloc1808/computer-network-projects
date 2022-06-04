import cv2

import time

# cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 24.0, (640, 480))

if vc.isOpened():
    rval, frame = vc.read()
else:
    rval = False

REC_TIME = 10

t = time.time()

while time.time() - t < REC_TIME:
    # cv2.imshow("preview", frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    out.write(frame)
    rval, frame = vc.read()
    # key = cv2.waitKey(20)
    # if key == 27:
    #     break

vc.release()
out.release()
# cv2.destroyWindow("preview")