import nanonis_esr_tcp as tcp
import time
import pickle
import numpy as np
import pandas as pd

my_tcp = tcp.tcp_ctrl()
connect = tcp.nanonis_ctrl(my_tcp)

def bias_spectr_par_save():
    BiasParameter = {'BiasSpectrChs': connect.BiasSpectrChsGet(),
                     'BiasSpectrProps': connect.BiasSpectrPropsGet(),
                     'BiasSpectrAdvProps': connect.BiasSpectrAdvPropsGet(),
                     'BiasSpectrLimits': connect.BiasSpectrLimitsGet(),
                     'BiasSpectrTiming': connect.BiasSpectrTimingGet(),
                     'BiasSpectrTTLSync': connect.BiasSpectrTTLSyncGet(),
                     'BiasSpectrAltZCtrl': connect.BiasSpectrAltZCtrlGet(),
                     'BiasSpectrMLSLockinPerSeg': connect.BiasSpectrMLSLockinPerSegGet(),
                     'BiasSpectrMLSMode': connect.BiasSpectrMLSModeGet(),
                     'BiasSpectrMLSVals': connect.BiasSpectrMLSValsGet(),
                     'BiasSpectrMore': pd.DataFrame({'Auto save': 'Yes/On', 'Save dialog': 'No/Off', 'Basename' : 'STS_%Y%m%d_'}, index=[0]).T,
                     'LockInModAmp1': connect.LockInModAmpGet(1),
                     'LockInModFreq1': connect.LockInModPhasFreqGet(1),
                     'LockInOnOff1': connect.LockInModOnOffGet(1)
                      }
    with open('BiasSpectr.par', 'wb') as handle:
        pickle.dump(BiasParameter, handle)
    return

def bias_spectr_par_load():
    return

def bias_spectr():
    return

# my_tcp.socket_close()
