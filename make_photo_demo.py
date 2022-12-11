import cv2
import imutils
from time import time

cap = cv2.VideoCapture(0)

_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)

start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

alarm = False
detect_mode = False
count = 0
th_sum = 0
while True:
    _, frame = cap.read()
    frame = imutils.resize(frame, width=500)

    if detect_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw
        th_sum = threshold.sum()

        if th_sum > 5000:
            count += 1

        else:
            if count > 0:
                count -= 1

        cv2.imshow("Cam", threshold)
    else:
        cv2.imshow("Cam", frame)

    if count >= 1:
        if not alarm:
            alarm = True
            cv2.imwrite(f"photos/{int(time()*1000)}_G0.jpg", frame)
            alarm = False
            count = 0
    key_pressed = cv2.waitKey(10)

    if key_pressed == ord("t"):
        detect_mode = not detect_mode
        if detect_mode:
            print("detect mode on")
        else:
            print("detect mode off")

    if key_pressed == ord("q"):
        print("camera turn off")
        detect_mode = False
        break

cap.release()
cv2.destroyAllWindows()
