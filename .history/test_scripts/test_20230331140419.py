import nanonis_esr_tcp as tcp
import time
import pickle
import numpy as np
import pandas as pd

my_tcp = tcp.tcp_ctrl()
connect = tcp.nanonis_ctrl(my_tcp)

def bias_spectr_par_save(com, fdir, fname):
    BiasParameter = {'BiasSpectrChs': com.BiasSpectrChsGet(),
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
    with open(fdir + 'BiasSpectr' + fname + '.par', 'wb') as handle:
        pickle.dump(BiasParameter, handle)
    
    print(f'".par" file created in {fdir}')

def bias_spectr_par_load(fdir, fname):
    with open(fdir + fname, 'rb') as handle:
        BiasParameter = pickle.load(handle)
    for keys in BiasParameter:
        BiasParameter[keys] = BiasParameter[keys].replace({'No change': 0,
                                                           'Yes/On': 1,
                                                           'No/Off': 2,
                                                           'False/Off': 0,
                                                           'True/On': 1})
    return BiasParameter

def bias_spectr(com, par, basename = ):
    connect.BiasSpectrOpen()
    props = (int(par['BiasSpectrProps'].loc['Save all', 0]),
             int(par['BiasSpectrProps'].loc['Number of sweeps']),
             par['BiasSpectrProps'].loc['Backward sweep', 0],
             int(par['BiasSpectrProps'].loc['Number of points']),
             float(par['BiasSpectrTiming'].loc['Z offset (m)']),
             par['BiasSpectrMore'].loc['Auto save', 0],
             par['BiasSpectrMore'].loc['Save dialog', 0])
    
    connect.BiasSpectrChsSet(*par['BiasSpectrChs'].values)
    connect.BiasSpectrPropsSet(*props)
    connect.BiasSpectrAdvPropsSet(*par['BiasSpectrAdvProps'].values)
    connect.BiasSpectrLimitsSet(*par['BiasSpectrLimits'].values)
    connect.BiasSpectrTimingSet(*par['BiasSpectrTiming'].values)
    print(*par['BiasSpectrTTLSync'].values)

    connect.BiasSpectrTTLSyncSet(*par['BiasSpectrTTLSync'].values)
    connect.BiasSpectrAltZCtrlSet(*par['BiasSpectrAltZCtrl'].values)
    connect.BiasSpectrMLSLockinPerSegSet(*par['BiasSpectrMLSLockinPerSeg'].values)
    connect.BiasSpectrMLSModeSet(*par['BiasSpectrMLSMode'].values)
    connect.BiasSpectrMLSValsSet(*par['BiasSpectrMLSVals'].values)

    connect.LockInModAmpSet(*par['LockInModAmp1'].values)
    connect.LockInModPhasFreqSet(*par['LockInModFreq1'].values)
    connect.LockInModOnOffSet(*par['LockInOnOff1'].values)
    data, parameters = connect.BiasSpectrStart(1, basename)

    return data, parameters

# my_tcp.socket_close()
