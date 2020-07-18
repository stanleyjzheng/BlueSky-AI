from makedataset import dataset
import torch
import numpy
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import metrics

train, trainLabels, ver, verLabels = dataset()

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(1, 4)),
    keras.layers.Dense(14, activation="relu"),
	keras.layers.Dense(9, activation='relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dense(3, activation="softmax")
    ])

model.compile(
    optimizer= 'adam', 
        loss="categorical_crossentropy", 
        metrics=["accuracy"]
)

model.fit(train, trainLabels, batch_size = 2048, epochs = 100, validation_data = (ver, verLabels))