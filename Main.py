##### 標準
import numpy as np
import json
import matplotlib.pyplot as plt
import urllib
import os

##### 作ったやつ
# import DataProcessing.CovertTyphoonInfo as Model
import EuclidModel.Model as Model
# import PearsonModel.InitialModel as Model
import General.UpdateModel as UModel
# import SimpleModel.ModelMain as Model

import General.PredictMap as pm

def GlobalDistance(pos1, pos2):
    import math
    R = 6378.1370
        
    lat1 = math.radians(pos1[0])
    long1 = math.radians(pos1[1])
    lat2 = math.radians(pos2[0])
    long2 = math.radians(pos2[1])

    averageLat = (lat1 - lat2) / 2
    averageLong = (long1 - long2) / 2

    return R * 2 * math.asin( math.sqrt(math.pow( math.sin(averageLat), 2) + math.cos(lat1) * math.cos(lat2) * math.pow( math.sin(averageLong), 2)))


def main():
    model0 = Model.ModelMain('SampleData/Z__C_RJTD_20180902000000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin', [22.7, 135.8])
    model0.processing()
    position = model0.getPredictPosition()

    if not (22.4 < float(position[0]) and float(position[0]) < 47.6 and 120 < float(position[1]) and float(position[1]) < 150):
        exit()
    model6 = Model.ModelMain('SampleData/Z__C_RJTD_20180902000000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin', position, init_time = 6)
    model6.processing()
    
    position = model6.getPredictPosition()
    if not (22.4 < float(position[0]) and float(position[0]) < 47.6 and 120 < float(position[1]) and float(position[1]) < 150):
        exit()
    #model12 = Model.ModelMain('SampleData/Z__C_RJTD_20180902000000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin', position, init_time = 12)
    #model12.processing()
    Map = pm.PredictMap([22.7, 135.8], [model0, model6])
    # Map = pm.PredictMap([22.7, 135.8], [model0])
    Map.show()
    Map.save('SampleData/Predict')

    m = UModel.ModelMain([23.7 , 135.0], 'SampleData/Predict.json', 6)
    print(m.predictionUpdate())
    print(m.predictionUpdate_2())
    print(m.getPrediction(12))
    print('real:[24.5 , 134.4]')
    print(GlobalDistance(m.predictionUpdate(), [24.5 , 134.4]))
    print(GlobalDistance(m.predictionUpdate_2(), [24.5 , 134.4]))
    print(GlobalDistance(m.getPrediction(12), [24.5 , 134.4]))
    Map = pm.PredictMap([23.7 , 135.0], [m])
    Map.showOriginals([[23.7 , 135.0], [24.5 , 134.4], m.getPrediction(6), m.predictionUpdate(), m.getPrediction(12)], ['black', 'gray', 'Green', 'Red', 'Blue'])


#main()
#import DataProcessing.AnaliticsModelData

import DataProcessing.ModelErrorAnalizing