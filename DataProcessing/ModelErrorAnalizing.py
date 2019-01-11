##### 標準
import numpy as np
import json
import matplotlib.pyplot as plt
import urllib
import os
import time

##### 作ったやつ
import PearsonModel.InitialModel as PModel
import EuclidModel.Model as EModel
import General.UpdateModel as UModel
import General.PredictMap as pm

def download(yy, mm, dd, hh, filename):
    mm_str = mm if len(mm) != 1 else '0' + mm
    dd_str = dd if len(dd) != 1 else '0' + dd
    time = str(hh) if len(str(hh)) == 2 else '0' + str(hh)
    url = "http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/"


    dates = yy + '/' + mm_str + '/' + dd_str
    dates_nonsplitter = yy + mm_str + dd_str

    print(dates + '/Z__C_RJTD_' + dates_nonsplitter + time +'0000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin')
    fname = filename
    try:
        urllib.request.urlretrieve(url + dates + '/Z__C_RJTD_' + dates_nonsplitter + time +'0000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin', filename = fname)
    except:
        print('ERROR!! -' + fname)
        with open('./GPV/error_log.txt', mode = 'a') as f:
            f.write('\n' + fname)

def main():
    
    fp = open('./typhoon/TyphoonInfo.json', 'r')
    jsondata = json.load(fp)
    fp.close()
    #skips = np.random.randint(5, 50)
    skips = 5
    
    start = time.time()
    check = time.time()

    analysis_data = []
    analysis_data2 = []
    for index, data in jsondata.items():
        if index == "comment":
            continue
        if skips > 0:
            skips -= 1
            continue


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
                skips = 5
                break
            if flag == 1:
                real06.append(float(row[7]))
                real06.append(float(row[8]))
                flag = 2
            if int(row[1]) == data['month'] and int(row[2]) == data['day'] and int(row[3]) == data['hour']:
                flag = 1
                print(row)

        # if len(real06) != 2 or len(real12) != 2 or len(real18) != 2:
        if len(real06) != 2 or len(real12) != 2:
            continue

        filename = 'Simulate/' + str(data['year']) + 'M' +str(data['month']) + 'D' + str(data['day']) + 'h' + str(data['hour']) + '.bin'
        # download(str(data['year']), str(data['month']), str(data['day']), str(data['hour']), filename)

        model0 = PModel.ModelMain(filename, [data['latitude'], data['longitude']])
        model0.processing()

        position = model0.getPredictPosition()
        if not (22.4 < float(position[0]) and float(position[0]) < 47.6 and 120 < float(position[1]) and float(position[1]) < 150):
            continue
        model6 = PModel.ModelMain(filename, position, init_time = 6)
        model6.processing()

        position = real06
        if not (22.4 < float(position[0]) and float(position[0]) < 47.6 and 120 < float(position[1]) and float(position[1]) < 150):
            continue
        model_next = PModel.ModelMain(filename, position, init_time = 6)
        model_next.processing()

        ######################## Pearson's Calc
        rows = []
        # 0h
        rows.append(data['latitude'])   # 0 A
        rows.append(data['longitude'])   # 1 B

        # 6h
        predict = model0.getPredictPosition()
        rows.append(predict[0])   # 2 C
        rows.append(predict[1])   # 3 D
        rows.append(real06[0])   # 4 E
        rows.append(real06[1])   # 5 F
        rows.append(model0.GlobalDistance(predict, real06))   # 6 G
        rows.append(model0.AngularDifference(predict, real06))   # 7 H
        rows.append(model0.getSampleDataNum())   # 8 I

        # 12h
        predict2 = model6.getPredictPosition()
        rows.append(predict2[0])   # 9 J
        rows.append(predict2[1])   # 10 K
        rows.append(real12[0])   # 11 L
        rows.append(real12[1])   # 12 M
        rows.append(model6.GlobalDistance(predict2, real12))   # 13 N
        rows.append(model6.AngularDifference(predict2, real12))   # 14 O
        rows.append(model6.getSampleDataNum())   # 15 P

        # 6h Later Model
        predict_next = model_next.getPredictPosition()
        rows.append(predict_next[0])   # 16 Q
        rows.append(predict_next[1])   # 17 R
        rows.append(real12[0])   # 18 S
        rows.append(real12[1])   # 19 T
        rows.append(model_next.GlobalDistance(predict_next, real12))   # 20 U
        rows.append(model_next.AngularDifference(predict_next, real12))   # 21 V
        rows.append(model_next.getSampleDataNum())   # 22 W

        # Update
        Map = pm.PredictMap([data['latitude'], data['longitude']], [model0, model6])
        Map.save('SampleData/Predict_sub')

        m = UModel.ModelMain(real06, 'SampleData/Predict_sub.json', 6)
        predictUp = m.predictionUpdate()
        rows.append(predictUp[0])   # 23 X
        rows.append(predictUp[1])   # 24 Y
        rows.append(model0.GlobalDistance(predictUp, real12))   # 25 Z
        rows.append(model0.AngularDifference(predictUp, real12))   # 26 AA

        predictUp2 = m.predictionUpdate_2()
        rows.append(predictUp2[0])   # 27 AB
        rows.append(predictUp2[1])   # 28 AC
        rows.append(model0.GlobalDistance(predictUp2, real12))   # 29 AD
        rows.append(model0.AngularDifference(predictUp2, real12))   # 30 AE


        analysis_data.append(rows)
        """
        ######################## Euclid's Calc
        rows2 = []
        rows2.append(data['latitude'])   # 0
        rows2.append(data['longitude'])   # 1

        # 6h
        predict = xmodel0.getPredictPosition()
        rows2.append(predict[0])   # 2
        rows2.append(predict[1])   # 3
        rows2.append(real06[0])   # 4
        rows2.append(real06[1])   # 5
        rows2.append(xmodel0.GlobalDistance(predict, real06))   # 6
        rows2.append(xmodel0.AngularDifference(predict, real06))   # 7
        rows2.append(xmodel0.getSampleDataNum())   # 8

        # 12h
        predict2 = xmodel6.getPredictPosition()
        rows2.append(predict2[0])   # 9
        rows2.append(predict2[1])   # 10
        rows2.append(real12[0])   # 11
        rows2.append(real12[1])   # 12
        rows2.append(xmodel6.GlobalDistance(predict2, real12))   # 13
        rows2.append(xmodel6.AngularDifference(predict2, real12))   # 14
        rows2.append(xmodel6.getSampleDataNum())   # 15
        
        # 18h
        predict3 = xmodel12.getPredictPosition()
        rows2.append(predict3[0])   # 16
        rows2.append(predict3[1])   # 17
        rows2.append(real18[0])   # 18
        rows2.append(real18[1])   # 19
        rows2.append(xmodel12.GlobalDistance(predict3, real18))   # 20
        rows2.append(xmodel12.AngularDifference(predict3, real18))   # 21
        rows2.append(xmodel12.getSampleDataNum())   # 22

        # Update
        Map = pm.PredictMap([data['latitude'], data['longitude']], [xmodel0, xmodel6, xmodel12])
        Map.save('SampleData/Predict')
        m = UModel.ModelMain(real06, 'SampleData/Predict.json', 6)
        predictUp = m.predictionUpdate()
        rows2.append(predictUp[0])   # 23
        rows2.append(predictUp[1])   # 24
        rows2.append(xmodel0.GlobalDistance(predictUp, real12))   # 25
        
        analysis_data2.append(rows2)
        """
        del(model0)
        del(model6)
        del(m)
        
        print('Num: ' + str((2070 - int(index) - 1) / 5))
        print('Remaining... ' + str((time.time() - check) * (2070 - int(index) - 1) / 5))
        check = time.time()

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
    
    print(len(analysis_data))
    np.savetxt('typhoon/outPearson_re.csv', np.array(analysis_data), delimiter=",")
    """
    x1 = []
    y1 = []
    x2 = []
    y2 = []

    # 6h - 12h Error
    for row in analysis_data:
        x1.append(row[6])
        y1.append(row[13])
        x2.append(np.rad2deg(row[7]))
        y2.append(np.rad2deg(row[14]))

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
    
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    # 6h - 18h Error
    for row in analysis_data:
        x1.append(row[6])
        y1.append(row[20])
        x2.append(row[7])
        y2.append(row[21])

    fig, (plt1, plt2) = plt.subplots(ncols=2)
    plt1.scatter(x1, y1)
    plt1.set_title('6hour Distance Error - 18hour Distance Error')
    plt1.set_xlabel('6hour Distance Error [km]')
    plt1.set_ylabel('18hour Distance Error [km]')
    plt2.scatter(x2, y2)
    plt2.set_title('6hour Angular Error - 18hour Angular Error')
    plt2.set_xlabel('6hour Angular Error [Deg]')
    plt2.set_ylabel('18hour Angular Error [Deg]')
    plt2.set_xlim(-180, 180)
    plt2.set_ylim(-180, 180)
    
    plt.show()
    """

