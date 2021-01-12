import cv2
import numpy as np
import os
from readPlayerStats import cleanImage, getPlayerDictVID

vid = cv2.VideoCapture("vidTest.mp4")

if (vid.isOpened()==False):
    print("ERROR OPENNING FILE")

pos = 0

while (vid.isOpened()):
    ret, frame = vid.read()

    if ret == True:
        # cv2.imshow("Frame",frame)

        cv2.imshow("curr",frame)
        cv2.waitKey(3000)
        cleanFrame = frame.copy()
        cleanFrame = cleanImage(cleanFrame)
        getPlayerDictVID(1,cleanFrame,frame)
        pos+=2000
        vid.set(cv2.CAP_PROP_POS_MSEC, pos)

        # cv2.imwrite("temp.PNG",frame)
        # os.remove("temp.PNG")
        #does this run sync?

        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break

    else:
        break

vid.release()

cv2.destroyAllWindows()