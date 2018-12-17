import numpy as np
import json
import math
from General.Constant import Const

class ModelMain(object):
    def __init__(self, realPosition, predictionFile, predictTime):
        self.real = realPosition
        fp = open(predictionFile, 'r')
        self.prediction = json.load(fp)
        fp.close()
        self.time = predictTime

    def predictionUpdate(self):
        predict_pos = [self.prediction[str(self.time) + 'h']['latitude'], self.prediction[str(self.time) + 'h']['longitude']]

        errors = [self.__GlobalDistance__(predict_pos, self.real), self.__AngularDifference__(predict_pos, self.real)]
        update_pos = self.__updatePostion__(errors, predict_pos)
        return update_pos

    # 通常の更新（predictionUpdate）に加え、6-12hの移動量予測を実況にあてはめ（平行移動）させたものを平均化
    def predictionUpdate_2(self):
        up_pos = self.predictionUpdate()

        try:
            predict_now_pos = np.array([self.prediction[str(self.time) + 'h']['latitude'], self.prediction[str(self.time) + 'h']['longitude']])
            predict_next_pos = np.array([self.prediction[str(self.time + 6) + 'h']['latitude'], self.prediction[str(self.time + 6) + 'h']['longitude']])

            movement = predict_next_pos - predict_now_pos
            up2_pos = np.array(self.real) + movement
            
            return (up_pos + up2_pos) / 2.0

        except:
            print('No key... Please predict next time by initModel')
            return

    def getPrediction(self, time):
        return [self.prediction[str(time) + 'h']['latitude'], self.prediction[str(time) + 'h']['longitude']]

    def getPredictPosition():
        return self.predictionUpdate()

    def __updatePostion__(self, errors, predict):
        lat_error = (errors[0] * math.sin(errors[1]) * Const.LatDistError6_12h) / 110.94297

        long_1deg_distance = math.cos(math.radians(predict[0])) * 2 * math.pi * 6378.137 / 360
        long_error = (errors[0] * math.cos(errors[1]) * Const.LongDistError6_12h) / long_1deg_distance

        return [predict[0] + lat_error, predict[1] + long_error]
    


    # 2点間の距離の算出 - OK
    def __GlobalDistance__(self, pos1, pos2):
        R = 6378.1370
        
        lat1 = math.radians(pos1[0])
        long1 = math.radians(pos1[1])
        lat2 = math.radians(pos2[0])
        long2 = math.radians(pos2[1])

        averageLat = (lat1 - lat2) / 2
        averageLong = (long1 - long2) / 2

        return R * 2 * math.asin( math.sqrt(math.pow( math.sin(averageLat), 2) + math.cos(lat1) * math.cos(lat2) * math.pow( math.sin(averageLong), 2)))

    # 角度の算出 - OK
    def __AngularDifference__(self, predict, real):
        Y = real[0] - predict[0]
        X = real[1] - predict[1]
        if X == 0.0:
            return np.pi / 2 if Y > 0 else - np.pi / 2
        return np.arctan2(Y, X)