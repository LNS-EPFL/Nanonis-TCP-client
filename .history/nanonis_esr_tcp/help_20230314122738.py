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
        print('Bias.Set\
              \n Sets the Bias voltage to the specified value.\
              \n Arguments:\
              \n - Bias value (V) (float32)\
              \n Return arguments (if Send response back flag is set to True when sending request message):\
              \n - Error described in the Response message>Body section')

    def BiasGet(self):
        print('Bias.Get\
              \n Returns the Bias voltage value.\
              \n Arguments: None\
              \n Return arguments (if Send response back flag is set to True when sending request message):\
              \n - Bias value (V) (float32)\
              \n - Error described in the Response message>Body section')
    
    def BiasPulse(self):
        print("Bias.Pulse\
              \nGenerates one bias pulse\
              \nArguments:\
              \n- Wait until done (unsigned int32), if True, this function will wait until the pulse has finished. 1=True and 0=False\
              \n- Bias pulse width (s) (float32) is the pulse duration in seconds\
              \n- Bias value (V) (float32) is the bias value applied during the pulse\
              \n- Z-Controller on hold (unsigned int16) sets whether the controller is set to hold (deactivated) during the pulse. Possible values are: 0=no change, 1=hold, 2=don't hold\
              \n- Pulse absolute/relative (unsigned int16) sets whether the bias value argument is an absolute value or relative to the current bias voltage. Possible values are: 0=no change, 1=relative, 2=absolute\
              \nReturn arguments (if Send response back flag is set to True when sending request message):\
              \n- Error described in the Response message>Body section")
    
    def BiasSpectrOpen(self):
        print('BiasSpectr.Open\
              \n Opens the Bias Spectroscopy module.\
              \n Arguments:\
              \n Return arguments (if Send response back flag is set to True when sending request message):\
              \n - Error described in the Response message>Body section')
    
    def BiasSpectrStart(self):
        print('BiasSpectr.Start\
            \nStarts a bias spectroscopy in the Bias Spectroscopy module.\
            \nBefore using this function, select the channels to record in the Bias Spectroscopy module.\
            \nArguments:\
            \n- Get data (unsigned int32) defines if the function returns the spectroscopy data (1=True) or not (0=False)\
            \n- Save base name string size (int) defines the number of characters of the Save base name string\
            \n- Save base name (string) is the basename used by the saved files. If empty string, there is no change\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Channels names size (int) is the size in bytes of the Channels names string array\
            \n- Number of channels (int) is the number of elements of the Channels names string array\
            \n- Channels names (1D array string) returns the list of channels names. The size of each string item comes right before it as integer 32\
            \n- Data rows (int) defines the number of rows of the Data array\
            \n- Data columns (int) defines the number of columns of the Data array\
            \n- Data (2D array float32) returns the spectroscopy data\
            \n- Number of parameters (int) is the number of elements of the Parameters array\
            \n- Parameters (1D array float32) returns the list of fixed parameters and parameters (in that order). To see the names of the returned parameters, use the BiasSpectr.PropsGet function.\
            \n- Error described in the Response message>Body section')
 
    def BiasSpectrStop(self):
        print('BiasSpectr.Stop\
              \nStops the current Bias Spectroscopy measurement.\
              \nArguments:\
              \nReturn arguments (if Send response back flag is set to True when sending request message):\
              \n- Error described in the Response message>Body section')
    
    def BiasSpectrStatusGet(self):
        print('BiasSpectr.StatusGet\
            \nReturns the status of the Bias Spectroscopy measurement.\
            \nArguments:\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Status (unsigned int32) where 0=not running and 1=running\
            \n- Error described in the Response message>Body section')
    
    def BiasSpectrChsSet(self):
        print('BiasSpectr.ChsSet\
            \nSets the list of recorded channels in Bias Spectroscopy.\
            \nArguments:\
            \n- Number of channels (int) is the number of recorded channels. It defines the size of         the Channel indexes array\
            \n- Channel indexes (1D array int) are the indexes of recorded channels. The index is comprised between 0 and 127, and it corresponds to the full list of signals available in    the system.\
            \nTo get the signal name and its corresponding index in the list of the 128 available signals in the Nanonis Controller, use the Signal.NamesGet function, or check the RT Idx value in the Signals Manager module.\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')
    
    def BiasSpectrChsGet(self):
        print('BiasSpectr.ChsGet\
            \nReturns the list of recorded channels in Bias Spectroscopy.\
            \nArguments:\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Number of channels (int) is the number of recorded channels. It defines the size of the Channel indexes array\
            \n- Channel indexes (1D array int) are the indexes of recorded channels. The index is comprised between 0 and 127, and it corresponds to the full list of signals available in the system.\
            \nTo get the signal name and its corresponding index in the list of the 128 available signals in the Nanonis Controller, use the Signal.NamesGet function, or check the RT Idx value in the Signals Manager module.\
            \n- Error described in the Response message>Body section)')
    
    def BiasSpectrPropsSet(self):
        print('BiasSpectr.PropsSet\
            \nConfigures the Bias Spectroscopy parameters.\
            \nArguments:\
            \n- Save all (unsigned int16) where 0 means no change, 1 means that the data from the individual sweeps is saved along with the average data of all of them, and 2 means that the individual sweeps are not saved in the file. This parameter only makes sense when multiple sweeps are configured\
            \n- Number of sweeps (int) is the number of sweeps to measure and average. 0 means no change with respect to the current selection\
            \n- Backward sweep (unsigned int16) selects whether to also acquire a backward sweep (forward is always measured) when it is 1. When it is 2 means that no backward sweep is performed, and 0 means no change.\
            \n- Number of points (int) defines the number of points to acquire over the sweep range, where 0 means no change\
            \n- Z offset (m) (float32) defines which distance to move the tip before starting the spectroscopy measurement. Positive value means retracting, negative value approaching\
            \n- Autosave (unsigned int16) selects whether to automatically save the data to ASCII file once the sweep is done (=1). This flag is off when =2, and 0 means no change\
            \n- Show save dialog (unsigned int16) selects whether to show the save dialog box once the sweep is done (=1). This flag is off when =2, and 0 means no change\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')
    
    def BiasSpectrPropsGet(self):
        print('BiasSpectr.PropsGet\
            \nReturns the Bias Spectroscopy parameters.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Save all (unsigned int16) where 1 means that the data from the individual sweeps is saved along with the average data of all of them, and 0 means that the individual sweeps are not saved in the file. This parameter only makes sense when multiple sweeps are configured\
            \n- Number of sweeps (int) is the number of sweeps to measure and average\
            \n- Backward sweep (unsigned int16), where 1 means that the backward sweep is performed (forward is always measured) and 0 means that there is no backward sweep\
            \n- Number of points (int) is the number of points to acquire over the sweep range\
            \n- Channels size (int) is the size in bytes of the Channels string array\
            \n- Number of channels (int) is the number of elements of the Channels string array\
            \n- Channels (1D array string) returns the names of the acquired channels in the sweep. The size of each string item comes right before it as integer 32\
            \n- Parameters size (int) is the size in bytes of the Parameters string array\
            \n- Number of parameters (int) is the number of elements of the Parameters string array\
            \n- Parameters (1D array string) returns the parameters of the sweep. The size of each string item comes right before it as integer 32\
            \n- Fixed parameters size (int) is the size in bytes of the Fixed parameters string array\
            \n- Number of fixed parameters (int) is the number of elements of the Fixed parameters string array\
            \n- Fixed parameters (1D array string) returns the fixed parameters of the sweep. The size of each string item comes right before it as integer 32\
            \n- Error described in the Response message>Body section')
    
    def BiasSpectrAdvPropsSet(self):
        print('BiasSpectr.AdvPropsSet\
            \nSets parameters from the Advanced configuration section of the bias spectroscopy module.\
            \nArguments:\
            \n- Reset Bias (unsigned int16) sets whether Bias voltage returns to the initial value at the end of the spectroscopy measurement. 0 means no change, 1 means On, and 2 means Off\
            \n- Z-Controller Hold (unsigned int16) sets the Z-Controller on hold during the sweep. 0 means no change, 1 means On, and 2 means Off\
            \n- Record final Z (unsigned int16) records the Z position during Z averaging time at the end of the sweep and stores the average value in the header of the file when saving. 0 means no change, 1 means On, and 2 means Off\
            \n- Lockin Run (unsigned int16) sets the Lock-In to run during the measurement.\
            \nWhen using this feature, make sure the Lock-In is configured correctly and settling times are set to twice the Lock-In period at least. This option is ignored when Lock-In is already running.\
            \nThis option is disabled if the Sweep Mode is MLS and the flag to configure the Lock-In per segment in the Multiline segment editor is set. 0 means no change, 1 means On, and 2 means Off\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')
    
    def BiasSpectrAdvPropsGet(self):
        print('BiasSpectr.AdvPropsGet\
            \nReturns the parameters from the Advanced configuration section of the bias spectroscopy module.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Reset Bias (unsigned int16) indicates whether Bias voltage returns to the initial value at the end of the spectroscopy measurement. 0 means Off, 1 means On\
            \n- Z-Controller Hold (unsigned int16) indicates if the Z-Controller is on hold during the sweep. 0 means Off, 1 means On\
            \n- Record final Z (unsigned int16) indicates whether to record the Z position during Z averaging time at the end of the sweep and store the average value in the header of the file when saving. 0 means Off, 1 means On\
            \n- Lockin Run (unsigned int16) indicates if the Lock-In to runs during the measurement. This option is ignored when Lock-In is already running. This option is disabled if the Sweep Mode is MLS and the flag to configure the Lock-In per segment in the Multiline segment editor is set. 0 means Off, 1 means On\
            \n- Error described in the Response message>Body section')
    
    def BiasSpectrLimitsSet(self):
        print('BiasSpectr.LimitsSet\
            \nSets the Bias spectroscopy limits.\
            \nArguments:\
            \n- Start value (V) (float32) is the starting value of the sweep\
            \n- End value (V) (float32) is the ending value of the sweep\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')
    
    def BiasSpectrLimitsGet(self):
        print('BiasSpectr.LimitsGet\
            \nReturns the Bias spectroscopy limits.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Start value (V) (float32) is the starting value of the sweep\
            \n- End value (V) (float32) is the ending value of the sweep\
            \n- Error described in the Response message>Body section')
    
    def BiasSpectrTimingSet(self):
        print('BiasSpectr.TimingSet\
            \nConfigures the Bias spectroscopy timing parameters.\
            \nArguments:\
            \n- Z averaging time (s) (float32)\
            \n- Z offset (m) (float32)\
            \n- Initial settling time (s) (float32)\
            \n- Maximum slew rate (V/s) (float32)\
            \n- Settling time (s) (float32)\
            \n- Integration time (s) (float32)\
            \n- End settling time (s) (float32)\
            \n- Z control time (s) (float32)\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def BiasSpectrTimingGet(self):
        print('BiasSpectr.TimingGet\
            \nReturns the Bias spectroscopy timing parameters.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Z averaging time (s) (float32)\
            \n- Z offset (m) (float32)\
            \n- Initial settling time (s) (float32)\
            \n- Maximum slew rate (V/s) (float32)\
            \n- Settling time (s) (float32)\
            \n- Integration time (s) (float32)\
            \n- End settling time (s) (float32)\
            \n- Z control time (s) (float32)\
            \n- Error described in the Response message>Body section')
    def BiasSpectrTTLSyncSet(self):
        print()
        
    def BiasSpectrTTLSyncGet(self):
        print()
        
    def BiasSpectrAltZCtrlSet(self):
        print()
        
    def BiasSpectrAltZCtrlGet(self):
        print()
        
    def BiasSpectrMLSLockinPerSegSet(self):
        print()
        
    def BiasSpectrMLSLockinPerSegGet(self):
        print()
        
    def BiasSpectrMLSModeSet(self):
        print()
        
    def BiasSpectrMLSModeGet(self):
        print()
        
    def BiasSpectrMLSValsSet(self):
        print()
        
    def BiasSpectrMLSValsGet(self):
        print()
        

help = help()    
# print(help.general_info)
help.BiasSpectrPropsSet()