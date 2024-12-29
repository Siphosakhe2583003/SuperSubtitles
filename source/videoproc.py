import os
from datetime import datetime

import cv2 as cv
import numpy as np

from utils import format_timestamp

cap = cv.VideoCapture('../videos/EP.1.v0.1639462663.720p.mp4')
fps = cap.get(cv.CAP_PROP_FPS)
timestamps = [cap.get(cv.CAP_PROP_POS_MSEC)]

while cap.isOpened():
    ret, frame = cap.read()
    timestamp = cap.get(cv.CAP_PROP_POS_MSEC)
    if not ret:
        break

    font = cv.FONT_HERSHEY_PLAIN
    hr, min, sec, msec = format_timestamp(timestamp)
    cv.putText(frame, f"{hr}:{min}:{sec}:{msec}", (20, 40), font, 2, (255, 255, 255), 2, cv.LINE_AA)
    timestamps.append(timestamp)
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

