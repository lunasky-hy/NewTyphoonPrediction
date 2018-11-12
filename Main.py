##### 標準

##### 作ったやつ
# import DataProcessing.CovertTyphoonInfo as Model
# import EuclidModel.Model as Model
import PearsonModel.Model as Model
# import SimpleModel.ModelMain as Model
"""
import DataProcessing.ReadJSON
import DataProcessing.functions
import DataProcessing.ConvertGRIB2
"""

def main():
    model = Model.ModelMain('./SampleData/Z__C_RJTD_20180902000000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin', [22.7, 135.8])
    model.processing()
    model.plotGraph()

main()