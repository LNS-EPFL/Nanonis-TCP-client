# -*- encoding: utf-8 -*-
'''
@Time    :   2023/03/05 15:51:09
@Author  :   Shixuan Shan 
'''
import pickle
import pandas as pd
from os import mkdir
from os.path import exists

class esr_meas:
    def __init__(self, connect):
        self.connect = connect
        return
    
    def check_dirs(self, dirName):
        if not exists(dirName):
            mkdir(dirName)
            print("Directory ", dirName,  " Created ")
        return dirName
    
    def bias_spectr_par_save(self, fdir, fname = ''):
        bias_par = {'BiasSpectrChs': self.connect.BiasSpectrChsGet(),
                    'BiasSpectrProps': self.connect.BiasSpectrPropsGet(),
                    'BiasSpectrAdvProps': self.connect.BiasSpectrAdvPropsGet(),
                    'BiasSpectrLimits': self.connect.BiasSpectrLimitsGet(),
                    'BiasSpectrTiming': self.connect.BiasSpectrTimingGet(),
                    'BiasSpectrTTLSync': self.connect.BiasSpectrTTLSyncGet(),
                    'BiasSpectrAltZCtrl': self.connect.BiasSpectrAltZCtrlGet(),
                    'BiasSpectrMLSLockinPerSeg': self.connect.BiasSpectrMLSLockinPerSegGet(),
                    'BiasSpectrMLSMode': self.connect.BiasSpectrMLSModeGet(),
                    'BiasSpectrMLSVals': self.connect.BiasSpectrMLSValsGet(),
                    'BiasSpectrMore': pd.DataFrame({'Auto save': 'Yes/On', 'Save dialog': 'No/Off', 'Basename' : 'STS_%Y%m%d_'}, index=[0]).T,
                    'LockInModAmp1': self.connect.LockInModAmpGet(1),
                    'LockInModFreq1': self.connect.LockInModPhasFreqGet(1),
                    'LockInOnOff1': self.connect.LockInModOnOffGet(1),
                    }
        with open(fdir + '/BiasSpectr' + fname + '.par', 'wb') as handle:
            pickle.dump(bias_par, handle)
        print(f'".par" file created in {fdir}')

    def bias_spectr_par_load(self, fdir, fname):
        with open(fdir + '/' + fname, 'rb') as handle:
            bias_par = pickle.load(handle)
        for keys in bias_par:
            bias_par[keys] = bias_par[keys].replace({'No change': 0,
                                                     'Yes/On': 1,
                                                     'No/Off': 2,
                                                     'False/Off': 0,
                                                     'True/On': 1})
        return bias_par

    def bias_spectr(self, par, data_folder, basename = '%Y%m%d_'):
        self.connect.BiasSpectrOpen()
        props = (int(par['BiasSpectrProps'].loc['Save all', 0]),
                 int(par['BiasSpectrProps'].loc['Number of sweeps']),
                 par['BiasSpectrProps'].loc['Backward sweep', 0],
                 int(par['BiasSpectrProps'].loc['Number of points']),
                 float(par['BiasSpectrTiming'].loc['Z offset (m)']),
                 par['BiasSpectrMore'].loc['Auto save', 0],
                 par['BiasSpectrMore'].loc['Save dialog', 0])

        self.connect.BiasSpectrChsSet(*par['BiasSpectrChs'].values)
        self.connect.BiasSpectrPropsSet(*props)
        self.connect.BiasSpectrAdvPropsSet(*par['BiasSpectrAdvProps'].values)
        self.connect.BiasSpectrLimitsSet(*par['BiasSpectrLimits'].values)
        self.connect.BiasSpectrTimingSet(*par['BiasSpectrTiming'].values)
        self.connect.BiasSpectrTTLSyncSet(*par['BiasSpectrTTLSync'].values)
        self.connect.BiasSpectrAltZCtrlSet(*par['BiasSpectrAltZCtrl'].values)
        self.connect.BiasSpectrMLSLockinPerSegSet(*par['BiasSpectrMLSLockinPerSeg'].values)
        self.connect.BiasSpectrMLSModeSet(*par['BiasSpectrMLSMode'].values)
        self.connect.BiasSpectrMLSValsSet(*par['BiasSpectrMLSVals'].values)

        self.connect.LockInModAmpSet(*par['LockInModAmp1'].values)
        self.connect.LockInModPhasFreqSet(*par['LockInModFreq1'].values)
        self.connect.LockInModOnOffSet(*par['LockInOnOff1'].values)


        sess_path = self.connect.UtilSessionPathGet().loc['Session path', 0]
        bias_spectr_path = check_dirs(sess_path + '\\' + data_folder)
        self.connect.UtilSessionPathSet(bias_spectr_path, 0)
        data, parameters = self.connect.BiasSpectrStart(1, basename)
        self.connect.UtilSessionPathSet(sess_path, 0)
        return data, parameters