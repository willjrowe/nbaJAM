import cv2
import numpy as np
import os
from BESTSTATSREADER import getAllPlayerDicts

vid = cv2.VideoCapture("./5min.mp4")

if (vid.isOpened()==False):
    print("ERROR OPENNING FILE")

pos = 277300

while (vid.isOpened()):
    vid.set(cv2.CAP_PROP_POS_MSEC, pos)
    ret, frame = vid.read()

    if ret == True:
        getAllPlayerDicts(frame)
        pos+=900
        print(pos)
        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break

    else:
        break

vid.release()

cv2.destroyAllWindows()