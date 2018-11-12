##### 標準

##### 作ったやつ
# import DataProcessing.CovertTyphoonInfo as SModel
import EuclidModel.Model as SModel
#import SimpleModel.ModelMain as SModel
"""
import DataProcessing.ReadJSON
import DataProcessing.functions
import DataProcessing.ConvertGRIB2
"""

def main():
    model = SModel.ModelMain('./SampleData/Z__C_RJTD_20180902000000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin', [22.7, 135.8])
    model.processing()
    model.plotGraph()

main()