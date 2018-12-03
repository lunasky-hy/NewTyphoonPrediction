##### 標準
import numpy as np
import json
import matplotlib.pyplot as plt
import urllib
import os

##### 作ったやつ
# import DataProcessing.CovertTyphoonInfo as Model
# import EuclidModel.Model as Model
import PearsonModel.Model as Model
# import SimpleModel.ModelMain as Model
import PearsonModel.AnalysisPredictErrorModel as AModel

import General.PredictMap as pm

def main():
    """
    # 6h
    model6 = Model.ModelMain('./SampleData/Z__C_RJTD_20180902000000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin', [22.7, 135.8])
    model6.processing()
    model6.plotGraph()

    # 12h
    model12 = Model.ModelMain('./SampleData/Z__C_RJTD_20180902000000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin', model6.getPredictPosition(), init_time = 6)
    model12.processing()
    model12.plotGraph()
    """
    
    fp = open('./typhoon/TyphoonInfo.json', 'r')
    jsondata = json.load(fp)
    fp.close()
    skips = np.random.randint(5, 50)

    analysis_data = []

    for index, data in jsondata.items():
        if index == "comment":
            continue
        if skips > 0:
            skips -= 1
            continue

    # model0 = Model.ModelMain('SampleData/Z__C_RJTD_20180902000000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin', [22.7, 135.8])
    model0 = AModel.AnalysisPredictErrorModel([22.7, 135.8])
    model0.processing()
    position = model0.getPredictPosition()

    if not (22.4 < float(position[0]) and float(position[0]) < 47.6 and 120 < float(position[1]) and float(position[1]) < 150):
        exit()
    #model6 = Model.ModelMain('SampleData/Z__C_RJTD_20180902000000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin', position, init_time = 6)
    model6 = AModel.AnalysisPredictErrorModel(model0.getPredictPosition(), init_time = 6)
    model6.processing()
    """
    position = model6.getPredictPosition()
    if not (22.4 < float(position[0]) and float(position[0]) < 47.6 and 120 < float(position[1]) and float(position[1]) < 150):
        exit()
    model12 = Model.ModelMain('SampleData/Z__C_RJTD_20180902000000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin', position, init_time = 12)
    model12.processing()
    
    position = model12.getPredictPosition()
    if not (22.4 < float(position[0]) and float(position[0]) < 47.6 and 120 < float(position[1]) and float(position[1]) < 150):
        exit()
    model18 = Model.ModelMain('SampleData/Z__C_RJTD_20180902000000_MSM_GPV_Rjp_L-pall_FH18-33_grib2.bin', position, init_time = 18)
    model18.processing()
    """

    Map = pm.PredictMap([model0, model6])
    Map.show([22.7, 135.8])



# main()
import DataProcessing.ModelErrorAnalizing
