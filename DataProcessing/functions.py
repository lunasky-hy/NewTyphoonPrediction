import numpy as np

# 2D配列から7ｘ7フィルタの値を2Ｄ配列で返す
def GaussianFilter(Data2D):
    FilterSize = 7
    FilterCenter = int(FilterSize / 2)

    row_num = len(Data2D)
    colum_num = len(Data2D[0])

    FilteringValue = np.zeros([int(row_num / FilterSize), int(colum_num / FilterSize)])
    for row in range(int(row_num / FilterSize)):
        for colum in range(int(colum_num / FilterSize)):
            Array2d = Data2D[row * FilterSize : (row + 1) * FilterSize, colum * FilterSize : (colum + 1) * FilterSize]
            #print(Array2d)
            FilteringValue[row, colum] = Gauss(Array2d, FilterSize)

    return FilteringValue


# ガウシアン演算で配列の中心点の値を求める
def Gauss(Array2d, size):
    center = int(size / 2)
    sigma = 0.75

    value = 0
    total_cof = 0
    for row in range(size):
        for colum in range(size):
            dval = Array2d[row, colum]
            distance = pow(row - center, 2) + pow(colum - center, 2)
            coefficient = 1 / (np.pi * pow(sigma, 2)) * np.exp(- distance / (2 * pow(sigma, 2)))
            value += dval * coefficient
            total_cof += coefficient
    return value / total_cof

# 格子間隔でのフィルタ（未完成）
def GridFilter(Array2d, interval):
    row_itvl = interval / 0.125
    colum_itvl = interval / 0.1

    row_num = len(Data2D)
    colum_num = len(Data2D[0])

    FilteringValue = np.zeros([int(row_num / FilterSize), int(colum_num / FilterSize)])
    for row in range(int(row_num / FilterSize)):
        for colum in range(int(colum_num / FilterSize)):
            Array2d = Data2D[row * FilterSize : (row + 1) * FilterSize, colum * FilterSize : (colum + 1) * FilterSize]
            print(Array2d)
            FilteringValue[row, colum] = Gauss(Array2d, FilterSize)

    return FilteringValue