def main2():

    analysis_data = []
    data = np.loadtxt('typhoon/table2018.csv', dtype = str, delimiter = ",", skiprows = 1)

    n = 0
    
    for index, row in enumerate(data):
        if index + 2 >= len(data):
            break

        if not (22.4 < float(row[7]) and float(row[7]) < 47.6 and 120 < float(row[8]) and float(row[8]) < 150):
            continue

        if not (row[4] == data[index + 1][4] and (int(row[3]) + 6) % 24 == int(data[index + 1][3])):
            continue
        
        if not (row[4] == data[index + 2][4] and (int(row[3]) + 12) % 24 == int(data[index + 2][3])):
            continue

        n += 1

    print(n)


    for index, row in enumerate(data):
        if index + 2 >= len(data):
            break

        if not (22.4 < float(row[7]) and float(row[7]) < 47.6 and 120 < float(row[8]) and float(row[8]) < 150):
            continue

        if not (row[4] == data[index + 1][4] and (int(row[3]) + 6) % 24 == int(data[index + 1][3])):
            continue
        
        if not (row[4] == data[index + 2][4] and (int(row[3]) + 12) % 24 == int(data[index + 2][3])):
            continue


        # file download
        filename = 'Simulate/' + row[0] + 'M' + row[1] + 'D' + row[2] + 'h' + row[3] + '.bin'
        #download(row[0], row[1], row[2], row[3], filename)

        # 0h -> 6h predict
        model0 = PModel.ModelMain(filename, [float(row[7]), float(row[8])])
        model0.processing()

        position = model0.getPredictPosition()
        if not (22.4 < float(position[0]) and float(position[0]) < 47.6 and 120 < float(position[1]) and float(position[1]) < 150):
            continue

        # 6h -> 12h predict
        model6 = PModel.ModelMain(filename, position, init_time = 6)
        model6.processing()
        
        real06 = [float(data[index + 1][7]), float(data[index + 1][8])]
        real12 = [float(data[index + 2][7]), float(data[index + 2][8])]
        rows = []

        # 0h
        rows.append(float(row[7]))   # 0 A
        rows.append(float(row[8]))   # 1 B

        # 6h
        predict = model0.getPredictPosition()
        rows.append(predict[0])   # 2 C
        rows.append(predict[1])   # 3 D
        rows.append(real06[0])   # 4 E
        rows.append(real06[1])   # 5 F
        rows.append(model0.GlobalDistance(predict, real06))   # 6 G
        rows.append(model0.AngularDifference(predict, real06))   # 7 H
        rows.append(model0.getSampleDataNum())   # 8 I

        # 12h
        predict2 = model6.getPredictPosition()
        rows.append(predict2[0])   # 9 J
        rows.append(predict2[1])   # 10 K
        rows.append(real12[0])   # 11 L
        rows.append(real12[1])   # 12 M
        rows.append(model6.GlobalDistance(predict2, real12))   # 13 N
        rows.append(model6.AngularDifference(predict2, real12))   # 14 O
        rows.append(model6.getSampleDataNum())   # 15 P

        # Update
        Map = pm.PredictMap([float(row[7]), float(row[8])], [model0, model6])
        Map.save('SampleData/Predict')

        m = UModel.ModelMain([float(data[index + 1][7]), float(data[index + 1][8])], 'SampleData/Predict.json', 6)
        predictUp = m.predictionUpdate()
        rows.append(predictUp[0])   # 16 Q
        rows.append(predictUp[1])   # 17 R
        rows.append(model0.GlobalDistance(predictUp, real12))   # 18 S
        rows.append(model0.AngularDifference(predictUp, real12))   # 19 T

        predictUp2 = m.predictionUpdate_2()
        rows.append(predictUp2[0])   # 20 U
        rows.append(predictUp2[1])   # 21 V
        rows.append(model0.GlobalDistance(predictUp2, real12))   # 22 W
        rows.append(model0.AngularDifference(predictUp2, real12))   # 23 X

        rows.append(index)
        
        analysis_data.append(rows)
        del(model0)
        del(model6)
        del(m)

    print(len(analysis_data))
    np.savetxt('typhoon/out2018_re.csv', np.array(analysis_data), delimiter=",")

main()
#main2()