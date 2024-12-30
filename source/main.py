import os

import cv2 as cv
import easyocr
from deep_translator import DeeplTranslator
from utils import are_images_similar, format_timestamp

reader = easyocr.Reader(['ja'])
cap = cv.VideoCapture('../videos/test.mp4')
fps = cap.get(cv.CAP_PROP_FPS)
timestamps = []
data_from_frames = {}
frame_number = 1
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

    if success and not is_similar:
        hr, min, sec, msec = format_timestamp(timestamp)
        formatted_timestamp = f"{hr:02}:{min:02}:{sec:02},{msec}"
        timestamps.append(formatted_timestamp)

        # read text from frames
        frame_text = reader.readtext(frame, detail=0)
        print(frame_text)
        data_from_frames[frame_number] = {
            'timestamp_start': formatted_timestamp,
            'timestamp_end': formatted_timestamp,
            'text': ''.join(frame_text),
        }
        if prev_frame is not None:
            data_from_frames[frame_number - 1] = {
                **data_from_frames[frame_number - 1],
                'timestamp_end': formatted_timestamp
            }
        # cv.imwrite(f'../frames/ {frame_number}.jpg', frame)
        cv.imshow('frame', frame)
        frame_number += 1

    prev_frame = frame
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

file = open('../subtitle/sub.srt', 'w')
for number, value in data_from_frames.items():
    file.write(str(number))
    file.write('\n')
    file.write(f"{value['timestamp_start']} --> {value['timestamp_end']} \n")
    file.write(value['text'])
    file.write('\n')
    file.write('\n')

