##### 標準

##### 作ったやつ
# import DataProcessing.CovertTyphoonInfo as ti
import SimpleModel.ModelMain as SModel
"""
import DataProcessing.ReadJSON
import DataProcessing.functions
import DataProcessing.ConvertGRIB2
"""

def main():
    model = SModel.ModelMain('file', [27, 140])
    model.processing()
    model.plotGraph()

main()