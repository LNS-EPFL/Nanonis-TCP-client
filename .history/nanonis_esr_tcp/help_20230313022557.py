# -*- encoding: utf-8 -*-
'''
@Time    :   2023/03/13 00:44:06
@Author  :   Shixuan Shan 
'''

#  This is a help module if you don't know how to use the funcitons in nanonis_ctrl.py file
from nanonis_ctrl import nanonis_ctrl

class help:
    def __init__(self):
        self.general_info = "This is a help module if you don't know how to use the funcitons in nanonis_ctrl.py file \n Call help() to get a list of the function included in the module.\n Call the name of that function to get the help of that function, eg BiasSet()"        

    def help(self):
        func_list = [func for func in dir(nanonis_ctrl) if callable(getattr(nanonis_ctrl, func)) and not func.startswith("__")]
        print('All available functions:\n'+str(func_list))

        print('Here are some tips of using this Nanonis TCP module: \
              \n 1. Normally for a tristate setting, such as "save all" in "BiasSpectrPropsSet" function, there are three valid input values: \n\
              1) 0 --> No change \n\
              2) 1 --> Yes/On \n\
              3) 2 --> No/Off')

    def BiasSet(self):
        print('BiasSet(self, bias)')

    def BiasGet(self):
        print('BiasGet(self)')
    
    def BiasPulse(self):
        print('BiasPulse(self, wait_until_done, bias_pulse_width, bias_value, zctrl_on_hold, pulse_abs_rel)')
    
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
help.general_info()
