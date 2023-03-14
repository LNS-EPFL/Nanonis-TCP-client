# -*- encoding: utf-8 -*-
'''
@Time    :   2023/03/13 00:44:06
@Author  :   Shixuan Shan 
'''

#  This is a help module if you don't know how to use the funcitons in nanonis_ctrl.py file
from nanonis_ctrl import nanonis_ctrl
import pandas as pd
import numpy as np

class help:
    def __init__(self):
        self.general_info = "This is a help module if you don't know how to use the funcitons in nanonis_ctrl.py file \n Call help() to get a list of the function included in the module.\n Call the name of that function to get the help of that function, eg BiasSet()"        

    def help(self):
        func_list = [func for func in dir(nanonis_ctrl) if callable(getattr(nanonis_ctrl, func)) and not func.startswith("__")]

        print('Here are some tips of using this Nanonis TCP module: \
              \n 1. For a tristate setting, such as "save all" in "BiasSpectrPropsSet" function, there are three valid input values: \n\
              1) 0 --> No change \n\
              2) 1 --> Yes/On \n\
              3) 2 --> No/Off')
        print(f'All available {len(func_list)} functions:\n',func_list)

    def BiasSet(self):
        print('Bias.Set\nSets the Bias voltage to the specified value.\nArguments:\n- Bias value (V) (float32)\nReturn arguments (if Send response back flag is set to True when sending request message):\n- Error described in the Response message>Body section')

    def BiasGet(self):
        print('Returns the Bias voltage value.\nArguments: None\nReturn arguments (if Send response back flag is set to True when sending request message):\n- Bias value (V) (float32)\n- Error described in the Response message>Body section')
    
    def BiasPulse(self):
        print("Bias.Pulse\nGenerates one bias pulse.\
              \nArguments:\n- Wait until done (unsigned int32), if True, this function will wait until the pulse has finished. 1=True and 0=False\n- Bias pulse width (s) (float32) is the pulse duration in seconds\n- Bias value (V) (float32) is the bias value applied during the pulse\n- Z-Controller on hold (unsigned int16) sets whether the controller is set to hold (deactivated) during the pulse. Possible values are: 0=no change, 1=hold, 2=don't hold\n- Pulse absolute/relative (unsigned int16) sets whether the bias value argument is an absolute value or relative to the current bias voltage. Possible values are: 0=no change, 1=relative, 2=absolute\nReturn arguments (if Send response back flag is set to True when sending request message):\n- Error described in the Response message>Body section")
    
    def BiasSpectrOpen(self):
        print('BiasSpectrOpen(self)')
    
    def BiasSpectrStart(self):
        print('BiasSpectrStart(self, get_data, save_base_name)')
    
    def BiasSpectrStop(self):
        print('BiasSpectrStop(self)')
    
    def BiasSpectrStatusGet(self):
        print('BiasSpectrStatusGet(self):')
    
    def BiasSpectrChsSet(self):
        print('BiasSpectrChsSet(self, num_chs, ch_idx)')
    
    def BiasSpectrChsGet(self):
        print('BiasSpectrChsGet(self)')
    
    def BiasSpectrPropsSet(self):
        print('BiasSpectrPropsSet(self, save_all, num_sweeps, bw_sweep, num_pts, z_offset, auto_save, show_save_dialog)')
    
    def BiasSpectrPropsGet(self):
        print('BiasSpectrPropsGet(self)')
    
    def BiasSpectrAdvPropsSet(self):
        print('BiasSpectrAdvPropsSet(self, reset_bias, z_ctrl_hold, rec_final_z, lock_in_run)')
    
    def BiasSpectrAdvPropsGet(self):
        print('BiasSpectrAdvPropsGet(self)')
    
    def BiasSpectrLimitsSet(self):
        print('BiasSpectrLimitsSet(self, start_val, end_val)')
    
    def BiasSpectrLimitsGet(self):
        print('BiasSpectrLimitsGet(self)')
    
    def BiasSpectrTimingSet(self):
        print('BiasSpectrTimingSet(self,, z_avg_t, z_offset, init_settling_t, max_slew_rate, settling_t, int_t, end_settling_t, z_ctrl_t)')

    def BiasSpectrTimingGet(self):
        print('BiasSpectrTimingGet(self)')

help = help()    
print(help.general_info)
help.BiasPulse()