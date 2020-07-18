from makedataset import dataset
import pandas as pd
import numpy as np
from collections import namedtuple
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor
import torch
import numpy

train, trainLabels, verLabels, ver = dataset()

print(trainLabels.head)
print(train.head)
print(ver.head)
print(verLabels.head)

DISCOVERY_DOY = trainLabels['CONT_DOY']
print(DISCOVERY_DOY)

print(trainLabels.shape)
print(train.shape)
print(verLabels.shape)
print(ver.shape)