from dataset.data_loader import X_scaled, Y, scaler # Importing preprocessed data
from sklearn.model_selection import train_test_split
from models.mlp_model import mlp_model
import matplotlib.pyplot as plt
import joblib

X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=42) # Splitting the dataset into training and testing sets

model = mlp_model(X_train.shape[1]) # Creating the model with the input shape

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy']) # Compiling the model

history = model.fit(X_train, Y_train, epochs=50, batch_size=32, validation_data=(X_test, Y_test)) # Training the model

plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Val Accuracy')
plt.legend()
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.show()

model.save("models/mlp_model.h5") # Saving the trained model
joblib.dump(scaler, "models/scaler.pkl") # Saving the scaler for future use