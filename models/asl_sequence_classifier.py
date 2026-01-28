# models/asl_sequence_classifier.py

from tensorflow.keras import Sequential
from tensorflow.keras.layers import (
    InputLayer,
    Conv1D,
    BatchNormalization,
    Dropout,
    Bidirectional,
    GRU,
    Dense,
    GlobalAveragePooling1D,
)
from tensorflow.keras.regularizers import l2


def build_asl_sequence_classifier(
    num_classes: int,
    seq_len: int,
    features_per_frame: int,
    conv_dropout: float = 0.20,
    rnn_dropout: float = 0.30,
    dense_dropout: float = 0.30,
    l2_strength: float = 1e-4,
):

    model = Sequential(
        [
            InputLayer(input_shape=(seq_len, features_per_frame)),

            Conv1D(
                128,
                kernel_size=3,
                activation="relu",
                padding="same",
                kernel_regularizer=l2(l2_strength),
            ),
            BatchNormalization(),
            Dropout(conv_dropout),

            Conv1D(
                256,
                kernel_size=3,
                activation="relu",
                padding="same",
                kernel_regularizer=l2(l2_strength),
            ),
            BatchNormalization(),
            Dropout(conv_dropout),

            Bidirectional(GRU(128, return_sequences=True)),
            BatchNormalization(),
            Dropout(rnn_dropout),

            GlobalAveragePooling1D(),

            Dense(128, activation="relu", kernel_regularizer=l2(l2_strength)),
            Dropout(dense_dropout),

            Dense(num_classes, activation="softmax"),
        ]
    )

    return model


if __name__ == "__main__":
    model = build_asl_sequence_classifier(num_classes=27, seq_len=30, features_per_frame=63)
    model.summary()
