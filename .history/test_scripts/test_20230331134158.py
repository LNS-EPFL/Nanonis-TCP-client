import nanonis_esr_tcp as tcp
import time
import pickle
import numpy as np
import pandas as pd

my_tcp = tcp.tcp_ctrl()
connect = tcp.nanonis_ctrl(my_tcp)

def bias_spectr_par_save(com, fname, ):
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
    with open('BiasSpectr' + fname + '.par', 'wb') as handle:
        pickle.dump(BiasParameter, handle)
    return

def bias_spectr_par_load():
    return

def bias_spectr():
    return

# my_tcp.socket_close()
