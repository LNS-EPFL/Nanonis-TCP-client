import nanonis_esr_tcp as tcp
from os import mkdir
from os.path import exists
# import time
import pickle
import numpy as np
import pandas as pd

my_tcp = tcp.tcp_ctrl()
connect = tcp.nanonis_ctrl(my_tcp)

def check_dirs(dirName):
    # for dirName in dirs:
    if not exists(dirName):
        mkdir(dirName)
        print("Directory ", dirName,  " Created ")

def bias_spectr_par_save(com, fdir, fname = ''):
    bias_par = {'BiasSpectrChs': com.BiasSpectrChsGet(),
                'BiasSpectrProps': com.BiasSpectrPropsGet(),
                'BiasSpectrAdvProps': com.BiasSpectrAdvPropsGet(),
                'BiasSpectrLimits': com.BiasSpectrLimitsGet(),
                'BiasSpectrTiming': com.BiasSpectrTimingGet(),
                'BiasSpectrTTLSync': com.BiasSpectrTTLSyncGet(),
                'BiasSpectrAltZCtrl': com.BiasSpectrAltZCtrlGet(),
                'BiasSpectrMLSLockinPerSeg': com.BiasSpectrMLSLockinPerSegGet(),
                'BiasSpectrMLSMode': com.BiasSpectrMLSModeGet(),
                'BiasSpectrMLSVals': com.BiasSpectrMLSValsGet(),
                'BiasSpectrMore': pd.DataFrame({'Auto save': 'Yes/On', 'Save dialog': 'No/Off', 'Basename' : 'STS_%Y%m%d_'}, index=[0]).T,
                'LockInModAmp1': com.LockInModAmpGet(1),
                'LockInModFreq1': com.LockInModPhasFreqGet(1),
                'LockInOnOff1': com.LockInModOnOffGet(1)
                }
    with open(fdir + '/BiasSpectr' + fname + '.par', 'wb') as handle:
        pickle.dump(bias_par, handle)
    
    print(f'".par" file created in {fdir}')

def bias_spectr_par_load(fdir, fname):
    with open(fdir + '/' + fname, 'rb') as handle:
        bias_par = pickle.load(handle)
    for keys in bias_par:
        bias_par[keys] = bias_par[keys].replace({'No change': 0,
                                                           'Yes/On': 1,
                                                           'No/Off': 2,
                                                           'False/Off': 0,
                                                           'True/On': 1})
    return bias_par

def bias_spectr(com, par, basename = '%Y%m%d_'):
    com.BiasSpectrOpen()
    props = (int(par['BiasSpectrProps'].loc['Save all', 0]),
             int(par['BiasSpectrProps'].loc['Number of sweeps']),
             par['BiasSpectrProps'].loc['Backward sweep', 0],
             int(par['BiasSpectrProps'].loc['Number of points']),
             float(par['BiasSpectrTiming'].loc['Z offset (m)']),
             par['BiasSpectrMore'].loc['Auto save', 0],
             par['BiasSpectrMore'].loc['Save dialog', 0])
    
    com.BiasSpectrChsSet(*par['BiasSpectrChs'].values)
    com.BiasSpectrPropsSet(*props)
    com.BiasSpectrAdvPropsSet(*par['BiasSpectrAdvProps'].values)
    com.BiasSpectrLimitsSet(*par['BiasSpectrLimits'].values)
    com.BiasSpectrTimingSet(*par['BiasSpectrTiming'].values)
    print(*par['BiasSpectrTTLSync'].values)

    com.BiasSpectrTTLSyncSet(*par['BiasSpectrTTLSync'].values)
    com.BiasSpectrAltZCtrlSet(*par['BiasSpectrAltZCtrl'].values)
    com.BiasSpectrMLSLockinPerSegSet(*par['BiasSpectrMLSLockinPerSeg'].values)
    com.BiasSpectrMLSModeSet(*par['BiasSpectrMLSMode'].values)
    com.BiasSpectrMLSValsSet(*par['BiasSpectrMLSVals'].values)

    com.LockInModAmpSet(*par['LockInModAmp1'].values)
    com.LockInModPhasFreqSet(*par['LockInModFreq1'].values)
    com.LockInModOnOffSet(*par['LockInOnOff1'].values)
    sess_path = com.UtilSessionPathGet()
    data, parameters = com.BiasSpectrStart(1, basename)

    return data, parameters

# bias_spectr_par_save(connect, 'C:/Personal_files/Study/Python_scripts/GitHub/Scripts/')
# print('done')
# bias_par = bias_spectr_par_load('C:/Personal_files/Study/Python_scripts/GitHub/Scripts/', 'BiasSpectr.par')
# data, _ = bias_spectr(connect, bias_par)
# sess_path = connect.UtilSessionPathGet().loc['Session path']
# print(sess_path)
sess_path = check_dirs('C:/Personal_files/Study/Python_scripts/test_session/STS')
# connect.UtilSessionPathSet(sess_path + '/STS', 0)
my_tcp.socket_close()