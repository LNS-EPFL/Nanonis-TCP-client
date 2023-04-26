# -*- encoding: utf-8 -*-
'''
@Time    :   2023/03/05 15:51:09
@Author  :   Shixuan Shan 
'''
import pickle
import pandas as pd
from os import mkdir
from os.path import exists
import time
import numpy as np

class esr_meas:
    def __init__(self, connect):
        self.connect = connect
        return
    
    def check_dirs(self, dirName):
        if not exists(dirName):
            mkdir(dirName)
            print("Directory ", dirName,  " Created ")
        return dirName
    
    #################################### BIAS SPECTROSCOPY ###################################3
    def bias_spectr_par_get(self):
        bias_par = {'Bias': self.connect.BiasGet(),
                    'BiasSpectrChs': self.connect.BiasSpectrChsGet(),
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
        return bias_par
    
    def bias_spectr_par_save(self, bias_par, fdir, fname = ''):
        with open(fdir + '/BiasSpectr' + fname + '.par', 'wb') as handle:
            pickle.dump(bias_par, handle)
        print(f'".par" file created in {fdir}')

    def bias_spectr_par_load(self, fdir, fname):
        with open(fdir + '/' + fname, 'rb') as handle:
            bias_par = pickle.load(handle)
        for keys in bias_par:
            bias_par[keys] = bias_par[keys].replace(['No change', 'Yes/On', 'No/Off', 'False/Off', 'True/On'], [0, 1, 2, 0, 1])
        return bias_par

    def bias_spectr(self, par, data_folder, basename = '%Y%m%d_', run = True):
        self.connect.BiasSpectrOpen()
        props = (int(par['BiasSpectrProps'].loc['Save all', 0]),
                 int(par['BiasSpectrProps'].loc['Number of sweeps']),
                 par['BiasSpectrProps'].loc['Backward sweep', 0],
                 int(par['BiasSpectrProps'].loc['Number of points']),
                 float(par['BiasSpectrTiming'].loc['Z offset (m)']),
                 par['BiasSpectrMore'].loc['Auto save', 0],
                 par['BiasSpectrMore'].loc['Save dialog', 0])
        self.connect.BiasSet(*par['Bias'].values)
        self.connect.BiasSpectrChsSet(*par['BiasSpectrChs'].values.tolist())
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

        if run:
            self.connect.LockInModOnOffSet(*par['LockInOnOff1'].values)
            sess_path = self.connect.UtilSessionPathGet().loc['Session path', 0]
            bias_spectr_path = self.check_dirs(sess_path + '\\' + data_folder)
            self.connect.UtilSessionPathSet(bias_spectr_path, 0)
            data, parameters = self.connect.BiasSpectrStart(1, basename)
            self.connect.LockInModOnOffSet(1, 0)
            self.connect.UtilSessionPathSet(sess_path, 0)
            return data, parameters
        
    ##################################### PICK UP ATOMS ##################################    
    def atom_pickup(self):
        def meas_dz(radius = 1.5e-9):
            z_cen = self.connect.ZCtrlZPosGet()
            xy = self.connect.FolMeXYPosGet(1)
            x = xy.loc['X (m)']
            y = xy.loc['Y (m)']
            surrounding_xy_list_ = [[x-radius, y], [x, y-radius], [x+radius,y], [x, y+radius]]
            surrounding_z_list = []

            for i in range(len(surrounding_xy_list_)):
                self.connect.FolMeXYPosSet(*surrounding_xy_list_[i], 1)
                self.connect.FolMeXYPosGet(1)
                surrounding_z = self.connect.ZCtrlZPosGet()
                surrounding_z_list.append(surrounding_z)
            self.connect.FolMeXYPosSet(x, y, 1)
            z_sur = np.mean(surrounding_z_list)
            print('--------------', z_cen.iloc[0, 0] - z_sur, '-------------')
            return z_cen - z_sur

        bias_ini = self.connect.BiasGet()

        # tracking the atom for 3s
        self.connect.AtomTrackCtrlSet(0,1)
        self.connect.AtomTrackCtrlSet(1,1)
        print('Wait atom tracking for 3 seconds...')
        time.sleep(3)
        self.connect.AtomTrackCtrlSet(0,0)
        self.connect.AtomTrackCtrlSet(1,0)

        dz1 = meas_dz()
        self.connect.BiasSet('50u')
        self.connect.ZCtrlOnOffSet(0)
        self.connect.BiasPulse(1, '150m', '650m', 1, 0)
        self.connect.BiasSet(bias_ini.loc['Bias (V)', 0])
        dz2 = meas_dz()
        delta_z = dz1[0] - dz2[0]
        print(dz1)
        print(f'delta z (pm): {delta_z*1e12}')
        if delta_z > 80e-12:
            print('Atom picked up.')
        else:
            print('Atom not picked up. Try again!')
        return