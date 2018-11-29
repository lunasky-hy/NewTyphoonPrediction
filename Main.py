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
"""
import DataProcessing.ReadJSON
import DataProcessing.functions
import DataProcessing.ConvertGRIB2
"""

def download(yy, mm, dd, hh):
    mm_str = mm if len(mm) != 1 else '0' + mm
    dd_str = dd if len(dd) != 1 else '0' + dd
    time = str(hh) if len(str(hh)) == 2 else '0' + str(hh)
    url = "http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/"

    #dates = str(yy) + '/' + mm_str + '/' + dd_str
    #dates_nonsplitter = str(yy) + mm_str + dd_str

    dates = yy + '/' + mm_str + '/' + dd_str
    dates_nonsplitter = yy + mm_str + dd_str

    print(dates + '/Z__C_RJTD_' + dates_nonsplitter + time +'0000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin')
    fname = 'SampleData/TempData.bin'
    try:
        urllib.request.urlretrieve(url + dates + '/Z__C_RJTD_' + dates_nonsplitter + time +'0000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin', filename = fname)
    except:
        print('ERROR!! -' + fname)
        with open('./GPV/error_log.txt', mode = 'a') as f:
            f.write('\n' + fname)

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

        download(str(data['year']), str(data['month']), str(data['day']), str(data['hour']))
        model0 = Model.ModelMain('SampleData/TempData.bin', [data['latitude'], data['longitude']])
        model0.processing()
        position = model0.getPredictPosition()
        if not (22.4 < float(position[0]) and float(position[0]) < 47.6 and 120 < float(position[1]) and float(position[1]) < 150):
            continue
        model6 = Model.ModelMain('SampleData/TempData.bin', position, init_time = 6)
        model6.processing()

        flag = 0
        real06 = []
        real12 = []
        typhoons = np.loadtxt('typhoon/table' + str(data['year']) + '.csv', dtype = str, delimiter = ",", skiprows = 1)
        for row in typhoons:
            if row[4] != data['number']:
                continue
            if flag == 2:
                real12.append(float(row[7]))
                real12.append(float(row[8]))
                skips = np.random.randint(10, 50)
                flag = 0
            if flag == 1:
                real06.append(float(row[7]))
                real06.append(float(row[8]))
                flag = 2
            if int(row[1]) == data['month'] and int(row[2]) == data['day'] and int(row[3]) == data['hour']:
                flag = 1
                print(row)

        if len(real06) != 2 or len(real12) != 2:
            continue

        rows = []
        # 0h
        rows.append(data['latitude'])
        rows.append(data['longitude'])
        # 6h
        predict = model0.getPredictPosition()
        rows.append(predict[0])
        rows.append(predict[1])
        rows.append(model0.GlobalDistance(predict, real06))
        rows.append(model0.AngularDifference(predict, real06))
        # 12h
        predict2 = model6.getPredictPosition()
        rows.append(predict2[0])
        rows.append(predict2[1])
        rows.append(model6.GlobalDistance(predict2, real12))
        rows.append(model6.AngularDifference(predict2, real12))

        analysis_data.append(rows)
        del(model0)
        del(model6)

    """
    for index, data in jsondata.items():
        if index == "comment":
            continue
        if skips > 0:
            skips -= 1
            continue

        model0 = AModel.AnalysisPredictErrorModel([data['latitude'], data['longitude']])
        model0.processing()
        position = model0.getPredictPosition()
        if not (22.4 < float(position[0]) and float(position[0]) < 47.6 and 120 < float(position[1]) and float(position[1]) < 150):
            continue
        model6 = AModel.AnalysisPredictErrorModel(model0.getPredictPosition(), init_time = 6)
        model6.processing()

        flag = 0
        real06 = []
        real12 = []
        typhoons = np.loadtxt('typhoon/table' + str(data['year']) + '.csv', dtype = str, delimiter = ",", skiprows = 1)
        for row in typhoons:
            if row[4] != data['number']:
                continue
            if flag == 2:
                real12.append(float(row[7]))
                real12.append(float(row[8]))
                skips = np.random.randint(10, 50)
                flag = 0
            if flag == 1:
                real06.append(float(row[7]))
                real06.append(float(row[8]))
                flag = 2
            if int(row[1]) == data['month'] and int(row[2]) == data['day'] and int(row[3]) == data['hour']:
                flag = 1
                print(row)

        if len(real06) != 2 or len(real12) != 2:
            continue

        rows = []
        # 0h
        rows.append(data['latitude'])
        rows.append(data['longitude'])
        # 6h
        predict = model0.getPredictPosition()
        rows.append(predict[0])
        rows.append(predict[1])
        rows.append(model0.GlobalDistance(predict, real06))
        rows.append(model0.AngularDifference(predict, real06))
        # 12h
        predict2 = model6.getPredictPosition()
        rows.append(predict2[0])
        rows.append(predict2[1])
        rows.append(model6.GlobalDistance(predict2, real12))
        rows.append(model6.AngularDifference(predict2, real12))

        analysis_data.append(rows)
        del(model0)
        del(model6)

    """
    
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    for row in analysis_data:
        x1.append(row[4])
        y1.append(row[8])
        x2.append(np.rad2deg(row[5]))
        y2.append(np.rad2deg(row[9]))

    fig, (plt1, plt2) = plt.subplots(ncols=2)
    plt1.scatter(x1, y1)
    plt1.set_title('6hour Distance Error - 12hour Distance Error')
    plt1.set_xlabel('6hour Distance Error [km]')
    plt1.set_ylabel('12hour Distance Error [km]')
    plt2.scatter(x2, y2)
    plt2.set_title('6hour Angular Error - 12hour Angular Error')
    plt2.set_xlabel('6hour Angular Error [Deg]')
    plt2.set_ylabel('12hour Angular Error [Deg]')
    plt2.set_xlim(-180, 180)
    plt2.set_ylim(-180, 180)

    plt.show()
    print(len(analysis_data))
    np.savetxt('typhoon/out.csv', np.array(analysis_data), delimiter=",")

main()