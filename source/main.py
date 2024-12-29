import os

import cv2 as cv
import easyocr
from deep_translator import GoogleTranslator

from utils import are_images_similar, format_timestamp

reader = easyocr.Reader(['ja'])
cap = cv.VideoCapture('../videos/EP.1.v0.1639462663.720p.mp4')
fps = cap.get(cv.CAP_PROP_FPS)
timestamps = []
data_from_frames = {}
frame_number = 0
prev_frame = None
font = cv.FONT_HERSHEY_PLAIN

if not os.path.exists('../frames'):
    os.makedirs('../frames')

while cap.isOpened():
    success, frame = cap.read()
    timestamp = cap.get(cv.CAP_PROP_POS_MSEC)
    is_similar = False

    if prev_frame is not None and frame is not None:
        is_similar = are_images_similar(frame, prev_frame)
    else:
        is_similar = False

    if success and not is_similar:
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        hr, min, sec, msec = format_timestamp(timestamp)
        formatted_timestamp = f"{hr}:{min}:{sec}:{msec}"
        timestamps.append(formatted_timestamp)

        # read the text from frames
        frame_data = reader.readtext(frame, detail=0)
        text = ' '.join(frame_data)
        translated_text = ''
        if text != '':
            translated_text = GoogleTranslator(source='ja', target='en').translate(text)

        cv.putText(frame, translated_text, (20, 2000), font, 1, (255, 255, 255), 2, cv.LINE_AA)

        # data_from_frames[frame_number] = [timestamp, frame_data]
        # print(frame_data)
        # cv.imwrite(f'../frames/ {frame_number}.jpg', frame)
        cv.imshow('frame', frame)
        frame_number += 1

    prev_frame = frame
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

#for key, data in data_from_frames.values():
#   print(data)



