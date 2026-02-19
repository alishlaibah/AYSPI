from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

def mlp_model(input_shape):
    model = Sequential()
    model.add(Dense(128, activation='relu', input_shape=(input_shape,))) # Input layer
    model.add(Dense(64, activation='relu')) # Hidden layer
    model.add(Dense(1, activation='sigmoid')) # Output layer
    return model