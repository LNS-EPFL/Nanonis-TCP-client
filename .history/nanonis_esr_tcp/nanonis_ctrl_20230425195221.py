# -*- encoding: utf-8 -*-
'''
@Time    :   2023/03/04 01:54:34
@Author  :   Shixuan Shan 
'''
import pandas as pd
import numpy as np

class nanonis_ctrl:
    def __init__(self, tcp):
        self.tcp = tcp

# it is recommended to construct body first so that you don't need to calculate the body size by yourself
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
        bias_df = pd.DataFrame({'Bias (V)': bias},
                                index=[0]).T
        print('\n'+
              bias_df.to_string(header=False)+
              '\n\nBias set.')
        return bias_df 

    def BiasGet(self):
        header = self.tcp.header_construct('Bias.Get', body_size=0) # the body size here is the body size of Bias.Get argument 

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('float32')

        self.tcp.print_err(res_err)
        bias_df = pd.DataFrame({'Bias (V)': res_arg[0]},
                                index=[0]).T
        print('\n'+
              bias_df.to_string(header=False)+
              '\n\nBias returned.')
        return bias_df 
    
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
        bias_pulse_df = pd.DataFrame({'Wait until done': self.tcp.bistate_cvt(wait_until_done),
                                      'Bias pulse width (s)': bias_pulse_width,
                                      'Bias value (V)': bias_value,
                                      'Z-Controller on hold': self.tcp.tristate_cvt(zctrl_on_hold),
                                      'Pulse absolute/relative': pulse_abs_rel
                                       },
                                index=[0]).T
        print('\n'+
              bias_pulse_df.to_string(header=False)+
              '\n\nBias pulse set.')
        return bias_pulse_df 

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
        body += self.tcp.dtype_cvt(num_pts, 'int', 'bin')
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
        body += self.tcp.dtype_cvt(ttl_polarity, 'uint16', 'bin')
        body += self.tcp.dtype_cvt(t_2_on, 'float32', 'bin')
        body += self.tcp.dtype_cvt(on_duration, 'float32', 'bin')
        header = self.tcp.header_construct('BiasSpectr.TTLSyncSet', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        ttl_df = pd.DataFrame({'Enable': self.tcp.tristate_cvt(enable),
                               'TTL line': ttl_line,
                               'TTL polarity': ttl_polarity,
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
        _, res_arg, res_err = self.tcp.res_recv('int', 'str') # for string, no need to put 'int' before 'str'

        self.tcp.print_err(res_err)
        mls_mode_df = pd.DataFrame({'Sweep mode': res_arg[1]},
                                index=[0]).T
        print('\n'+
              mls_mode_df.to_string(header=False)+
              '\n\nLock-In per Segment flag in Multi line segment editor settings returned.')
        return mls_mode_df 
    
    def BiasSpectrMLSValsSet(self, num_segs, bias_start, bias_end, init_settling_t, settling_t, inte_t, steps, lockin_run):
        bias_start = self.tcp.unit_cvt(bias_start)
        bias_end = self.tcp.unit_cvt(bias_end)
        init_settling_t = self.tcp.unit_cvt(init_settling_t)
        settling_t = self.tcp.unit_cvt(settling_t)
        inte_t = self.tcp.unit_cvt(inte_t)

        body  = self.tcp.dtype_cvt(num_segs, 'int', 'bin')
        body += self.tcp.dtype_cvt(bias_start, '1dfloat32', 'bin')
        body += self.tcp.dtype_cvt(bias_end, '1dfloat32', 'bin')
        body += self.tcp.dtype_cvt(init_settling_t, '1dfloat32', 'bin')
        body += self.tcp.dtype_cvt(settling_t, '1dfloat32', 'bin')
        body += self.tcp.dtype_cvt(inte_t, '1dfloat32', 'bin')
        body += self.tcp.dtype_cvt(steps, '1dint', 'bin')
        body += self.tcp.dtype_cvt(lockin_run, '1duint32', 'bin')
        header = self.tcp.header_construct('BiasSpectr.MLSValsSet', body_size = len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        mls_df = pd.DataFrame({'Number of segments': num_segs,
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
        _, res_arg, res_err = self.tcp.res_recv('float32') 

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
        header = self.tcp.header_construct('Current.CalibrGet', 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('float64', 'float64')
        self.tcp.print_err(res_err)
        at_props_df = pd.DataFrame({'Calibration': res_arg[0],
                                    'Offset': res_arg[1]},
                                 index=[0]).T
        print('\n'+
              at_props_df.to_string(header=False)+
              '\n\nCalibration and offset of the selected gain returned.')
        return at_props_df

######################################## Z-controller Module #############################################
    def ZCtrlZPosSet(self, z_pos):
        z_pos = self.tcp.unit_cvt(z_pos)

        body = self.tcp.dtype_cvt(z_pos, 'float32', 'bin')
        header = self.tcp.header_construct('ZCtrl.ZPosSet', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        z_pos_df = pd.DataFrame({'Z position of the tip (m)': z_pos},
                                 index=[0]).T
        print('\n'+
              z_pos_df.to_string(header=False)+
              '\n\nZ position of the tip set. Note: to change the Z-position of the tip, the Z-controller must be switched OFF!!!')
        return z_pos_df
          
    def ZCtrlZPosGet(self):
        header = self.tcp.header_construct('ZCtrl.ZPosGet', 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('float32')
        print(res_arg)

        self.tcp.print_err(res_err)
        z_pos_df = pd.DataFrame({'Z position of the tip (m)': res_arg[0]},
                                 index=[0]).T
        print('\n'+
              z_pos_df.to_string(header=False)+
              '\n\nZ position of the tip returned.')
        return z_pos_df
         
          
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
        z_ctrl_sp = self.tcp.unit_cvt(z_ctrl_sp)

        body = self.tcp.dtype_cvt(z_ctrl_sp, 'float32', 'bin')
        header = self.tcp.header_construct('ZCtrl.SetpntSet', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        z_ctrl_sp_df = pd.DataFrame({'Z-controller setpoint (A)': z_ctrl_sp},
                                 index=[0]).T
        print('\n'+
              z_ctrl_sp_df.to_string(header=False)+
              '\n\nZ-controller setpoint set.')
        return z_ctrl_sp_df
        
    def ZCtrlSetpntGet(self):
        header = self.tcp.header_construct('ZCtrl.SetpntGet', 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('float32')

        self.tcp.print_err(res_err)
        z_ctrl_sp_df = pd.DataFrame({'Z-controller setpoint (A)': res_arg[0]},
                                 index=[0]).T
        print('\n'+
              z_ctrl_sp_df.to_string(header=False)+
              '\n\nZ-controller setpoint returned.')
        return z_ctrl_sp_df
        
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
    def ScanAction(self, scan_act, scan_dir):
        body  = self.tcp.dtype_cvt(scan_act, 'uint16', 'bin')
        body += self.tcp.dtype_cvt(scan_dir, 'uint32', 'bin')
        header = self.tcp.header_construct('Scan.Action', body_size = len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        scan_act_df = pd.DataFrame({'Scan action': scan_act,
                                    'Scan direction': scan_dir},
                                    index=[0]).T
        
        print('\n'+
              scan_act_df.to_string(header=False)+
              '\n\nScan action set.')
        return scan_act_df
    
    def ScanStatusGet(self):
        header = self.tcp.header_construct('Scan.StatusGet', body_size = 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('uint32')

        self.tcp.print_err(res_err)
        scan_status_df = pd.DataFrame({'Scan status': res_arg[0]},
                                        index=[0]).T
        
        print('\n'+
              scan_status_df.to_string(header=False)+
              '\n\nScan status returned.')
        return scan_status_df
    
    def ScanWaitEndOfScan(self, timeout):
        body  = self.tcp.dtype_cvt(timeout, 'int', 'bin')
        header = self.tcp.header_construct('Scan.WaitEndOfScan', body_size = len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, res_arg, res_err = self.tcp.res_recv('uint32', 'uint32', 'str')

        self.tcp.print_err(res_err)
        wait_scan_df = pd.DataFrame({'Timeout status': res_arg[0],
                                     'file_path': res_arg[2]},
                                        index=[0]).T
        
        print('\n'+
              wait_scan_df.to_string(header=False)+
              '\n\nScan status returned.')
        return wait_scan_df    
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

    def TipShaperPropsSet(self, switch_off_delay, change_bias, bias, tip_lift, lift_t1, bias_lift, bias_settling_t, lift_h, lift_t2, end_wait_t, restore_feedback):
        switch_off_delay = self.tcp.unit_cvt(switch_off_delay)
        bias = self.tcp.unit_cvt(bias)
        tip_lift = self.tcp.unit_cvt(tip_lift)
        lift_t1 = self.tcp.unit_cvt(lift_t1)
        bias_lift = self.tcp.unit_cvt(bias_lift)
        bias_settling_t = self.tcp.unit_cvt(bias_settling_t)
        lift_h = self.tcp.unit_cvt(lift_h)
        lift_t2 = self.tcp.unit_cvt(lift_t2)
        end_wait_t = self.tcp.unit_cvt(end_wait_t)

        body  = self.tcp.dtype_cvt(switch_off_delay, 'float32', 'bin')
        body += self.tcp.dtype_cvt(change_bias, 'uint32', 'bin')
        body += self.tcp.dtype_cvt(bias, 'float32', 'bin')
        body += self.tcp.dtype_cvt(tip_lift, 'float32', 'bin')
        body += self.tcp.dtype_cvt(lift_t1, 'float32', 'bin')
        body += self.tcp.dtype_cvt(bias_lift, 'float32', 'bin')
        body += self.tcp.dtype_cvt(bias_settling_t, 'float32', 'bin')
        body += self.tcp.dtype_cvt(lift_h, 'float32', 'bin')
        body += self.tcp.dtype_cvt(lift_t2, 'float32', 'bin')
        body += self.tcp.dtype_cvt(end_wait_t, 'float32', 'bin')
        body += self.tcp.dtype_cvt(restore_feedback, 'uint32', 'bin')
        header = self.tcp.header_construct('TipShaper.PropsSet', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        tip_shaper_props_df = pd.DataFrame({'Switch off delay (s)': switch_off_delay,
                                            'Change bias': self.tcp.tristate_cvt(change_bias),
                                            'Bias (V)': bias,
                                            'Tip lift (m)': tip_lift,
                                            'Lift time 1 (s)': lift_t1,
                                            'Bias lift (V)': bias_lift,
                                            'Bias settling time (s)': bias_settling_t,
                                            'Lift height (m)': lift_h,
                                            'Lift time 2 (s)': lift_t2,
                                            'End wait time (s)': end_wait_t,
                                            'Restore feedback': self.tcp.tristate_cvt(restore_feedback),
                                            },
                                 index=[0]).T
        print('\n'+
              tip_shaper_props_df.to_string(header=False)+
              '\n\nTip shaper procedure set.')
        return tip_shaper_props_df

    def TipShaperPropsGet(self):
        header = self.tcp.header_construct('TipShaper.PropsGet', 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('float32', 'uint32', 'float32', 'float32', 'float32', 'float32', 'float32', 'float32', 'float32', 'float32', 'uint32')

        self.tcp.print_err(res_err)
        tip_shaper_props_df = pd.DataFrame({'Switch off delay (s)': res_arg[0],
                                            'Change bias': self.tcp.tristate_cvt(res_arg[1]),
                                            'Bias (V)': res_arg[2],
                                            'Tip lift (m)': res_arg[3],
                                            'Lift time 1 (s)': res_arg[4],
                                            'Bias lift (V)': res_arg[5],
                                            'Bias settling time (s)': res_arg[6],
                                            'Lift height (m)': res_arg[7],
                                            'Lift time 2 (s)': res_arg[8],
                                            'End wait time (s)': res_arg[9],
                                            'Restore feedback': self.tcp.tristate_cvt(res_arg[10]),
                                            },
                                 index=[0]).T
        print('\n'+
              tip_shaper_props_df.to_string(header=False)+
              '\n\nTip shaper procedure returned.')
        return tip_shaper_props_df

######################################## Generic Sweeper Module #############################################
    def GenSwpAcqChsSet(self, num_chs, ch_idx):
        body  = self.tcp.dtype_cvt(num_chs, 'int', 'bin')
        body += self.tcp.dtype_cvt(ch_idx, '1dint', 'bin')
        header = self.tcp.header_construct('GenSwp.AcqChsSet', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        gen_swp_chs_df = pd.DataFrame({'Number of channels': num_chs,
                                 'Channel indexes': ch_idx},
                                 index=[0]).T
        print('\n'+
              gen_swp_chs_df.to_string(header=False)+
              '\n\nThe recorded channels of the Generic Sweeper set.')
        return gen_swp_chs_df

    def GenSwpAcqChsGet(self):
        header = self.tcp.header_construct('GenSwp.AcqChsGet', 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('int', '1dint')

        self.tcp.print_err(res_err)
        gen_swp_chs_df = pd.DataFrame({'Number of channels': res_arg[0],
                                 'Channel indexes': res_arg[1]},
                                 index=[0]).T
        print('\n'+
              gen_swp_chs_df.to_string(header=False)+
              '\n\nThe recorded channels of the Generic Sweeper returned.')
        return gen_swp_chs_df
    
    def GenSwpSwpSignalSet(self, swp_ch_name_size, swp_ch_name):
        body  = self.tcp.dtype_cvt(swp_ch_name_size, 'int', 'bin')
        body += self.tcp.dtype_cvt(swp_ch_name, 'str', 'bin')
        header = self.tcp.header_construct('GenSwp.SwpSignalSet', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        gen_swp_sgn_df = pd.DataFrame({'Sweep channel name size': swp_ch_name_size,
                                 'Sweep channel name': swp_ch_name},
                                 index=[0]).T
        print('\n'+
              gen_swp_sgn_df.to_string(header=False)+
              '\n\nThe recorded channels of the Generic Sweeper set.')
        return gen_swp_sgn_df

    def GenSwpSwpSignalGet(self):
        header = self.tcp.header_construct('GenSwp.SwpSignalGet', 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('int', 'str', 'int', 'int', '1dstr')

        print(res_arg[1])
        self.tcp.print_err(res_err)
        gen_swp_sgn_df = pd.DataFrame({'Sweep channel name': res_arg[1], 'Channel names': res_arg[4]},
                                 index=[0]).T
        print('\n'+
              gen_swp_sgn_df.to_string(header=False)+
              '\n\nThe recorded channels of the Generic Sweeper returned.')
        return gen_swp_sgn_df
    
    def GenSwpLimitsSet(self, lo_lmt, up_lmt):
        lo_lmt = self.tcp.unit_cvt(lo_lmt)
        up_lmt = self.tcp.unit_cvt(up_lmt)

        body  = self.tcp.dtype_cvt(lo_lmt, 'float32', 'bin')
        body += self.tcp.dtype_cvt(up_lmt, 'float32', 'bin')
        header = self.tcp.header_construct('GenSwp.LimitsSet', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        gen_swp_lmt_df = pd.DataFrame({'Lower limit': lo_lmt,
                                       'Upper limit': up_lmt},
                                       index=[0]).T
        print('\n'+
              gen_swp_lmt_df.to_string(header=False)+
              '\n\nThe limits of the Sweep signals set.')
        return gen_swp_lmt_df

    def GenSwpLimitsGet(self):
        header = self.tcp.header_construct('GenSwp.LimitsGet', 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('float32', 'float32')

        self.tcp.print_err(res_err)
        gen_swp_lmt_df = pd.DataFrame({'Lower limit': res_arg[0],
                                       'Upper limit': res_arg[1]},
                                       index=[0]).T
        print('\n'+
              gen_swp_lmt_df.to_string(header=False)+
              '\n\nThe limits of the Sweep signals returned.')
        return gen_swp_lmt_df

    # ! -1=no change, 0=Off, 1=On different from other functions!!!
    def GenSwpPropsSet(self, init_settling_t, max_slew_rate, num_steps, periods, autosave, save_dialog, settling_t):
        init_settling_t = self.tcp.unit_cvt(init_settling_t)*1000
        periods = int(self.tcp.unit_cvt(periods)*1000)
        settling_t = self.tcp.unit_cvt(settling_t)*1000

        body  = self.tcp.dtype_cvt(init_settling_t, 'float32', 'bin')
        body += self.tcp.dtype_cvt(max_slew_rate, 'float32', 'bin')
        body += self.tcp.dtype_cvt(num_steps, 'int', 'bin') #* 0 means no change
        body += self.tcp.dtype_cvt(periods, 'uint16', 'bin') #* 0 means no change
        body += self.tcp.dtype_cvt(autosave, 'int', 'bin')
        body += self.tcp.dtype_cvt(save_dialog, 'int', 'bin')
        body += self.tcp.dtype_cvt(settling_t, 'float32', 'bin')
        header = self.tcp.header_construct('GenSwp.PropsSet', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        gen_swp_props_df = pd.DataFrame({'Initial Settling time (ms)': init_settling_t,
                                         'Maximum slew rate (units/s)': max_slew_rate,
                                         'Number of steps': num_steps, 
                                         'Period (ms)': periods, 
                                         'Autosave': self.tcp.tristate_cvt_2(autosave), 
                                         'Save dialog box': self.tcp.tristate_cvt_2(save_dialog),
                                         'Settling time (ms)': settling_t},
                                        index=[0]).T
        
        print('\n'+
              gen_swp_props_df.to_string(header=False)+
              '\n\nGeneric sweeper parameters set.')
        return gen_swp_props_df

    def GenSwpPropsGet(self):
        header = self.tcp.header_construct('GenSwp.PropsGet', 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('float32', 'float32', 'int', 'uint16', 'uint32', 'uint32', 'float32')

        self.tcp.print_err(res_err)
        gen_swp_props_df = pd.DataFrame({'Initial Settling time (ms)': res_arg[0],
                                         'Maximum slew rate (units/s)': res_arg[1],
                                         'Number of steps': res_arg[2], 
                                         'Period (ms)': res_arg[3], 
                                         'Autosave': self.tcp.bistate_cvt(res_arg[4]), 
                                         'Save dialog box': self.tcp.bistate_cvt(res_arg[5]),
                                         'Settling time (ms)': res_arg[6]},
                                 index=[0]).T
        print('\n'+
              gen_swp_props_df.to_string(header=False)+
              '\n\nGeneric sweeper parameters returned.')
        return gen_swp_props_df

    def GenSwpStart(self, get_data, sweep_dir, save_base_name, reset_signal):
        save_base_name_str_size = len(save_base_name)

        body  = self.tcp.dtype_cvt(get_data, 'uint32', 'bin')
        body += self.tcp.dtype_cvt(sweep_dir, 'uint32', 'bin')
        body += self.tcp.dtype_cvt(save_base_name_str_size, 'int', 'bin')
        body += self.tcp.dtype_cvt(save_base_name, 'str', 'bin')
        body += self.tcp.dtype_cvt(reset_signal, 'uint32', 'bin')
        header = self.tcp.header_construct('GenSwp.Start', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, res_arg, res_err = self.tcp.res_recv('int', 'int', '1dstr', 'int', 'int', 'int', '2dfloat32')

        self.tcp.print_err(res_err)
        gen_swp_df = pd.DataFrame(res_arg[5].T, columns = res_arg[2][0])

        gen_swp_param_df = pd.DataFrame({'Get data': self.tcp.bistate_cvt(get_data),
                                         'Sweep direction': sweep_dir,
                                         'Save base name string size': save_base_name_str_size,
                                         'Save base name string': save_base_name,
                                         'Reset signal': self.tcp.bistate_cvt(reset_signal), 
                                         'Channels names size': res_arg[0],
                                         'Number of channels': res_arg[1],
                                         'Channels names': res_arg[2],
                                         'Number of rows': res_arg[3],
                                         'Number of columns': res_arg[4]},
                                        index=[0]).T
        print(gen_swp_df)
        print('\n\n'+
              gen_swp_param_df.to_string(header=False)+
              '\n\nGeneric sweep done!')
        return gen_swp_df, gen_swp_param_df

    def GenSwpStop(self):
        header = self.tcp.header_construct('GenSwp.Stop', 0)

        self.tcp.cmd_send(header)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)

        print('\n'+
              '\n\nGeneric sweeper stopped.')
        return 

    def GenSwpOpen(self):
        header = self.tcp.header_construct('GenSwp.Open', 0)

        self.tcp.cmd_send(header)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)

        print('\n'+
              '\n\nGeneric sweep module opened.')
        return 

######################################## Atom Tracking Module #############################################
    def AtomTrackCtrlSet(self, at_ctrl, status): #Modulation: 0; Controller: 1; Drift measurement:2
        body  = self.tcp.dtype_cvt(at_ctrl, 'uint16', 'bin')
        body += self.tcp.dtype_cvt(status,'uint16', 'bin')
        header = self.tcp.header_construct('AtomTrack.CtrlSet', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        at_ctrl_df = pd.DataFrame({'Modulation=0 Controller=1 Drift measurement=2': None,
                                   'Atom tracking control': at_ctrl,
                                   'Status': self.tcp.bistate_cvt(status)},
                                   index=[0]).T
        print('\n'+
              at_ctrl_df.to_string(header=False)+
              '\n\nAtom tracking control set.')
        return at_ctrl_df

    def AtomTrackStatusGet(self, at_ctrl):
        body  = self.tcp.dtype_cvt(at_ctrl, 'uint16', 'bin')
        header = self.tcp.header_construct('AtomTrack.CtrlGet', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, res_arg, res_err = self.tcp.res_recv('uint16')

        self.tcp.print_err(res_err)
        at_ctrl_df = pd.DataFrame({'Modulation=0 Controller=1 Drift measurement=2': None,
                                   'Atom tracking control': at_ctrl,
                                   'Status': self.tcp.bistate_cvt(res_arg[0])},
                                   index=[0]).T
        print('\n'+
              at_ctrl_df.to_string(header=False)+
              '\n\nAtom tracking control status returned.')
        return at_ctrl_df

    def AtomTrackPropsSet(self, inte_gain, freq, ampl, phase, switch_off_delay):
        inte_gain = self.tcp.unit_cvt(inte_gain)
        freq = self.tcp.unit_cvt(freq)
        ampl = self.tcp.unit_cvt(ampl)
        switch_off_delay= self.tcp.unit_cvt(switch_off_delay)

        body  = self.tcp.dtype_cvt(inte_gain, 'float32', 'bin')
        body += self.tcp.dtype_cvt(freq, 'float32', 'bin')
        body += self.tcp.dtype_cvt(ampl, 'float32', 'bin')
        body += self.tcp.dtype_cvt(phase, 'float32', 'bin')
        body += self.tcp.dtype_cvt(switch_off_delay, 'float32', 'bin')
        header = self.tcp.header_construct('AtomTrack.PropsSet', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()
        self.tcp.print_err(res_err)
        at_props_df = pd.DataFrame({'Integral gain (m/(m/m.s))': inte_gain,
                                    'Frequency (Hz)': freq,
                                    'Amplitude (m)': ampl,
                                    'Phase (deg)': phase,
                                    'Switch off delay (s)': switch_off_delay,
                                    },
                                 index=[0]).T
        print('\n'+
              at_props_df.to_string(header=False)+
              '\n\nAtom track parameters set.')
        return at_props_df

    def AtomTrackPropsGet(self):
        header = self.tcp.header_construct('AtomTrack.PropsGet', 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('float32', 'float32', 'float32', 'float32', 'float32')
        self.tcp.print_err(res_err)
        at_props_df = pd.DataFrame({'Integral gain (m/(m/m.s))': res_arg[0],
                                    'Frequency (Hz)': res_arg[1],
                                    'Amplitude (m)': res_arg[2],
                                    'Phase (deg)': res_arg[3],
                                    'Switch off delay (s)': res_arg[4],
                                    },
                                 index=[0]).T
        print('\n'+
              at_props_df.to_string(header=False)+
              '\n\nAtom track parameters returned.')
        return at_props_df

    def AtomTrackQuickCompStart(self):
        return

    def AtomTrackDriftComp(self):
        return

######################################## Lock-in Module #############################################
    def LockInModOnOffSet(self, modu_num, lockin_onoff):
        body  = self.tcp.dtype_cvt(modu_num, 'int', 'bin')
        body += self.tcp.dtype_cvt(lockin_onoff, 'uint32', 'bin')
        header = self.tcp.header_construct('LockIn.ModOnOffSet', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        lockin_onoff_df = pd.DataFrame({'Modulator number': modu_num,
                                        'Lock-in on/off': self.tcp.bistate_cvt(lockin_onoff)},
                                        index=[0]).T
        
        print('\n'+
              lockin_onoff_df.to_string(header=False)+
              '\n\nLock-in modulator status set.')
        return lockin_onoff_df

    def LockInModOnOffGet(self, modu_num):
        body  = self.tcp.dtype_cvt(modu_num, 'int', 'bin')
        header = self.tcp.header_construct('LockIn.ModOnOffGet', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, res_arg, res_err = self.tcp.res_recv('uint32')

        self.tcp.print_err(res_err)
        lockin_onoff_df = pd.DataFrame({'Modulator number': modu_num,
                                        'Lock-in on/off': self.tcp.bistate_cvt(res_arg[0])},
                                        index=[0]).T
        
        print('\n'+
              lockin_onoff_df.to_string(header=False)+
              '\n\nLock-in modulator status returned.')
        return lockin_onoff_df

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

    def LockInModAmpSet(self, modu_num, ampl):
        ampl = self.tcp.unit_cvt(ampl)

        body  = self.tcp.dtype_cvt(modu_num, 'int', 'bin')
        body += self.tcp.dtype_cvt(ampl, 'float32', 'bin')
        header = self.tcp.header_construct('LockIn.ModAmpSet', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        lockin_amp_df = pd.DataFrame({'Modulator number': modu_num,
                                      'Amplitude': ampl},
                                      index=[0]).T
        
        print('\n'+
              lockin_amp_df.to_string(header=False)+
              '\n\nLock-in modulator amplitude set.')
        return lockin_amp_df

    def LockInModAmpGet(self, modu_num):
        body  = self.tcp.dtype_cvt(modu_num, 'int', 'bin')
        header = self.tcp.header_construct('LockIn.ModAmpGet', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, res_arg, res_err = self.tcp.res_recv('float32')

        self.tcp.print_err(res_err)
        lockin_amp_df = pd.DataFrame({'Modulator number': modu_num,
                                      'Amplitude': res_arg[0]},
                                      index=[0]).T
        
        print('\n'+
              lockin_amp_df.to_string(header=False)+
              '\n\nLock-in modulator amplitude returned.')
        return lockin_amp_df

    def LockInModPhasFreqSet(self, modu_num, freq):
        freq = self.tcp.unit_cvt(freq)

        body  = self.tcp.dtype_cvt(modu_num, 'int', 'bin')
        body += self.tcp.dtype_cvt(freq, 'float64', 'bin')
        header = self.tcp.header_construct('LockIn.ModPhasFreqSet', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        lockin_freq_df = pd.DataFrame({'Modulator number': modu_num,
                                      'Frequency (Hz)': freq},
                                      index=[0]).T
        
        print('\n'+
              lockin_freq_df.to_string(header=False)+
              '\n\nLock-in modulator frequency set.')
        return lockin_freq_df

    def LockInModPhasFreqGet(self, modu_num):
        body  = self.tcp.dtype_cvt(modu_num, 'int', 'bin')
        header = self.tcp.header_construct('LockIn.ModPhasFreqGet', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, res_arg, res_err = self.tcp.res_recv('float64')

        self.tcp.print_err(res_err)
        lockin_freq_df = pd.DataFrame({'Modulator number': modu_num,
                                      'Frequency (Hz)': res_arg[0]},
                                      index=[0]).T
        
        print('\n'+
              lockin_freq_df.to_string(header=False)+
              '\n\nLock-in modulator frequency returned.')
        return lockin_freq_df

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
######################################## Signals Module #############################################
    def SignalsNamesGet(self):
        header = self.tcp.header_construct('Signals.NamesGet', 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('int', 'int', '1dstr')

        self.tcp.print_err(res_err)
        signal_name_df = pd.DataFrame({'Signal names': res_arg[2].flatten()})
        # print(res_arg[2][0])
        pd.set_option('display.max_rows', None)
        print('\n'+
              signal_name_df.to_string()+
              '\n\nSignal name list returned.')
        return signal_name_df

######################################## Utilities Module #############################################
    def UtilSessionPathGet(self):
        header = self.tcp.header_construct('Util.SessionPathGet', 0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('int', 'str')

        self.tcp.print_err(res_err)
        util_session_path_df = pd.DataFrame({'Session path': res_arg[1]},
                                       index=[0]).T
        print('\n'+
              util_session_path_df.to_string(header=False)+
              '\n\nSession folder path returned.')
        return util_session_path_df
    

    def UtilSessionPathSet(self, sess_path, save_settings_to_prev):
        sess_path_size = len(sess_path)

        body  = self.tcp.dtype_cvt(sess_path_size, 'int', 'bin')
        body += self.tcp.dtype_cvt(sess_path, 'str', 'bin')
        body += self.tcp.dtype_cvt(save_settings_to_prev, 'uint32', 'bin')
        header = self.tcp.header_construct('Util.SessionPathSet', len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        util_session_path_df = pd.DataFrame({'Session path': sess_path,
                                             'Save settings to previous': self.tcp.bistate_cvt(save_settings_to_prev)}, 
                                             index=[0]).T
        
        print('\n'+
              util_session_path_df.to_string(header=False)+
              '\n\nSession folder path set.')
        return util_session_path_df
    

    def UtilSettingsLoad(self):

        return

    def UtilSettingsSave(self):

        return

    def UtilLayoutLoad(self):

        return

    def UtilLayoutSave(self):

        return

    def UtilLock(self):

        return

    def UtilUnLock(self):

        return

    def UtilRTFreqSet(self):

        return

    def UtilRTFreqGet(self):

        return

    def UtilAcqPeriodSet(self):

        return

    def UtilAcqPeriodGet(self):

        return

    def UtilRTOversamplSet(self):

        return

    def UtilRTOversamplGet(self):

        return

    def UtilQuit(self):

        return
