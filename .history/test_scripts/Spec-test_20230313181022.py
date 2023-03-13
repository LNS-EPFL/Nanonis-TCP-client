from nanonispy.read  import *

file= "\\\\atlas\\lnsharrigroup\\LABS\\He3_STM\\data\\20230131_Ag-100_MgO_He4\\STS_20230131_00001.dat"

mydata=Spec(file)

print(mydata.header['Bias Spectroscopy>Sweep Start (V)'])