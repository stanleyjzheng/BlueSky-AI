import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import metrics
from makedataset import dataset
import pandas as pd
import numpy as np
import datetime

def toint(date, STAT_CAUSE_DISC, LATITUDE, LONGITUDE):
    fmt = '%Y.%m.%d'
    s = '1111.'+'date'#Date should be mm.dd. We could also do mm/dd
    dt = datetime.datetime.strptime(s, fmt)
    tt = dt.timetuple()
    tt = tt.tm_yday
    if lower(STAT_CAUSE_DISC)=='lightning':
        STAT_CAUSE_CODE = 1
    if lower(STAT_CAUSE_DISC)=='equipment use':
        STAT_CAUSE_CODE = 2
    if lower(STAT_CAUSE_DISC)=='smoking':
        STAT_CAUSE_CODE = 3
    if lower(STAT_CAUSE_DISC)=='campfire':
        STAT_CAUSE_CODE = 4
    if lower(STAT_CAUSE_DISC)=='debris burning':
        STAT_CAUSE_CODE = 5
    if lower(STAT_CAUSE_DISC)=='railroad':
        STAT_CAUSE_CODE = 6
    if lower(STAT_CAUSE_DISC)=='arson':
        STAT_CAUSE_CODE = 7
    if lower(STAT_CAUSE_DISC)=='children':
        STAT_CAUSE_CODE = 8
    if lower(STAT_CAUSE_DISC)=='misc/other':
        STAT_CAUSE_CODE = 9
    if lower(STAT_CAUSE_DISC)=='fireworks':
        STAT_CAUSE_CODE = 10
    if lower(STAT_CAUSE_DISC)=='power line':
        STAT_CAUSE_CODE = 11
    if lower(STAT_CAUSE_DISC)=='structure':
        STAT_CAUSE_CODE = 12
    if lower(STAT_CAUSE_DISC)=='missing':
        STAT_CAUSE_CODE = 13

def predictModel(DISCOVERY_DOY, STAT_CAUSE_CODE, LATITUDE, LONGITUDE):
    model = keras.models.load_model('saves/saved_model')
    DISCOVERY_DOY/=366.0
    STAT_CAUSE_CODE/=13.0
    LATITUDE = (abs(LATITUDE)-25)/48
    LONGITUDE = (abs(LONGITUDE)-50)/116
    label = model.predict([[DISCOVERY_DOY, STAT_CAUSE_CODE, LATITUDE, LONGITUDE]])
    np.squeeze(label)
    label = label.tolist()
    contained = int(abs(label[0][0]*366))
    fireSize = int(label[0][1]*606945)
    fireSizeClass = int(label[0][2]*7)
    if contained>DISCOVERY_DOY:
        containDiff=contained-DISCOVERY_DOY
    elif contained<DISCOVERY_DOY:
        containDiff=(contained-DISCOVERY_DOY+365)
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
    if fireSize>fireSizeVerTop:
        fireSizeAvg = (fireSizeVerTop+fireSizeVerBottom)/2
        fireSize = (fireSizeAvg+fireSize)/2
    elif fireSize<fireSizeVerBottom*0.75:
        fireSizeAvg = (fireSizeVerTop+fireSizeVerBottom)/2
        fireSize = (fireSizeAvg+fireSize)/2
    return int(abs(fireSize)), int(abs(containDiff))