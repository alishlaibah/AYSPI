import os
import logging

import cv2
import mediapipe as mp
import numpy as np

all_samples = []
label_map = {
    ' ' : 0, 'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,
    'g': 7, 'h': 8, 'i': 9, 'j': 10, 'k': 11, 'l': 12,
    'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17, 'r': 18,
    's': 19, 't': 20, 'u': 21, 'v': 22, 'w': 23, 'x': 24,
    'y': 25, 'z': 26
}

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('mediapipe').setLevel(logging.ERROR)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.9,
    min_tracking_confidence=0.9
)

webcam = cv2.VideoCapture(0)
webcam.set(cv2.CAP_PROP_FPS, 30)
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


while True:
    success, frame = webcam.read()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand, connections=mp_hands.HAND_CONNECTIONS)

        letter = cv2.waitKey(1)
        try:
            letter = chr(letter).lower()
        except:
            letter = ""

        if letter in label_map:
            hand = result.multi_hand_landmarks[0]
            my_array = []

            for lm in hand.landmark:
                my_array.extend([lm.x, lm.y, lm.z])

            my_array.append(label_map[letter])
            all_samples.append(my_array)
            print(f"Sample saved for letter '{letter.upper()}")

    cv2.imshow("Cam", frame)

    key = cv2.waitKey(1)
    if key == ord(" "):
        np.save("A.npy", np.array(all_samples))
        break

webcam.release()
cv2.destroyAllWindows()
