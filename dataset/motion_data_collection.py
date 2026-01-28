import os
import logging
import cv2
import mediapipe as mp
import numpy as np

all_samples = []

label_map = {
    ' ': 0, 'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,
    'g': 7, 'h': 8, 'i': 9, 'j': 10, 'k': 11, 'l': 12,
    'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17, 'r': 18,
    's': 19, 't': 20, 'u': 21, 'v': 22, 'w': 23, 'x': 24,
    'y': 25, 'z': 26
}

SEQ_FRAMES = 60
FEATURES_PER_FRAME = 63
EXPECTED_LEN = (SEQ_FRAMES * FEATURES_PER_FRAME) + 1  # + label

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
logging.getLogger("mediapipe").setLevel(logging.ERROR)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

webcam = cv2.VideoCapture(1)
webcam.set(cv2.CAP_PROP_FPS, 30)
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


while True:
    success, frame = webcam.read()
    if not success or frame is None:
        continue

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Cam", frame)

    key = cv2.waitKey(1) & 0xFF

    
    if key == ord(" "):
        np.save("A.npy", np.array(all_samples, dtype=np.float32))
        break

    if key == 255:
        continue

    letter = chr(key).lower()

    if letter not in label_map:
        continue

    if not result.multi_hand_landmarks:
        continue

    my_array = []
    frames_collected = 0
    missed_frames = 0
    MAX_MISSES = 10

    while frames_collected < SEQ_FRAMES:
        success, seq_frame = webcam.read()
        if not success or seq_frame is None:
            missed_frames += 1
            if missed_frames > MAX_MISSES:
                break
            continue

        seq_frame = cv2.flip(seq_frame, 1)
        seq_rgb = cv2.cvtColor(seq_frame, cv2.COLOR_BGR2RGB)
        seq_result = hands.process(seq_rgb)

        if not seq_result.multi_hand_landmarks:
            missed_frames += 1
            if missed_frames > MAX_MISSES:
                break
            continue

        hand = seq_result.multi_hand_landmarks[0]

        # append 63 vals
        for lm in hand.landmark:
            my_array.extend([lm.x, lm.y, lm.z])

        frames_collected += 1

    if frames_collected == SEQ_FRAMES:
        my_array.append(label_map[letter])
        if len(my_array) == EXPECTED_LEN:
            all_samples.append(my_array)
            print(f"[OK] Sample saved for '{letter.upper()}' Total: {len(all_samples)}")
        else:
            print(f"[ERROR] Bad sample length ({len(my_array)}), expected {EXPECTED_LEN}. Not saved.")
    else:
        print("[FAIL] Sequence capture failed (too many missed frames). Try again.")

webcam.release()
cv2.destroyAllWindows()
