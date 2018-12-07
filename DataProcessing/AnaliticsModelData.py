import csv
import numpy as np


def main():
    
    data = np.loadtxt('SampleData\Graphs\ModelData.csv', dtype = float, delimiter = ",", skiprows = 0)
    x = []
    y = []
    for row in data:
        x.append(row[6])
        y.append(row[13])

    res1 = np.polyfit(x, y, 1)
    res2 = np.polyfit(x, y, 2)
    print(res1)
    print(res2)

main()