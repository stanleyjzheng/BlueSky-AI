# experimental optimizer func:
#optimizer = keras.optimizers.SGD(learning_rate=0.1, nesterov=True)
#optimizer = keras.optimizers.Aadam(learning_rate=0.05)
from makedataset import dataset
import pandas as pd
import numpy as np
from collections import namedtuple
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor
import torch
import numpy
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import metrics

train, trainLabels, verLabels, ver = dataset()

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(1, 4)),
    keras.layers.Dense(14, activation="relu"),
    keras.layers.Dense(6, activation='relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dense(3, activation="softmax")
    ])


model.compile(
    optimizer= 'adam', 
        loss="categorical_crossentropy", 
        metrics=["accuracy"]
)

model.fit(train, trainLabels, batch_size = 2048, epochs = 100, validation_data = (ver, verLabels))
