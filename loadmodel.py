import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import metrics
from makedataset import dataset

#def loadmodel(modelver):
#   new_model = keras.models.load_model('saves/saved_model' + str('modelver'))

train, trainLabels, verLabels, ver = dataset()

new_model = keras.models.load_model('saves/saved_model')

print(new_model.evaluate(ver, verLabels, batch_size = 2048))