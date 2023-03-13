# -*- encoding: utf-8 -*-
'''
@Time    :   2023/03/04 01:54:34
@Author  :   Shixuan Shan 
'''
from tcp_ctrl import tcp_ctrl
import pandas as pd
import numpy as np

class nanonis_ctrl:
    def __init__(self, tcp):
        self.tcp = tcp

# recommend to construct body first so that you don't need to calculate the body size by yourself
######################################## Bias Module #############################################
    def BiasSet(self, bias):
        bias = self.tcp.unit_cvt(bias)
        if bias > 10:
            raise ValueError('The maximum allowed bias is 10V. Please check your input! Bias has been set to 0 to protect the tip!')    
        
        body = self.tcp.dtype_cvt(bias, 'float32', 'bin')
        header = self.tcp.header_construct('Bias.Set', body_size = len(body))
        cmd = header+body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        print(f'The bias voltage is set to {bias}V')

    def BiasGet(self):
        header = self.tcp.header_construct('Bias.Get', body_size=0) # the body size here is the body size of Bias.Get argument 

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('float32')

        self.tcp.print_err(res_err)
        bias = str(res_arg[0]) + 'V' # first [0] gives the res_arg list, second [0] gives the bias value in the list
        print(f'Current bias: {bias}')
        return bias
    
    def BiasRangeSet(): 
        return print('function in progress......')
    
    def BiasRangeGet():
        return print('function in progress......')
    
    def BiasCalibrSet():
        return print('function in progress......')

    def BiasCalibrGet():
        return print('function in progress......')
    
    def BiasPulse(self, wait_until_done, bias_pulse_width, bias_value, zctrl_on_hold, pulse_abs_rel):
        bias_pulse_width = self.tcp.unit_cvt(bias_pulse_width)
        bias_value = self.tcp.unit_cvt(bias_value)
        if bias_value > 10:
            raise ValueError('The maximum allowed bias is 10V. Please check your input! Bias has been set to 0 to protect the tip!') 
        
        # recommend to construct body first so that you don't need to calculate the body size by yourself
        body  = self.tcp.dtype_cvt(wait_until_done, 'uint32', 'bin')
        body += self.tcp.dtype_cvt(bias_pulse_width, 'float32', 'bin')
        body += self.tcp.dtype_cvt(bias_value, 'float32', 'bin')
        body += self.tcp.dtype_cvt(zctrl_on_hold, 'uint16', 'bin')
        body += self.tcp.dtype_cvt(pulse_abs_rel, 'uint16', 'bin')
        header = self.tcp.header_construct('Bias.Pulse', body_size = len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        print(f'Bias pulse finished. \n Pulse width: {bias_pulse_width}s \n Pulse value: {bias_value}V')

######################################## Bias Spectroscopy Module #############################################
    def BiasSpectrOpen(self):
        header = self.tcp.header_construct('BiasSpectr.Open', body_size=0)

        self.tcp.cmd_send(header)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        print('Bias Spectroscopy window opened.')

    def BiasSpectrStart(self, get_data, save_base_name):
        save_base_name_size = len(save_base_name)

        print('Scanning tunneling spectroscopy (STS) launched. Please wait...')
        body  = self.tcp.dtype_cvt(get_data, 'uint32', 'bin')
        body += self.tcp.dtype_cvt(save_base_name_size, 'int', 'bin')
        body += self.tcp.dtype_cvt(save_base_name, 'str', 'bin')
        header = self.tcp.header_construct('BiasSpectr.Start', body_size = len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, res_arg, res_err= self.tcp.res_recv('int', 'int', '1dstr', 'int', 'int', '2dfloat32', 'int', '1dfloat32')
        
        self.tcp.print_err(res_err)
        bias_spectr_df = pd.DataFrame(res_arg[5].T, columns = res_arg[2][0])

        bias_spectr_param_df = pd.DataFrame(res_arg[7].T)
        print('STS done!')
        print(bias_spectr_df)
        print(bias_spectr_param_df)
        return bias_spectr_df, bias_spectr_param_df

    def BiasSpectrStop(self):
        header = self.tcp.header_construct('BiasSpectr.Stop', body_size=0)

        self.tcp.cmd_send(header)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        print('STS stopped.')

    def BiasSpectrStatusGet(self):
        header = self.tcp.header_construct('BiasSpectr.StatusGet', body_size=0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('uint32')

        self.tcp.print_err(res_err)
        status_df = pd.DataFrame({'Current status': 'Running' if res_arg[0] == 1 else 'Not running'}, index=[0]).T

        print('\n'+
              status_df.to_string(header=False)+
              '\n')
    
    def BiasSpectrChsSet(self, num_chs, ch_idx):
        print('To get the signal name and its corresponding index in the list of the 128 available signals in the Nanonis Controller, use the "Signal.NamesGet" function, or check the RT Idx value in the Signals Manager module.')

        body  = self.tcp.dtype_cvt(num_chs, 'int', 'bin')
        body += self.tcp.dtype_cvt(ch_idx, '1dint', 'bin')
        header = self.tcp.header_construct('BiasSpectr.ChsSet', body_size = len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        chs_df = pd.DataFrame({'Number of channels:': num_chs,
                               'Channel indexes:': ch_idx},
                               index=[0]).T

        print('\n'+
              chs_df.to_string(header=False)+
              '\n\nChannels set.')
        return chs_df

    def BiasSpectrChsGet(self):
        header = self.tcp.header_construct('BiasSpectr.ChsGet', body_size = 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('int', '1dint')

        self.tcp.print_err(res_err)
        chs_df = pd.DataFrame({'Number of channels:': res_arg[0],
                               'Channel indexes:': [res_arg[1]]},
                               index=[0]).T

        print('\n'+
              chs_df.to_string(header=False)+
              '\n\n Channels returned.')
        return chs_df

    def BiasSpectrPropsSet(self, save_all, num_sweeps, bw_sweep, num_pts, z_offset, auto_save, show_save_dialog):
        z_offset = self.tcp.unit_cvt(z_offset)

        body  = self.tcp.dtype_cvt(save_all, 'uint16', 'bin')
        body += self.tcp.dtype_cvt(num_sweeps, 'int', 'bin')
        body += self.tcp.dtype_cvt(bw_sweep, 'uint16', 'bin')
        body += self.tcp.dtype_cvt(num_pts, 'uint16', 'bin')
        body += self.tcp.dtype_cvt(z_offset, 'float32', 'bin')
        body += self.tcp.dtype_cvt(auto_save, 'uint16', 'bin')
        body += self.tcp.dtype_cvt(show_save_dialog, 'uint16', 'bin')
        header = self.tcp.header_construct('BiasSpectr.PropsSet', body_size = len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        props_df = pd.DataFrame({'Save all:': self.tcp.tristate_cvt(save_all), 
                                 'Number of sweeps:': num_sweeps, 
                                 'Backward sweep:': self.tcp.tristate_cvt(bw_sweep), 
                                 'Number of points:': num_pts, 
                                 'Z offset (m):': z_offset,
                                 'Autosave:': self.tcp.tristate_cvt(auto_save), 
                                 'Show save dialog:': self.tcp.tristate_cvt(show_save_dialog)},
                                 index=[0]).T

        print('\n'+
              props_df.to_string(header=False)+
              '\n\nBias spectroscopy properties set.')
        return props_df

    def BiasSpectrPropsGet(self):
        header = self.tcp.header_construct('BiasSpectr.PropsGet', body_size = 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('uint16', 'int', 'uint16', 'int', 'int', 'int', '1dstr', 'int', 'int', '1dstr', 'int', 'int', '1dstr')

        self.tcp.print_err(res_err)
        props_df = pd.DataFrame({'Save all:': self.tcp.tristate_cvt(res_arg[0]), 
                                 'Number of sweeps:': res_arg[1], 
                                 'Backward sweep:': self.tcp.tristate_cvt(res_arg[2]), 
                                 'Number of points:': res_arg[3], 
                                 'Number of channels:': res_arg[5],
                                 'Channels:': res_arg[6].tolist(), 
                                 'Number of parameters:': res_arg[8],
                                 'Parameters:': res_arg[9].tolist(),
                                 'Number of fixed parameters:': res_arg[11],
                                 'Fixed parameters:': res_arg[12].tolist()
                                 }).T
        print('\n'+
              props_df.to_string(header=False) + 
              '\n\nBias spectroscopy properties returned.')
        return props_df
    
    def BiasSpectrAdvPropsSet(self, reset_bias, z_ctrl_hold, rec_final_z, lock_in_run):
        body  = self.tcp.dtype_cvt(reset_bias, 'uint16', 'bin')
        body += self.tcp.dtype_cvt(z_ctrl_hold, 'uint16', 'bin')
        body += self.tcp.dtype_cvt(rec_final_z, 'uint16', 'bin')
        body += self.tcp.dtype_cvt(lock_in_run, 'uint16', 'bin')
        header = self.tcp.header_construct('BiasSpectr.AdvPropsSet', body_size = len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        props_df = pd.DataFrame({'Reset bias:': self.tcp.tristate_cvt(reset_bias), 
                                 'Z-Controller hold:': self.tcp.tristate_cvt(z_ctrl_hold), 
                                 'Record final Z:': self.tcp.tristate_cvt(rec_final_z), 
                                 'Lockin Run:': self.tcp.tristate_cvt(lock_in_run), 
                                 }).T
        print('\n'+
              props_df.to_string(header=False)+
              '\n\nBias spectroscopy advanced properties set.')
        return props_df
    
    def BiasSpectrAdvPropsGet(self):
        header = self.tcp.header_construct('BiasSpectr.AdvPropsGet', body_size = 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('uint16', 'uint16', 'uint16', 'uint16')

        self.tcp.print_err(res_err)
        props_df = pd.DataFrame({'Reset bias:': self.tcp.tristate_cvt(res_arg[0]), 
                                 'Z-Controller hold:': self.tcp.tristate_cvt(res_arg[1]), 
                                 'Record final Z:': self.tcp.tristate_cvt(res_arg[2]), 
                                 'Lockin Run:': self.tcp.tristate_cvt(res_arg[3]), 
                                 },
                                 index=[0]).T
        print('\n'+
              props_df.to_string(header=False)+
              '\n\nBias spectroscopy advanced properties returned.')
        return props_df
    
    def BiasSpectrLimitsSet(self, start_val, end_val):
        start_val = self.tcp.unit_cvt(start_val)
        end_val = self.tcp.unit_cvt(end_val)

        body  = self.tcp.dtype_cvt(start_val, 'float32', 'bin')
        body += self.tcp.dtype_cvt(end_val, 'float32', 'bin')
        header = self.tcp.header_construct('BiasSpectr.LimitsSet', body_size = len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        limits_df = pd.DataFrame({'Start value (V):': start_val, 
                                 'Stop value (V):': end_val, 
                                 },
                                 index=[0]).T
        print('\n'+
              limits_df.to_string(header=False)+
              '\n\nBias limits set.')
        return limits_df
    
    def BiasSpectrLimitsGet(self):
        header = self.tcp.header_construct('BiasSpectr.LimitsGet', body_size = 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('float32', 'float32')

        self.tcp.print_err(res_err)
        limits_df = pd.DataFrame({'Start value (V):': res_arg[0], 
                                 'Stop value (V):': res_arg[1]},
                                 index=[0]).T
        print('\n'+
              limits_df.to_string(header=False)+
              '\n\nBias spectroscopy bias limits returned.')
        return limits_df
    
    def BiasSpectrTimingSet(self, z_avg_t, z_offset, init_settling_t, max_slew_rate, settling_t, int_t, end_settling_t, z_ctrl_t):
        z_avg_t = self.tcp.unit_cvt(z_avg_t)
        z_offset = self.tcp.unit_cvt(z_offset)
        init_settling_t = self.tcp.unit_cvt(init_settling_t)
        max_slew_rate = self.tcp.unit_cvt(max_slew_rate)
        settling_t = self.tcp.unit_cvt(settling_t)
        int_t = self.tcp.unit_cvt(int_t)
        end_settling_t = self.tcp.unit_cvt(end_settling_t)
        z_ctrl_t = self.tcp.unit_cvt(z_ctrl_t)

        body  = self.tcp.dtype_cvt(z_avg_t, 'float32', 'bin')
        body += self.tcp.dtype_cvt(z_offset, 'float32', 'bin')
        body += self.tcp.dtype_cvt(init_settling_t, 'float32', 'bin')
        body += self.tcp.dtype_cvt(max_slew_rate, 'float32', 'bin')
        body += self.tcp.dtype_cvt(settling_t, 'float32', 'bin')
        body += self.tcp.dtype_cvt(int_t, 'float32', 'bin')
        body += self.tcp.dtype_cvt(end_settling_t, 'float32', 'bin')
        body += self.tcp.dtype_cvt(z_ctrl_t, 'float32', 'bin')
        header = self.tcp.header_construct('BiasSpectr.TimingSet', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        timing_df = pd.DataFrame({'Z averaging time (s):': z_avg_t,
                                   'Z offset (m):': z_offset,
                                   'Initial settling time (s):': init_settling_t,
                                   'Maximum slew rate (V/s):': max_slew_rate,
                                   'Settling time (s):': settling_t,
                                   'Integration time (s):': int_t,
                                   'End settling time (s):': end_settling_t,
                                   'Z control time (s):': z_ctrl_t}).T
        print('\n'+
              timing_df.to_string(header=False)+
              '\n\nBias spectroscopy timing set.')
        return timing_df

    def BiasSpectrTimingGet(self):
        header = self.tcp.header_construct('BiasSpectrTimingGet', 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('float32','float32','float32','float32','float32','float32','float32','float32')

        self.tcp.print_err(res_err)
        timing_df = pd.DataFrame({'Z averaging time (s):': res_arg[0],
                                  'Z offset (m):': res_arg[1],
                                  'Initial settling time (s):': res_arg[2],
                                  'Maximum slew rate (V/s):': res_arg[3],
                                  'Settling time (s):': res_arg[4],
                                  'Integration time (s):': res_arg[5],
                                  'End settling time (s):': res_arg[6],
                                  'Z control time (s):': res_arg[7]}).T
        print('\n'+
              timing_df.to_string(header=False)+
              '\n\nBias spectroscopy timing settings retured.')
        return timing_df

    def BiasSpectrTTLSyncSet(self):
        return print('function in progress......')
    
    def BiasSpectrTTLSyncGet(self):
        return print('function in progress......')
    
    def BiasSpectrAltZCtrlSet(self):
        return print('function in progress......')
    
    def BiasSpectrAltZCtrlGet(self):
        return print('function in progress......')
    
    def BiasSpectrMLSLockinPerSegSet(self):
        return print('function in progress......')
    
    def BiasSpectrMLSLockinPerSegGet(self):
        return print('function in progress......')
    
    def BiasSpectrMLSModeSet(self):
        return print('function in progress......')
    
    def BiasSpectrMLSModeGet(self):
        return print('function in progress......')
    
    def BiasSpectrMLSValsSet(self):
        return print('function in progress......')
    
    def BiasSpectrMLSValsGet(self):
        return print('function in progress......')

######################################## Current Module #############################################
    def CurrentGet(self):
        return

    def Current100Get(self):
        return

    def CurrentBEEMGet(self):
        return

    def CurrentGainSet(self):
        return

    def CurrentGainsGet(self):
        return

    def CurrentCalibrSet(self):
        return

    def CurrentCalibrGet(self):
        return

######################################## Z-controller Module #############################################
    def ZCtrlZPosSet(self):
        return
          
    def ZCtrlZPosGet(self):
        return
          
    def ZCtrlOnOffSet(self):
        return
         
    def ZCtrlOnOffGet(self):
        return
         
    def ZCtrlSetpntSet(self):
        return
        
    def ZCtrlSetpntGet(self):
        return
        
    def ZCtrlGainSet(self):
        return
          
    def ZCtrlGainGet(self):
        return
          
    def ZCtrlSwitchOffDelaySet(self):
        return

    def ZCtrlSwitchOffDelayGet(self):
        return

    def ZCtrlTipLiftSet(self):
        return

    def ZCtrlTipLiftGet(self):
        return

    def ZCtrlHome(self):
        return

    def ZCtrlHomePropsSet(self):
        return

    def ZCtrlHomePropsGet(self):
        return

    def ZCtrlActiveCtrlSet(self):
        return

    def ZCtrlCtrlListGet(self):
        return

    def ZCtrlWithdraw(self):
        return

    def ZCtrlWithdrawRateSet(self):
        return

    def ZCtrlWithdrawRateGet(self):
        return

    def ZCtrlLimitsEnabledSet(self):
        return

    def ZCtrlLimitsEnabledGet(self):
        return

    def ZCtrlLimitsSet(self):
        return

    def ZCtrlLimitsGet(self):
        return

    def ZCtrlStatusGet(self):
        return

######################################## Safe Tip Module #############################################
######################################## Auto Approach Module #############################################
######################################## Scan Module #############################################
######################################## Follow Me Module #############################################
######################################## Tip Shaper Module #############################################
    def TipShaperStart(self):
        return

    def TipShaperPropsSet(self):
        return

    def TipShaperPropsGet(self):
        return

######################################## Generic Sweeper Module #############################################
    def GenSwpAcqChsSet(self):
        return

    def GenSwpAcqChsGet(self):
        return

    def GenSwpSwpSignalSet(self):
        return

    def GenSwpSwpSignalGet(self):
        return

    def GenSwpLimitsSet(self):
        return

    def GenSwpLimitsGet(self):
        return

    def GenSwpPropsSet(self):
        return

    def GenSwpPropsGet(self):
        return

    def GenSwpStart(self):
        return

    def GenSwpStop(self):
        return

    def GenSwpOpen(self):
        return

######################################## Atom Tracking Module #############################################
    def AtomTrackCtrlSet(self):
        return

    def AtomTrackStatusGet(self):
        return

    def AtomTrackPropsSet(self):
        return

    def AtomTrackPropsGet(self):
        return

    def AtomTrackQuickCompStart(self):
        return

    def AtomTrackDriftComp(self):
        return

######################################## Lock-in Module #############################################
LockIn.ModOnOffSet......................................................................................................................... 119
LockIn.ModOnOffGet ........................................................................................................................ 119
LockIn.ModSignalSet ......................................................................................................................... 119
LockIn.ModSignalGet ........................................................................................................................ 120
LockIn.ModPhasRegSet ..................................................................................................................... 120
LockIn.ModPhasRegGet .................................................................................................................... 121
LockIn.ModHarmonicSet ................................................................................................................... 121
LockIn.ModHarmonicGet .................................................................................................................. 122
LockIn.ModPhasSet ........................................................................................................................... 122
LockIn.ModPhasGet .......................................................................................................................... 122
LockIn.ModAmpSet ........................................................................................................................... 123
LockIn.ModAmpGet .......................................................................................................................... 123
LockIn.ModPhasFreqSet ................................................................................................................... 123
LockIn.ModPhasFreqGet ................................................................................................................... 124
LockIn.DemodSignalSet ..................................................................................................................... 124
LockIn.DemodSignalGet .................................................................................................................... 124
LockIn.DemodHarmonicSet .............................................................................................................. 125
LockIn.DemodHarmonicGet .............................................................................................................. 125
LockIn.DemodHPFilterSet ................................................................................................................. 126
LockIn.DemodHPFilterGet................................................................................................................. 126
LockIn.DemodLPFilterSet .................................................................................................................. 127
LockIn.DemodLPFilterGet ................................................................................................................. 127
LockIn.DemodPhasRegSet ................................................................................................................ 128
LockIn.DemodPhasRegGet ................................................................................................................ 128
LockIn.DemodPhasSet....................................................................................................................... 129
LockIn.DemodPhasGet ...................................................................................................................... 129
LockIn.DemodSyncFilterSet .............................................................................................................. 129
LockIn.DemodSyncFilterGet .............................................................................................................. 130
LockIn.DemodRTSignalsSet ............................................................................................................... 130
LockIn.DemodRTSignalsGet .............................................................................................................. 131
Lock-In Frequency Sweep ..................................................................................................................... 132
LockInFreqSwp.Open ........................................................................................................................ 132
LockInFreqSwp.Start ......................................................................................................................... 132
LockInFreqSwp.SignalSet .................................................................................................................. 133
LockInFreqSwp.SignalGet .................................................................................................................. 133
LockInFreqSwp.LimitsSet .................................................................................................................. 133
LockInFreqSwp.LimitsGet .................................................................................................................. 133
LockInFreqSwp.PropsSet ................................................................................................................... 134
LockInFreqSwp.PropsGet .................................................................................................................. 134

tcp = tcp_ctrl()
ccc = nanonis_ctrl(tcp)
# ccc.help()
ccc.BiasSet('700m')
# ccc.BiasGet()
# ccc.BiasPulse('600m', '7')
# ccc.BiasSpectrOpen()
# ccc.BiasSpectrStart('drfue')
ccc.BiasSpectrTimingGet()
# ccc.BiasSpectrPropsSet(0, 1, 0, 101, '5n', 0)
 