import cv2
import numpy as np
import os
from readPlayerStats import cleanImage, getPlayerDictVID
from BESTSTATSREADER import getAllPlayerDicts

vid = cv2.VideoCapture("./assets/vidTest.mp4")

if (vid.isOpened()==False):
    print("ERROR OPENNING FILE")

pos = 5000

while (vid.isOpened()):
    vid.set(cv2.CAP_PROP_POS_MSEC, 0)
    ret, frame = vid.read()

    if ret == True:
        # cv2.imshow("Frame",frame)

        
        # cleanFrame = frame.copy()
        # cleanFrame = cleanImage(cleanFrame)
        # getPlayerDictVID(1,cleanFrame,frame)
        # getPlayerDictVID(2,cleanFrame,frame)
        getAllPlayerDicts(frame)
        pos+=2000
        vid.set(cv2.CAP_PROP_POS_MSEC, pos)

        
        # os.remove("temp.PNG")
        #does this run sync?

        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break

    else:
        break

vid.release()

cv2.destroyAllWindows()