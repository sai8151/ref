import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
import pickle

# Define image dimensions
img_width, img_height = 150, 150

# Function to preprocess image
def preprocess_image(img_path, target_size=(150, 150)):
    img = load_img(img_path, target_size=target_size)
    img_array = img_to_array(img)
    img_array = preprocess_input(img_array)  # Normalize pixel values
    return img_array

# Load data from CSV
data = pd.read_csv('data.csv')

# Preprocess images and labels
X = []
y = []
for idx, row in data.iterrows():
    img_path = os.path.join('images', row['filename'])  # Assuming images are stored in 'images' folder
    X.append(preprocess_image(img_path))
    y.append(row['label'])
X = np.array(X)
y = np.array(y)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=46)

# Initialize LabelEncoder
label_encoder = LabelEncoder()

# Encode labels to integers
y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)

# One-hot encode labels for categorical_crossentropy loss
num_classes = len(label_encoder.classes_)
y_train_categorical = np.eye(num_classes)[y_train_encoded]
y_test_categorical = np.eye(num_classes)[y_test_encoded]

# Data augmentation
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')
datagen.fit(X_train)

# Load pre-trained VGG16 model without the top layer
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(150, 150, 3))

# Freeze the base model layers
for layer in base_model.layers:
    layer.trainable = False

# Add custom classification layers
x = base_model.output
x = Flatten()(x)
x = Dense(512, activation='relu')(x)
predictions = Dense(num_classes, activation='softmax')(x)

# Create the final model
model = Model(inputs=base_model.input, outputs=predictions)

# Compile the model
optimizer = Adam(lr=0.001)
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model with data augmentation
epochs = 3
batch_size = 32
steps_per_epoch = len(X_train) // batch_size

history = model.fit(
    datagen.flow(X_train, y_train_categorical, batch_size=batch_size),
    steps_per_epoch=steps_per_epoch,
    epochs=epochs,
    validation_data=(X_test, y_test_categorical))

# Plot training history
plt.figure(figsize=(8, 6))
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test_categorical)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')
model_path = 'saved_model.h5'
model.save(model_path)
print(f'Model saved to {model_path}')

# Save the label encoder
with open('label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)
    print('Label encoder saved to label_encoder.pkl')