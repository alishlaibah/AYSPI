import os
import sys
import json

import joblib
import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from dataset.data_loader import (
    normalize_folder,
    load_normalized_dataset,
    make_wrist_relative
)

from models.asl_sequence_classifier import build_asl_sequence_classifier


def resolve_normalized_folder(project_root: str) -> str:
    option_a = os.path.join(project_root, "dataset_normalized")
    option_b = os.path.join(project_root, "dataset", "normalized")

    if os.path.isdir(option_a):
        return option_a
    return option_b


def folder_has_files(path: str) -> bool:
    if not os.path.isdir(path):
        return False
    for root, _, files in os.walk(path):
        if len(files) > 0:
            return True
    return False


def main():
    tf.keras.utils.set_random_seed(42)

    dataset_folder = os.path.join(PROJECT_ROOT, "dataset")
    normalized_folder = resolve_normalized_folder(PROJECT_ROOT)

    models_folder = os.path.join(PROJECT_ROOT, "models")
    os.makedirs(models_folder, exist_ok=True)

    if folder_has_files(normalized_folder):
        print(f"using existing normalized dataset -> {normalized_folder}")
    else:
        os.makedirs(normalized_folder, exist_ok=True)
        normalize_folder(dataset_folder, normalized_folder)

    X, y = load_normalized_dataset(normalized_folder)

    if X.ndim != 3:
        raise ValueError(f"Expected X shape (N, seq_len, features). Got: {X.shape}")

    seq_len = X.shape[1]
    features_per_frame = X.shape[2]

    X = make_wrist_relative(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    scaler = StandardScaler()

    X_train_2d = X_train.reshape(-1, features_per_frame)
    X_test_2d = X_test.reshape(-1, features_per_frame)

    X_train_scaled = scaler.fit_transform(X_train_2d).reshape(-1, seq_len, features_per_frame)
    X_test_scaled = scaler.transform(X_test_2d).reshape(-1, seq_len, features_per_frame)

    scaler_path = os.path.join(models_folder, "scaler.pkl")
    joblib.dump(scaler, scaler_path)

    num_classes = int(np.max(y)) + 1

    model = build_asl_sequence_classifier(
        num_classes=num_classes,
        seq_len=seq_len,
        features_per_frame=features_per_frame
    )

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    model.summary()

    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            filepath=os.path.join(models_folder, "best_asl_sequence_classifier.keras"),
            monitor="val_accuracy",
            save_best_only=True,
            mode="max",
            verbose=1,
        ),
        tf.keras.callbacks.EarlyStopping(
            monitor="val_accuracy",
            patience=12,
            restore_best_weights=True
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=4,
            min_lr=1e-5
        )
    ]

    history = model.fit(
        X_train_scaled, y_train,
        validation_data=(X_test_scaled, y_test),
        epochs=100,
        batch_size=64,
        callbacks=callbacks
    )

    loss, acc = model.evaluate(X_test_scaled, y_test, verbose=0)

    y_pred = np.argmax(model.predict(X_test_scaled, verbose=0), axis=1)

    final_model_path = os.path.join(models_folder, "asl_sequence_classifier.keras")
    model.save(final_model_path)

    metadata = {
        "seq_len": int(seq_len),
        "features_per_frame": int(features_per_frame),
        "num_classes": int(num_classes),
        "scaler_path": "scaler.pkl",
        "model_path": "asl_sequence_classifier.keras",
        "best_model_path": "best_asl_sequence_classifier.keras",
        "normalized_folder_used": os.path.relpath(normalized_folder, PROJECT_ROOT),
    }

    metadata_path = os.path.join(models_folder, "metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)


if __name__ == "__main__":
    main()
