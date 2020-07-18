import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import metrics
from makedataset import dataset
import pandas as pd

#def loadmodel(modelver):
#   new_model = keras.models.load_model('saves/saved_model' + str('modelver'))

train, trainLabels, ver, verLabels = dataset()

model = keras.models.load_model('saves/saved_model')


prediction = model.predict(ver)

print(prediction)



