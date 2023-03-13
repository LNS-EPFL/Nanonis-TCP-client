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
        status_df = pd.DataFrame({'Bias spectroscopy status': self.tcp.bistate_cvt(res_arg[0])}, index=[0]).T

        print('\n'+
              status_df.to_string(header=False)+
              '\n\nBias Spectroscopy status returned.')
    
    def BiasSpectrChsSet(self, num_chs, ch_idx):
        print('To get the signal name and its corresponding index in the list of the 128 available signals in the Nanonis Controller, use the "Signal.NamesGet" function, or check the RT Idx value in the Signals Manager module.')

        body  = self.tcp.dtype_cvt(num_chs, 'int', 'bin')
        body += self.tcp.dtype_cvt(ch_idx, '1dint', 'bin')
        header = self.tcp.header_construct('BiasSpectr.ChsSet', body_size = len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        chs_df = pd.DataFrame({'Number of channels': num_chs,
                               'Channel indexes': ch_idx},
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
        chs_df = pd.DataFrame({'Number of channels': res_arg[0],
                               'Channel indexes': [res_arg[1]]},
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
        props_df = pd.DataFrame({'Save all': self.tcp.tristate_cvt(save_all), 
                                 'Number of sweeps': num_sweeps, 
                                 'Backward sweep': self.tcp.tristate_cvt(bw_sweep), 
                                 'Number of points': num_pts, 
                                 'Z offset (m)': z_offset,
                                 'Autosave': self.tcp.tristate_cvt(auto_save), 
                                 'Show save dialog': self.tcp.tristate_cvt(show_save_dialog)},
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
        props_df = pd.DataFrame({'Save all': self.tcp.tristate_cvt(res_arg[0]), 
                                 'Number of sweeps': res_arg[1], 
                                 'Backward sweep': self.tcp.tristate_cvt(res_arg[2]), 
                                 'Number of points': res_arg[3], 
                                 'Number of channels': res_arg[5],
                                 'Channels': res_arg[6].tolist(), 
                                 'Number of parameters': res_arg[8],
                                 'Parameters': res_arg[9].tolist(),
                                 'Number of fixed parameters': res_arg[11],
                                 'Fixed parameters': res_arg[12].tolist()
                                 },
                                 index=[0]).T
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
        props_df = pd.DataFrame({'Reset bias': self.tcp.tristate_cvt(reset_bias), 
                                 'Z-Controller hold': self.tcp.tristate_cvt(z_ctrl_hold), 
                                 'Record final Z': self.tcp.tristate_cvt(rec_final_z), 
                                 'Lockin Run': self.tcp.tristate_cvt(lock_in_run), 
                                 },
                                 index=[0]).T
        print('\n'+
              props_df.to_string(header=False)+
              '\n\nBias spectroscopy advanced properties set.')
        return props_df
    
    def BiasSpectrAdvPropsGet(self):
        header = self.tcp.header_construct('BiasSpectr.AdvPropsGet', body_size = 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('uint16', 'uint16', 'uint16', 'uint16')

        self.tcp.print_err(res_err)
        props_df = pd.DataFrame({'Reset bias': self.tcp.tristate_cvt(res_arg[0]), 
                                 'Z-Controller hold': self.tcp.tristate_cvt(res_arg[1]), 
                                 'Record final Z': self.tcp.tristate_cvt(res_arg[2]), 
                                 'Lockin Run': self.tcp.tristate_cvt(res_arg[3]), 
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
        limits_df = pd.DataFrame({'Start value (V)': start_val, 
                                 'Stop value (V)': end_val, 
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
        limits_df = pd.DataFrame({'Start value (V)': res_arg[0], 
                                 'Stop value (V)': res_arg[1]},
                                 index=[0]).T
        print('\n'+
              limits_df.to_string(header=False)+
              '\n\nBias spectroscopy bias limits returned.')
        return limits_df
    
    def BiasSpectrTimingSet(self, z_avg_t, z_offset, init_settling_t, max_slew_rate, settling_t, inte_t, end_settling_t, z_ctrl_t):
        z_avg_t = self.tcp.unit_cvt(z_avg_t)
        z_offset = self.tcp.unit_cvt(z_offset)
        init_settling_t = self.tcp.unit_cvt(init_settling_t)
        max_slew_rate = self.tcp.unit_cvt(max_slew_rate)
        settling_t = self.tcp.unit_cvt(settling_t)
        inte_t = self.tcp.unit_cvt(inte_t)
        end_settling_t = self.tcp.unit_cvt(end_settling_t)
        z_ctrl_t = self.tcp.unit_cvt(z_ctrl_t)

        body  = self.tcp.dtype_cvt(z_avg_t, 'float32', 'bin')
        body += self.tcp.dtype_cvt(z_offset, 'float32', 'bin')
        body += self.tcp.dtype_cvt(init_settling_t, 'float32', 'bin')
        body += self.tcp.dtype_cvt(max_slew_rate, 'float32', 'bin')
        body += self.tcp.dtype_cvt(settling_t, 'float32', 'bin')
        body += self.tcp.dtype_cvt(inte_t, 'float32', 'bin')
        body += self.tcp.dtype_cvt(end_settling_t, 'float32', 'bin')
        body += self.tcp.dtype_cvt(z_ctrl_t, 'float32', 'bin')
        header = self.tcp.header_construct('BiasSpectr.TimingSet', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        timing_df = pd.DataFrame({'Z averaging time (s)': z_avg_t,
                                   'Z offset (m)': z_offset,
                                   'Initial settling time (s)': init_settling_t,
                                   'Maximum slew rate (V/s)': max_slew_rate,
                                   'Settling time (s)': settling_t,
                                   'Integration time (s)': inte_t,
                                   'End settling time (s)': end_settling_t,
                                   'Z control time (s)': z_ctrl_t},
                                 index=[0]).T
        print('\n'+
              timing_df.to_string(header=False)+
              '\n\nBias spectroscopy timing set.')
        return timing_df

    def BiasSpectrTimingGet(self):
        header = self.tcp.header_construct('BiasSpectr.TimingGet', 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('float32','float32','float32','float32','float32','float32','float32','float32')

        self.tcp.print_err(res_err)
        timing_df = pd.DataFrame({'Z averaging time (s)': res_arg[0],
                                  'Z offset (m)': res_arg[1],
                                  'Initial settling time (s)': res_arg[2],
                                  'Maximum slew rate (V/s)': res_arg[3],
                                  'Settling time (s)': res_arg[4],
                                  'Integration time (s)': res_arg[5],
                                  'End settling time (s)': res_arg[6],
                                  'Z control time (s)': res_arg[7]},
                                 index=[0]).T
        print('\n'+
              timing_df.to_string(header=False)+
              '\n\nBias spectroscopy timing settings retured.')
        return timing_df

    def BiasSpectrTTLSyncSet(self, enable, ttl_line, ttl_polarity, t_2_on, on_duration):
        t_2_on = self.tcp.unit_cvt(t_2_on)
        on_duration = self.tcp.unit_cvt(on_duration)

        body  = self.tcp.dtype_cvt(enable, 'uint16', 'bin')
        body += self.tcp.dtype_cvt(ttl_line, 'uint16', 'bin')
        body += self.tcp.dtype_cvt(ttl_polarity, 'unint16', 'bin')
        body += self.tcp.dtype_cvt(t_2_on, 'float32', 'bin')
        body += self.tcp.dtype_cvt(on_duration, 'float32', 'bin')
        header = self.tcp.header_construct('BiasSpectr.TTLSyncSet', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        ttl_df = pd.DataFrame({'Enable': self.tcp.tristate_cvt(enable),
                               'TTL line': self.tcp.tristate_cvt(ttl_line),
                               'TTL polarity': self.tcp.tristate_cvt(ttl_polarity),
                               'Time to on (s)': t_2_on,
                               'On duration (s)': on_duration},
                                index=[0]).T
        print('\n'+
              ttl_df.to_string(header=False)+
              '\n\nTTL sychronizetion set.')
        return ttl_df
    
    def BiasSpectrTTLSyncGet(self):
        header = self.tcp.header_construct('BiasSpectr.TTLSyncGet', body_size = 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('uint16', 'uint16', 'uint16', 'float32', 'float32')

        self.tcp.print_err(res_err)
        ttl_df = pd.DataFrame({'Enable': self.tcp.tristate_cvt(res_arg[0]),
                               'TTL line': self.tcp.tristate_cvt(res_arg[1]),
                               'TTL polarity': self.tcp.tristate_cvt(res_arg[2]),
                               'Time to on (s)': res_arg[3],
                               'On duration (s)': res_arg[4]},
                                index=[0]).T
        print('\n'+
              ttl_df.to_string(header=False)+
              '\n\nTTL sychronizetion settings returned.')
        return ttl_df

    def BiasSpectrAltZCtrlSet(self, alt_z_ctrl_sp, sp, settling_t):
        sp = self.tcp.unit_cvt(sp)
        settling_t = self.tcp.unit_cvt(settling_t)

        body  = self.tcp.dtype_cvt(alt_z_ctrl_sp, 'uint16', 'bin')
        body += self.tcp.dtype_cvt(sp, 'float32', 'bin')
        body += self.tcp.dtype_cvt(settling_t, 'float32', 'bin')
        header = self.tcp.header_construct('BiasSpectr.AltZCtrlSet', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        alt_z_ctrl_df = pd.DataFrame({'Alternative Z-controller setpoint': self.tcp.tristate_cvt(alt_z_ctrl_sp),
                                      'Setpoint (A)': sp,
                                      'Settling time (s)': settling_t
                                      },
                                        index=[0]).T  
        print('\n'+
              alt_z_ctrl_df.to_string(header=False)+
              '\n\nAlternative Z controller set.')
        return alt_z_ctrl_df   
    
    def BiasSpectrAltZCtrlGet(self):
        header = self.tcp.header_construct('BiasSpectr.AltZCtrlGet', 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('uint16', 'float32', 'float32')

        self.tcp.print_err(res_err)
        alt_z_ctrl_df = pd.DataFrame({'Alternative Z-controller setpoint': self.tcp.tristate_cvt(res_arg[0]),
                                      'Setpoint (A)': res_arg[1],
                                      'Settling time (s)': res_arg[2]
                                      },
                                      index=[0]).T  
        print('\n'+
              alt_z_ctrl_df.to_string(header=False)+
              '\n\nAlternative Z controller settings returned.')
        return alt_z_ctrl_df   
    
    def BiasSpectrMLSLockinPerSegSet(self, lockin_per_seg):
        body  = self.tcp.dtype_cvt(lockin_per_seg, 'uint32', 'bin')
        header = self.tcp.header_construct('BiasSpectr.MLSLockinPerSegSet', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        lockin_per_seg_df = pd.DataFrame({'Lock-in per segment': self.tcp.bistate_cvt(lockin_per_seg)},
                                index=[0]).T
        print('\n'+
              lockin_per_seg_df.to_string(header=False)+
              '\n\nLock-In per Segment flag in Multi line segment editor set.')
        return lockin_per_seg_df
    
    def BiasSpectrMLSLockinPerSegGet(self):
        header = self.tcp.header_construct('BiasSpectr.MLSLockinPerSegGet', 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('uint32')

        self.tcp.print_err(res_err)
        lockin_per_seg_df = pd.DataFrame({'Lock-in per segment': self.tcp.bistate_cvt(res_arg[0])},
                                index=[0]).T
        print('\n'+
              lockin_per_seg_df.to_string(header=False)+
              '\n\nLock-In per Segment flag in Multi line segment editor settings returned.')
        return lockin_per_seg_df          
    
    def BiasSpectrMLSModeSet(self, sweep_mode):
        # sweep mode: 'Linear' or 'MLS'
        sweep_mode_len = len(sweep_mode)

        body  = self.tcp.dtype_cvt(sweep_mode_len, 'int', 'bin')
        body += self.tcp.dtype_cvt(sweep_mode, 'str', 'bin')
        header = self.tcp.header_construct('BiasSpectr.MLSModeSet', body_size = len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        mls_mode_df = pd.DataFrame({'Sweep mode': sweep_mode},
                                 index=[0]).T
        print('\n'+
              mls_mode_df.to_string(header=False)+
              '\n\nBias spectroscopy sweep mode set.')
        return mls_mode_df
    
    def BiasSpectrMLSModeGet(self):
        header = self.tcp.header_construct('BiasSpectr.MLSModeGet', 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('str') # for string, no need to put 'int' before 'str'

        self.tcp.print_err(res_err)
        mls_mode_df = pd.DataFrame({'Sweep mode': res_arg},
                                index=[0]).T
        print('\n'+
              mls_mode_df.to_string(header=False)+
              '\n\nLock-In per Segment flag in Multi line segment editor settings returned.')
        return mls_mode_df 
    
    def BiasSpectrMLSValsSet(self, num_of_segs, bias_start, bias_end, init_settling_t, settling_t, inte_t, steps, lockin_run):
        bias_start = self.tcp.unit_cvt(bias_start)
        bias_end = self.tcp.unit_cvt(bias_end)
        init_settling_t = self.tcp.unit_cvt(init_settling_t)
        settling_t = self.tcp.unit_cvt(settling_t)
        inte_t = self.tcp.unit_cvt(inte_t)

        body  = self.tcp.dtype_cvt(num_of_segs, 'int', 'bin')
        body += self.tcp.dtype_cvt(bias_start, '1dfloat', 'bin')
        body += self.tcp.dtype_cvt(bias_end, '1dfloat', 'bin')
        body += self.tcp.dtype_cvt(init_settling_t, '1dfloat', 'bin')
        body += self.tcp.dtype_cvt(settling_t, '1dfloat', 'bin')
        body += self.tcp.dtype_cvt(inte_t, '1dfloat', 'bin')
        body += self.tcp.dtype_cvt(steps, '1dint', 'bin')
        body += self.tcp.dtype_cvt(lockin_run, '1duint32', 'bin')
        header = self.tcp.header_construct('BiasSpectr.MLSValsSet', body_size = len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        mls_df = pd.DataFrame({'Number of segments': num_of_segs,
                               'Bias start (V)': bias_start,
                               'Bias end (V)': bias_end,
                               'Initial settling time (s)': init_settling_t,
                               'Settling time (s)': settling_t,
                               'Integration time (s)': inte_t,
                               'Steps': steps,
                               'Lock-in run': lockin_run},
                                 index=[0]).T
        print('\n'+
              mls_df.to_string(header=False)+
              '\n\nBias sepectroscopy line segment configuration for Multi Line Segment mode set.')
        return mls_df 
       
    def BiasSpectrMLSValsGet(self):
        header = self.tcp.header_construct('BiasSpectr.MLSValsGet', body_size = 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('int', '1dfloat32', '1dfloat32', '1dfloat32', '1dfloat32', '1dfloat32', '1dint', '1duint32')

        self.tcp.print_err(res_err)
        mls_df = pd.DataFrame({'Number of segments': res_arg[0],
                               'Bias start (V)': res_arg[1],
                               'Bias end (V)': res_arg[2],
                               'Initial settling time (s)': res_arg[3],
                               'Settling time (s)': res_arg[4],
                               'Integration time (s)': res_arg[5],
                               'Steps': res_arg[6],
                               'Lock-in run': res_arg[7]},
                                index=[0]).T
        print('\n'+
              mls_df.to_string(header=False)+
              '\n\nBias sepectroscopy line segment configuration for Multi Line Segment mode settings returned.')
        return mls_df 
######################################## Current Module #############################################
    def CurrentGet(self):
        header = self.tcp.header_construct('Current.Get', 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('float32') # for string, no need to put 'int' before 'str'

        self.tcp.print_err(res_err)
        current_df = pd.DataFrame({'Current value (A)': res_arg},
                                index=[0]).T
        print('\n'+
              current_df.to_string(header=False)+
              '\n\nCurrent value returned.')
        return current_df 

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
          
    def ZCtrlOnOffSet(self, z_ctrl_status):
        body = self.tcp.dtype_cvt(z_ctrl_status, 'uint32', 'bin')
        header = self.tcp.header_construct('ZCtrl.OnOffSet', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        z_ctrl_df = pd.DataFrame({'Z-controller status': self.tcp.bistate_cvt(z_ctrl_status)},
                                 index=[0]).T
        print('\n'+
              z_ctrl_df.to_string(header=False)+
              '\n\nZ-controller on/off set.')
        return z_ctrl_df
         
    def ZCtrlOnOffGet(self):
        header = self.tcp.header_construct('ZCtrl.OnOffGet', 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('uint32')
        print(res_arg)

        self.tcp.print_err(res_err)
        z_ctrl_df = pd.DataFrame({'Z-controller status': self.tcp.bistate_cvt(res_arg[0])},
                                 index=[0]).T
        print('\n'+
              z_ctrl_df.to_string(header=False)+
              '\n\nZ-controller on/off set.')
        return z_ctrl_df
         
    def ZCtrlSetpntSet(self, z_ctrl_sp):
        body = self.tcp.dtype_cvt(z_ctrl_sp, 'float32', 'bin')
        header = self.tcp.header_construct('ZCtrl.SetpntSet', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        z_ctrl_df = pd.DataFrame({'Z-controller setpoint (A)': self.tcp.bistate_cvt(z_ctrl_sp)},
                                 index=[0]).T
        print('\n'+
              z_ctrl_df.to_string(header=False)+
              '\n\nZ-controller on/off set.')
        return z_ctrl_df
        
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
    def TipShaperStart(self, wait_until_fin, timeout):
        timeout = int(self.tcp.unit_cvt(timeout)*1000)

        body  = self.tcp.dtype_cvt(wait_until_fin, 'uint32', 'bin')
        body += self.tcp.dtype_cvt(timeout, 'int', 'bin')
        header = self.tcp.header_construct('TipShaper.Start', body_size = len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        tipshaper_start_df = pd.DataFrame({'Wait until finished': self.tcp.bistate_cvt(wait_until_fin),
                                           'Timeout (ms)': timeout},
                                           index=[0]).T
        
        print('\n'+
              tipshaper_start_df.to_string(header=False)+
              '\n\nTip shaping done.')
        return tipshaper_start_df

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
    def LockInModOnOffSet(self):
        return

    def LockInModOnOffGet(self):
        return

    def LockInModSignalSet(self):
        return

    def LockInModSignalGet(self):
        return

    def LockInModPhasRegSet(self):
        return

    def LockInModPhasRegGet(self):
        return

    def LockInModHarmonicSet(self):
        return

    def LockInModHarmonicGet(self):
        return

    def LockInModPhasSet(self, modu_num, phase):
        body  = self.tcp.dtype_cvt(modu_num, 'int', 'bin')
        body += self.tcp.dtype_cvt(phase, 'float32', 'bin')
        header = self.tcp.header_construct('LockIn.ModPhasSet', body_size = len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        print('currently not used in our system.')
        return

    def LockInModPhasGet(self):
        return

    def LockInModAmpSet(self):
        return

    def LockInModAmpGet(self):
        return

    def LockInModPhasFreqSet(self):
        return

    def LockInModPhasFreqGet(self):
        return

    def LockInDemodSignalSet(self):
        return

    def LockInDemodSignalGet(self):
        return

    def LockInDemodHarmonicSet(self):
        return

    def LockInDemodHarmonicGet(self):
        return

    def LockInDemodHPFilterSet(self):
        return

    def LockInDemodHPFilterGet(self):
        return

    def LockInDemodLPFilterSet(self):
        return

    def LockInDemodLPFilterGet(self):
        return

    def LockInDemodPhasRegSet(self):
        return

    def LockInDemodPhasRegGet(self):
        return

    def LockInDemodPhasSet(self):
        return

    def LockInDemodPhasGet(self):
        return

    def LockInDemodSyncFilterSet(self):
        return

    def LockInDemodSyncFilterGet(self):
        return

    def LockInDemodRTSignalsSet(self):
        return

    def LockInDemodRTSignalsGet(self):
        return





tcp = tcp_ctrl()
ccc = nanonis_ctrl(tcp)
# ccc.help()
# ccc.BiasSet('700m')
# ccc.BiasGet()
# ccc.BiasPulse('600m', '7')
# ccc.BiasSpectrOpen()
# ccc.BiasSpectrStart(1, 'drfue')
# df = ccc.BiasSpectrTimingGet()
# print(np.sqrt(df.T['Z averaging time (s):']))
# ccc.BiasSpectrPropsSet(0, 1, 0, 101, '5n', 0)
ccc.ZCtrlOnOffSet(1)
# bias_start = tcp.unit_cvt([1e-9,2,89.8e-9])
# ccc.TipShaperStart(1, 0.3)