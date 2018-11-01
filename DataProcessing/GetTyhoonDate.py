import numpy as np
import urllib
from time import sleep
import GRIB2
import time
import os


def main():
    typhoons = searchTyphoonDate()

    start = time.time()
    check = time.time()

    # 台風の日のデータ
    for colum in typhoons:
        date = colum.split("/")
        index = typhoons.index(colum)
        print('now : ' + str(index + 1) + " / " + str(len(typhoons)))
        print('--->' + colum)
        download(date[0], date[1], date[2])
        print('total file size : ' + str(getDirectorySize('./GPV') / 1024.0 / 1024.0) + ' MB')
        print('Remaining... ' + str((time.time() - check) * (len(typhoons) - index - 1)))
        check = time.time()
        sleep(2)


    # ダウンロードが終了したことを示す出力を追加
    # データがうまくダウンロードできなかった際の例外処理を追加

def searchTyphoonDate():
    typhoonDate = []
    for n in range(2008, 2018):
        # 月ごと31日ごとの2次元配列
        dates = [[''] * 31 for i in range(12)]
        
        # csvを読み込み、配列の合うところに文字を入れる
        data = np.loadtxt('typhoon/table' + str(n) + '.csv', dtype = str, delimiter = ",", skiprows = 1)
        for row in data:
            if (22.4 < float(row[7]) and float(row[7]) < 47.6 and 120 < float(row[8]) and float(row[8]) < 150):
                dates[int(row[1]) - 1][int(row[2]) - 1] = str(n) + '/' + row[1] + '/' + row[2]

        # 配列に入れた日付を取り出し、一覧のリストにする
        for month in dates:
            for day in month:
                if len(day) != 0:
                    #print(day)
                    typhoonDate.append(day)

    print(len(typhoonDate))
    return typhoonDate
    """
    data = np.loadtxt('typhoon/table' + str(n) + '.csv', dtype = str, delimiter = ",", skiprows = 1)
    for row in data:
        dates[int(row[1]) - 1][int(row[2]) - 1] = row[1] + " / " + row[2]

    for row in dates:
        for colum in row:
            if colum != '':
                split = colum.split("/")
    #           download(n, int(split[0]), int(split[1]))
                count += 1
    """

# 日付指定のデータを得る（日付は文字列型）
def download(yy, mm, dd):
    mm_str = mm if len(mm) != 1 else '0' + mm
    dd_str = dd if len(dd) != 1 else '0' + dd
    url = "http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/"

    #dates = str(yy) + '/' + mm_str + '/' + dd_str
    #dates_nonsplitter = str(yy) + mm_str + dd_str

    dates = yy + '/' + mm_str + '/' + dd_str
    dates_nonsplitter = yy + mm_str + dd_str
    for time in ['00', '06', '12', '18']:
        print(dates + '/Z__C_RJTD_' + dates_nonsplitter + time +'0000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin')
        fname = './GPV/' + str(yy) + '/' + str(mm) + '/' + str(dd) + 'MSM' + time + '.bin'
        try:
            urllib.request.urlretrieve(url + dates + '/Z__C_RJTD_' + dates_nonsplitter + time +'0000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin', filename = fname)
            file = GRIB2.GRIB2(fname)
            file.saveJSON()
            file.delete()
        except:
            print('ERROR!! -' + fname)
            with open('./GPV/error_log.txt', mode = 'a') as f:
                f.write('\n' + fname)

        sleep(1)

def getDirectorySize(path):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += getDirectorySize(entry.path)
    return total

main()
#file = GRIB2.GRIB2("./GPV/Z__C_RJTD_20181010000000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin")
#file.saveJSON()
#file.delete()
ReadJSON.read('./GPV/2017/8/4MSM12.json')
#ConvertGRIB2.ConvertGRIB2()


#urllib.request.urlretrieve('http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/2006/02/18/Z__C_RJTD_20060218000000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin', filename = './GPV/data.bin')