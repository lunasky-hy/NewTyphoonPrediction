import numpy as np
import json
import collections as cl



def formatGPVfilename(day, time):
    time = time if len(time) != 1 else '0' + time
    return day + 'MSM' + time + '.json'


def convert():
    jsondict = cl.OrderedDict()
    jsondict['comment'] = 'movement: [latitude move, longitude move]'
    sampleNum = 1
    typhoons = []
    for n in range(2006, 2018):

        typhoonNumber = 0
        info_dict = None

        data = np.loadtxt('typhoon/table' + str(n) + '.csv', dtype = str, delimiter = ",", skiprows = 1)

        # 各行ごとに読み込み
        for row in data:
            if not (row[3] in ['0', '6', '12', '18']):
                continue

            # 変数に台風データが入っている場合
            if typhoonNumber != 0:
                if typhoonNumber == int(row[4]) and (float(row[3]) - float(info_dict['hour']) == 6 or (float(info_dict['hour']) - float(row[3]) == 18 and float(row[2]) == float(info_dict['day']) + 1)):
                    move = [float(row[7]) - float(info_dict['latitude']), float(row[8]) - float(info_dict['longitude'])]
                    info_dict['movement'] = move

                    jsondict[str(sampleNum)] = info_dict
                    sampleNum += 1

                typhoonNumber = 0
                info_dict = None

            # 台風が範囲内にあるならdictに保存
            if (22.4 < float(row[7]) and float(row[7]) < 47.6 and 120 < float(row[8]) and float(row[8]) < 150):
                info_dict = cl.OrderedDict()
                info_dict['number'] = row[4]
                info_dict['year'] = n
                info_dict['month'] = int(row[1])
                info_dict['day'] = int(row[2])
                info_dict['hour'] = int(row[3])
                info_dict['latitude'] = float(row[7])
                info_dict['longitude'] = float(row[8])
                info_dict['pressure'] = int(row[9])
                info_dict['radius'] = float(row[15])
                info_dict['GPVfile'] = './GPV/' + str(n) + '/' + row[1] + '/' + formatGPVfilename(row[2], row[3])
                typhoonNumber = int(row[4])

            if not row[4] in typhoons:
                typhoons.append(row[4])
    
    fw = open('./typhoon/TyphoonInfo.json', 'w')
    json.dump(jsondict, fw, indent = 4)
    del(jsondict)
    fw.close()
    print(sampleNum)
    print(typhoons)
    print(len(typhoons))