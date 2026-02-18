import os
import glob

import numpy as np

FEATURES_PER_FRAME = 63
DEFAULT_SEQ_LEN = 30


def resample_or_pad(seq: np.ndarray, target_frames: int) -> np.ndarray:
    frames = seq.shape[0]

    if frames == target_frames:
        return seq

    # pad by repeating last frame
    if frames < target_frames:
        pad_count = target_frames - frames
        pad = np.repeat(seq[-1][None, :], pad_count, axis=0)
        return np.vstack([seq, pad])

    # downsample evenly
    idx = np.linspace(0, frames - 1, target_frames).astype(int)
    return seq[idx]


def parse_sample(sample):

    if isinstance(sample, (list, tuple)) and len(sample) == 2:
        feats, label = sample
        feats = np.array(feats, dtype=np.float32)
        label = int(label)

    else:
        arr = np.array(sample, dtype=object)

        if hasattr(arr, "shape") and arr.shape == (2,):
            feats = np.array(arr[0], dtype=np.float32)
            label = int(arr[1])
        else:
            arr = np.array(sample, dtype=np.float32)
            if arr.ndim != 1:
                raise ValueError(f"Unsupported sample ndim: {arr.ndim}")

            label = int(arr[-1])
            feats = arr[:-1].astype(np.float32)

    if feats.ndim == 1:
        if feats.shape[0] == FEATURES_PER_FRAME:
            seq = feats.reshape(1, FEATURES_PER_FRAME)
        else:
            if feats.shape[0] % FEATURES_PER_FRAME != 0:
                raise ValueError(
                    f"Feature length {feats.shape[0]} not divisible by {FEATURES_PER_FRAME}"
                )
            frames = feats.shape[0] // FEATURES_PER_FRAME
            seq = feats.reshape(frames, FEATURES_PER_FRAME)

    elif feats.ndim == 2:
        if feats.shape[1] != FEATURES_PER_FRAME:
            raise ValueError(f"Wrong shape. Expected shape (_,63) but got {feats.shape}")
        seq = feats

    else:
        raise ValueError(f"Unsupported feats shape: {feats.shape}")

    return seq.astype(np.float32), label


def normalize_folder(input_folder: str, output_folder: str, seq_len: int = DEFAULT_SEQ_LEN):
    os.makedirs(output_folder, exist_ok=True)
    npy_files = sorted(glob.glob(os.path.join(input_folder, "*.npy")))

    for file_path in npy_files:
        fname = os.path.basename(file_path)
        data = np.load(file_path, allow_pickle=True)

        normalized = []
        for sample in data:
            seq, label = parse_sample(sample)
            seq = resample_or_pad(seq, seq_len)

            flat = seq.flatten()  # (seq_len*63,)
            out = np.concatenate([flat, [label]]).astype(np.float32)
            normalized.append(out)

        normalized = np.array(normalized, dtype=np.float32)
        out_path = os.path.join(output_folder, fname)
        np.save(out_path, normalized)


def load_normalized_dataset(normalized_folder: str, seq_len: int = DEFAULT_SEQ_LEN):
    npy_files = sorted(glob.glob(os.path.join(normalized_folder, "*.npy")))
    if not npy_files:
        raise FileNotFoundError(f"No .npy files found in: {normalized_folder}")

    X_list, y_list = [], []

    for file_path in npy_files:
        data = np.load(file_path, allow_pickle=True)

        for sample in data:
            sample = np.array(sample, dtype=np.float32)
            label = int(sample[-1])
            feats = sample[:-1]

            seq = feats.reshape(seq_len, FEATURES_PER_FRAME)
            X_list.append(seq)
            y_list.append(label)

    X = np.array(X_list, dtype=np.float32)
    y = np.array(y_list, dtype=np.int64)
    return X, y


def make_wrist_relative(X: np.ndarray) -> np.ndarray:
    X_rel = X.copy()

    for i in range(X_rel.shape[0]):
        for t in range(X_rel.shape[1]):
            frame = X_rel[i, t].reshape(21, 3)
            wrist = frame[0]
            frame = frame - wrist
            X_rel[i, t] = frame.reshape(63)

    return X_rel


if __name__ == "__main__":
    in_folder = "dataset"
    out_folder = "dataset_normalized"
    normalize_folder(in_folder, out_folder, seq_len=DEFAULT_SEQ_LEN)
    X, y = load_normalized_dataset(out_folder, seq_len=DEFAULT_SEQ_LEN)
