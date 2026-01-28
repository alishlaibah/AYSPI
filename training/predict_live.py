import os
import json
import time
from collections import deque

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import cv2
import mediapipe as mp
import numpy as np
import joblib
import tensorflow as tf



MODELS_DIR = "models"
METADATA_PATH = os.path.join(MODELS_DIR, "metadata.json")


index_to_letter = {
    0: " ", 1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F",
    7: "G", 8: "H", 9: "I", 10: "J", 11: "K", 12: "L",
    13: "M", 14: "N", 15: "O", 16: "P", 17: "Q", 18: "R",
    19: "S", 20: "T", 21: "U", 22: "V", 23: "W", 24: "X",
    25: "Y", 26: "Z"
}


if not os.path.exists(METADATA_PATH):
    raise FileNotFoundError(
        f"Missing {METADATA_PATH}. Run training first so metadata is created."
    )

with open(METADATA_PATH, "r") as f:
    meta = json.load(f)

SEQ_LEN = int(meta["seq_len"])
FEATURES_PER_FRAME = int(meta["features_per_frame"])

MODEL_PATH = os.path.join(MODELS_DIR, meta.get("model_path", "asl_sequence_classifier.keras"))
SCALER_PATH = os.path.join(MODELS_DIR, meta.get("scaler_path", "scaler.pkl"))


if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

if not os.path.exists(SCALER_PATH):
    raise FileNotFoundError(f"Scaler not found: {SCALER_PATH}")

model = tf.keras.models.load_model(MODEL_PATH, compile=False)
scaler = joblib.load(SCALER_PATH)


mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.70,
    min_tracking_confidence=0.70
)


webcam = cv2.VideoCapture(0)
webcam.set(cv2.CAP_PROP_FPS, 30)
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

sequence_buffer = deque(maxlen=SEQ_LEN)

pred_buffer = deque(maxlen=8)


def extract_frame_features(hand_landmarks) -> np.ndarray:
    arr = []
    for lm in hand_landmarks.landmark:
        arr.extend([lm.x, lm.y, lm.z])
    return np.array(arr, dtype=np.float32)


def wrist_relative_frame(frame63: np.ndarray) -> np.ndarray:
    pts = frame63.reshape(21, 3)
    wrist = pts[0].copy()
    pts = pts - wrist
    return pts.reshape(63)


def stable_vote(indices):
    if len(indices) == 0:
        return None
    vals, counts = np.unique(np.array(indices), return_counts=True)
    return int(vals[np.argmax(counts)])


last_time = time.time()
fps = 0.0

while True:
    success, frame = webcam.read()
    if not success or frame is None:
        continue

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    prediction_text = "No Hand"
    confidence_text = ""
    fps_text = ""

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        frame63 = extract_frame_features(hand)

        if frame63.shape[0] == FEATURES_PER_FRAME:
            frame63 = wrist_relative_frame(frame63)

            sequence_buffer.append(frame63)

            if len(sequence_buffer) == SEQ_LEN:
                seq = np.array(sequence_buffer, dtype=np.float32) 

                seq_flat = seq.reshape(SEQ_LEN, FEATURES_PER_FRAME)
                seq_scaled = scaler.transform(seq_flat)
                seq_input = seq_scaled.reshape(1, SEQ_LEN, FEATURES_PER_FRAME)

                probs = model.predict(seq_input, verbose=0)[0]
                pred_index = int(np.argmax(probs))
                pred_conf = float(np.max(probs))

                pred_buffer.append(pred_index)
                stable_index = stable_vote(pred_buffer)

                pred_letter = index_to_letter.get(stable_index, "?")

                prediction_text = f"Prediction: {pred_letter}"
                confidence_text = f"Confidence: {pred_conf:.2f}"

    now = time.time()
    dt = now - last_time
    last_time = now
    if dt > 0:
        fps = 0.9 * fps + 0.1 * (1.0 / dt)
    fps_text = f"FPS: {fps:.1f}"

    cv2.putText(frame, prediction_text, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

    if confidence_text:
        cv2.putText(frame, confidence_text, (10, 65),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.putText(frame, fps_text, (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("ASL Live Prediction", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break


webcam.release()
cv2.destroyAllWindows()
