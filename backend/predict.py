import os
import json
from typing import Dict, List

# quiet tensorflow logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import joblib
import numpy as np
import tensorflow as tf


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
METADATA_PATH = os.path.join(MODELS_DIR, "metadata.json")

index_to_letter = {
    0: " ", 1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F",
    7: "G", 8: "H", 9: "I", 10: "J", 11: "K", 12: "L",
    13: "M", 14: "N", 15: "O", 16: "P", 17: "Q", 18: "R",
    19: "S", 20: "T", 21: "U", 22: "V", 23: "W", 24: "X",
    25: "Y", 26: "Z",
}


def _load_metadata() -> Dict[str, int | str]:
    if not os.path.exists(METADATA_PATH):
        raise FileNotFoundError(
            f"Missing {METADATA_PATH}. Run training first so metadata is created."
        )
    with open(METADATA_PATH, "r") as f:
        return json.load(f)


_meta = _load_metadata()
SEQ_LEN = int(_meta["seq_len"])
FEATURES_PER_FRAME = int(_meta["features_per_frame"])

MODEL_PATH = os.path.join(MODELS_DIR, _meta.get("model_path", "asl_sequence_classifier.keras"))
SCALER_PATH = os.path.join(MODELS_DIR, _meta.get("scaler_path", "scaler.pkl"))

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

if not os.path.exists(SCALER_PATH):
    raise FileNotFoundError(f"Scaler not found: {SCALER_PATH}")

model = tf.keras.models.load_model(MODEL_PATH, compile=False)
scaler = joblib.load(SCALER_PATH)


def _resample_or_pad(seq: np.ndarray, target_frames: int) -> np.ndarray:
    frames = seq.shape[0]

    if frames == target_frames:
        return seq

    if frames < target_frames:
        pad_count = target_frames - frames
        pad = np.repeat(seq[-1][None, :], pad_count, axis=0)
        return np.vstack([seq, pad])

    idx = np.linspace(0, frames - 1, target_frames).astype(int)
    return seq[idx]


def _wrist_relative(seq: np.ndarray) -> np.ndarray:
    seq_rel = seq.copy()
    for t in range(seq_rel.shape[0]):
        frame = seq_rel[t].reshape(21, 3)
        wrist = frame[0]
        frame = frame - wrist
        seq_rel[t] = frame.reshape(63)
    return seq_rel


def _prepare_sequence(landmarks: List[float]) -> np.ndarray:
    arr = np.array(landmarks, dtype=np.float32).reshape(-1)

    if arr.size % FEATURES_PER_FRAME != 0:
        raise ValueError(
            f"Expected landmarks multiple of {FEATURES_PER_FRAME}, got {arr.size}"
        )

    frames = arr.size // FEATURES_PER_FRAME
    seq = arr.reshape(frames, FEATURES_PER_FRAME)

    if frames != SEQ_LEN:
        seq = _resample_or_pad(seq, SEQ_LEN)

    return seq


def predict(landmarks: List[float]) -> Dict[str, float | str]:
    if not landmarks:
        return {"error": "No landmarks provided."}

    try:
        seq = _prepare_sequence(landmarks)
    except ValueError as exc:
        return {"error": str(exc)}

    seq = _wrist_relative(seq)

    seq_flat = seq.reshape(SEQ_LEN, FEATURES_PER_FRAME)
    seq_scaled = scaler.transform(seq_flat)
    seq_input = seq_scaled.reshape(1, SEQ_LEN, FEATURES_PER_FRAME)

    probs = model.predict(seq_input, verbose=0)[0]
    pred_index = int(np.argmax(probs))
    pred_conf = float(np.max(probs))

    return {
        "letter": index_to_letter.get(pred_index, "?"),
        "confidence": pred_conf,
        "index": pred_index,
    }


def get_metadata() -> Dict[str, int]:
    return {
        "seq_len": SEQ_LEN,
        "features_per_frame": FEATURES_PER_FRAME,
        "num_classes": int(_meta.get("num_classes", 0)),
    }
