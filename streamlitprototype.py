import streamlit as st
import torch
import numpy as np
from torch import nn
import torch.nn.functional as F

def modelCache():
    model = torch.load('forestfire-ai.pt', map_location='cpu')
    return model

def predict(DISCOVERY_DOY, STAT_CAUSE_CODE, LATITUDE, LONGITUDE):
    model = modelCache()
    model.eval()
    DISCOVERY_DOY/=366.0
    STAT_CAUSE_CODE/=13.0
    LATITUDE = (abs(LATITUDE)-25)/48
    LONGITUDE = (abs(LONGITUDE)-50)/116
    inputTensor = torch.from_numpy(np.asarray([DISCOVERY_DOY, STAT_CAUSE_CODE, LATITUDE, LONGITUDE]))
    inputTensor = inputTensor.type(torch.float).unsqueeze(0)
    label = model(inputTensor)
    print(label.shape)
    label = label.squeeze().tolist()
    contained = int(abs(label[0]*366))
    print(contained)
    fireSize = int(label[1])#*606945)
    fireSizeClass = int(label[2]*7)
    if contained>DISCOVERY_DOY:
        containDiff=contained-DISCOVERY_DOY
    elif contained<DISCOVERY_DOY:
        containDiff=(contained-DISCOVERY_DOY+366)
    if fireSizeClass==1:
        fireSizeVerBottom=0
        fireSizeVerTop=0.25
    elif fireSize==2:
        fireSizeVerBottom=0.26
        fireSizeVerTop=9.99
    elif fireSize==3:
        fireSizeVerBottom=10
        fireSizeVerTop=99.99
    elif fireSize==4:
        fireSizeVerBottom=100
        fireSizeVerTop=299.99
    elif fireSize==5:
        fireSizeVerBottom=300
        fireSizeVerTop=999.99
    elif fireSize==6:
        fireSizeVerBottom=1000
        fireSizeVerTop=4999.99
    elif fireSize==7:
        fireSizeVerBottom=5000
        fireSizeVerTop=500000
    else:
        fireSizeVerTop=5000000000
        fireSizeVerBottom=0.01
        print(fireSizeClass)
    if fireSize>fireSizeVerTop*1.5:
        fireSizeAvg = (fireSizeVerTop+fireSizeVerBottom)/2
        fireSize = (fireSizeAvg+fireSize)/2
    elif fireSize<fireSizeVerBottom*0.75:
        fireSizeAvg = (fireSizeVerTop+fireSizeVerBottom)/2
        fireSize = (fireSizeAvg+fireSize)/2
    return int(abs(fireSize)), int(abs(containDiff))

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.input = nn.Linear(4, 14)
        self.dense1 = nn.Linear(14, 9)
        self.dense2 = nn.Linear(9, 3)
        #self.dense3 = nn.Linear(3, 1)

    def forward(self, x):
        x = self.input(x)
        x = F.relu(x)
        x = self.dense1(x)
        x = F.relu(x)
        x = self.dense2(x)
        #x = self.dense3(x)
        output = F.log_softmax(x, dim=1)
        return output

print(predict(140, 4, 51.086284, -114.138636))