from __future__ import print_function
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import metrics
import numpy as np
import datetime
from flask import Flask, jsonify, request, Response, make_response

app = Flask(__name__)

@app.route('/test', methods=['POST', 'GET'])
def test():
    if request.method == 'POST':
        print('post app')
        req = request.json
        date = req['date']
        DISCOVERY_DOY, STAT_CAUSE_CODE = toint('09.11', str(req['stat']))
        acreage, contDate = predictModel(float(DISCOVERY_DOY), STAT_CAUSE_CODE, float(req['latitude']), float(req['longitude']))
        #DISCOVERY_DOY, STAT_CAUSE_CODE = toint('09.11', 'Children')
        #acreage, contDate = predictModel(DISCOVERY_DOY, STAT_CAUSE_CODE, 40.656564, -113.675837)
        #return jsonify({"acreage":acreage, "contDate": contDate})
    #return jsonify(something = str(DISCOVERY_DOY), somethingelse = str(STAT_CAUSE_CODE))
    return jsonify(acreage=acreage, contDate=contDate)

#@app.route('/model', methods=['POST', 'GET'])
def main():
    req = request.get_json(force=True)    
    date = request["date"]
    #STAT_CAUSE_DISC = request["stat"]
    #LATITUDE = request["latitude"]
    #LONGITUDE = request["long"]
    # print(req+'this is to see if print works')
    # date = req.date
    # STAT_CAUSE_DISC = req.stat
    # LATITUDE = req.latitude
    # LONGITUDE = req.long
    #DISCOVERY_DOY, STAT_CAUSE_CODE = toint(date, STAT_CAUSE_DISC)
    #acreage, contDate = predictModel(DISCOVERY_DOY, STAT_CAUSE_CODE, LATITUDE, LONGITUDE)
    out = make_response(jsonify({'acreage': 10, 'contDate': '5/6'}), 200)
    return (out)

def toint(date, STAT_CAUSE_DISC):
    fmt = '%Y.%m.%d'
    s = '1111.'+str(date)#Date should be mm.dd. We could also do mm/dd
    dt = datetime.datetime.strptime(s, fmt)
    tt = dt.timetuple()
    tt = tt.tm_yday
    tt = float(tt)
    if STAT_CAUSE_DISC.lower()=='lightning':
        STAT_CAUSE_CODE = 1
    if STAT_CAUSE_DISC.lower()=='equipment use':
        STAT_CAUSE_CODE = 2
    elif STAT_CAUSE_DISC.lower()=='smoking':
        STAT_CAUSE_CODE = 3
    elif STAT_CAUSE_DISC.lower()=='campfire':
        STAT_CAUSE_CODE = 4
    elif STAT_CAUSE_DISC.lower()=='debris burning':
        STAT_CAUSE_CODE = 5
    elif STAT_CAUSE_DISC.lower()=='railroad':
        STAT_CAUSE_CODE = 6
    elif STAT_CAUSE_DISC.lower()=='arson':
        STAT_CAUSE_CODE = 7
    elif STAT_CAUSE_DISC.lower()=='children':
        STAT_CAUSE_CODE = 8
    elif STAT_CAUSE_DISC.lower()=='misc/other':
        STAT_CAUSE_CODE = 9
    elif STAT_CAUSE_DISC.lower()=='fireworks':
        STAT_CAUSE_CODE = 10
    elif STAT_CAUSE_DISC.lower()=='power line':
        STAT_CAUSE_CODE = 11
    elif STAT_CAUSE_DISC.lower()=='structure':
        STAT_CAUSE_CODE = 12
    elif STAT_CAUSE_DISC.lower()=='missing':
        STAT_CAUSE_CODE = 13
    return tt, STAT_CAUSE_CODE

def predictModel(DISCOVERY_DOY, STAT_CAUSE_CODE, LATITUDE, LONGITUDE):
    LATITUDE = float(LATITUDE)
    LONGITUDE = float(LONGITUDE)
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
    regularday = datetime.datetime.strptime('2005 '+ str(int(containDiff)), '%Y %j')
    regularday = regularday.strftime('%Y/%m/%d')
    regularday = str(regularday)[5:10]
    return int(abs(fireSize)), regularday