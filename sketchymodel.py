from makedataset import dataset
import tensorflow as tf
from tensorflow import keras

train, trainLabels, verLabels, ver = dataset()

#maxFireSize=trainLabels['FIRE_SIZE']

print(ver.head)
#(20, -50) becomes (0, 0)
#(75, -170) becomes (55, 120)
print(max(ver))
# print(max(ver.iloc[:, 0]))
# print(max(ver.iloc[:, 1]))
print(max(ver.iloc[:, 2]))
print(max(ver.iloc[:, 3]))
print(min(ver.iloc[:, 2]))
print(min(ver.iloc[:, 3]))