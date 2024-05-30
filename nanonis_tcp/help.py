# -*- encoding: utf-8 -*-
'''
@Time    :   2023/03/13 00:44:06
@Author  :   Shixuan Shan 
'''
from .nanonis_ctrl import *
import pandas as pd
#  This is a help module if you want to know more about how to use the funcitons in nanonis_ctrl.py file
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)

class help:
    def __init__(self):
        self.general_info = "This is a help module if you want to know more about how to use the funcitons in nanonis_ctrl module \n Call help() to get a list of the function included in the module.\n Call the name of that function to get the help of that function, eg. BiasSet()"        

    def help(self):
        func_list = [func for func in dir(nanonis_ctrl) if callable(getattr(nanonis_ctrl, func)) and not func.startswith("__")]

        columns = {}
        for ele in func_list:
            first_letter = ele[0]
            if first_letter not in columns:
                columns[first_letter] = []
            columns[first_letter].append(ele)

        df = pd.DataFrame.from_dict(columns, orient='index').T

        # print('Here are some tips of using this Nanonis TCP module: \
        #       \n 1. For a tristate setting, such as "save all" in "BiasSpectrPropsSet" function, there are two possible sets of three valid input values: \n\
        #       1) 0/-1 --> No change \n\
        #       2) 1/1 --> Yes/On \n\
        #       3) 2/0 --> No/Off')
        print(f'All available {len(func_list)} functions:\n', df)

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
    def BiasRangeSet(self):
        print('Bias.RangeSet\
            \nSets the range of the Bias voltage, if different ranges are available.\
            \nArguments:\
            \n- Bias range index (unsigned int16) is the index out of the list of ranges which can be retrieved by the\
            \nfunction Bias.RangeGet.\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def BiasRangeGet(self):
        print('Bias.RangeGet\
            \nReturns the selectable ranges of bias voltage and the index of the selected one.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Bias ranges size (int) is the size in bytes of the bias ranges array\
            \n- Number of ranges (int) is the number of elements of the bias ranges array\
            \n- Bias ranges (1D array string) returns an array of selectable bias ranges. Each element of the array is\
            \npreceded by its size in bytes\
            \n- Bias range index (unsigned int16) is the index out of the list of bias ranges.\
            \n- Error described in the Response message>Body section')

    def BiasCalibrSet(self):
        print('Bias.CalibrSet\
            \nSets the calibration and offset of bias voltage.\
            \nIf several ranges are available, this function sets the values for the selected one.\
            \nArguments:\
            \n- Calibration (float32)\
            \n- Offset (float32)\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def BiasCalibrGet(self):
        print('Bias.CalibrGet\
            \nGets the calibration and offset of bias voltage.\
            \nIf several ranges are available, this function returns the values of the selected one.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Calibration (float32)\
            \n- Offset (float32)\
            \n- Error described in the Response message>Body section')

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
        print('BiasSpectr.TTLSyncSet\
            \nSets the configuration of the TTL Synchronization feature in the Advanced section of the Bias Spectroscopy module. TTL synchronization allows for controlling the high-speed digital outs according to the individual stages of the bias spectroscopy measurement.\
            \nArguments:\
            \n- Enable (unsigned int16) selects whether the feature is active or not. 0 means no change, 1 means On, and 2 means Off\
            \n- TTL line (unsigned int16) sets which digital line should be controlled. 0 means no change, 1 means HS Line 1, 2 means HS Line 2, 3 means HS Line 3, 4 means HS Line 4\
            \n- TTL polarity (unsigned int16) sets the polarity of the switching action. 0 means no change, 1 means Low Active, and 2 means High Active\
            \n- Time to on (s) (float32) defines the time to wait before activating the TTL line\
            \n- On duration (s) (float32) defines how long the TTL line should be activated before resetting\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def BiasSpectrTTLSyncGet(self):
        print('BiasSpectr.TTLSyncGet\
            \nReturns the configuration of the TTL Synchronization feature in the Advanced section of the Bias Spectroscopy module.\
            \nTTL synchronization allows for controlling the high-speed digital outs according to the individual stages of the bias\
            \nspectroscopy measurement.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Enable (unsigned int16) indicates whether the feature is active or not. 0 means Off, 1 means On\
            \n- TTL line (unsigned int16) indicates which digital line should be controlled. 0 means HS Line 1, 1 means HS Line 2, 2 means HS Line 3, 3 means HS Line 4\
            \n- TTL polarity (unsigned int16) indicates the polarity of the switching action. 0 means Low Active, 1 means High Active\
            \n- Time to on (s) (float32) indicates the time to wait before activating the TTL line\
            \n- On duration (s) (float32) indicates how long the TTL line should be activated before resetting\
            \n- Error described in the Response message>Body section')

    def BiasSpectrAltZCtrlSet(self):
        print('BiasSpectr.AltZCtrlSet\
            \nSets the configuration of the alternate Z-controller setpoint in the Advanced section of the Bias Spectroscopy module.\
            \nWhen switched on, the Z-controller setpoint is set to the setpoint right after starting the measurement. After changing the setpoint the settling time (s) will be waited for the Z-controller to adjust to the modified setpoint.\
            \nThen the Z averaging will start. The original Z-controller setpoint is restored at the end of the measurement, before restoring the Z-controller state.\
            \nArguments:\
            \n- Alternate Z-controller setpoint (unsigned int16) where 0 means no change, 1 means On, and 2 means Off\
            \n- Setpoint (float32)\
            \n- Settling time (s) (float32)\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def BiasSpectrAltZCtrlGet(self):
        print('BiasSpectr.AltZCtrlGet\
            \nReturns the configuration of the alternate Z-controller setpoint in the Advanced section of the Bias Spectroscopy module.\
            \nWhen switched on, the Z-controller setpoint is set to the setpoint right after starting the measurement. After changing the setpoint the settling time (s) will be waited for the Z-controller to adjust to the modified setpoint.\
            \nThen the Z averaging will start. The original Z-controller setpoint is restored at the end of the measurement, before restoring the Z-controller state.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Alternate Z-controller setpoint (unsigned int16) where 0 means Off, 1 means On\
            \n- Setpoint (float32)\
            \n- Settling time (s) (float32)\
            \n- Error described in the Response message>Body section')

    def BiasSpectrMLSLockinPerSegSet(self):
        print('BiasSpectr.MLSLockinPerSegSet\
            \nSets the Lock-In per Segment flag in the Multi line segment editor.\
            \nWhen selected, the Lock-In can be defined per segment in the Multi line segment editor. Otherwise, the Lock-In is set globally according to the flag in the Advanced section of Bias spectroscopy.\
            \nArguments:\
            \n- Lock-In per segment (unsigned int32) where 0 means Off, 1 means On\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def BiasSpectrMLSLockinPerSegGet(self):
        print('BiasSpectr.MLSLockinPerSegGet\
            \nReturns the Lock-In per Segment flag in the Multi line segment editor.\
            \nWhen selected, the Lock-In can be defined per segment in the Multi line segment editor. Otherwise, the Lock-In is set globally according to the flag in the Advanced section of Bias spectroscopy.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Lock-In per segment (unsigned int32) where 0 means Off, 1 means On\
            \n- Error described in the Response message>Body section')

    def BiasSpectrMLSModeSet(self):
        print('BiasSpectr.MLSModeSet\
            \nSets the Bias Spectroscopy sweep mode.\
            \nArguments:\
            \n- Sweep mode (int) is the number of characters of the sweep mode string. If the sweep mode is Linear, this value is 6. If the sweep mode is MLS, this value is 3\
            \n- Sweep mode (string) is Linear in Linear mode or MLS in MultiSegment mode\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def BiasSpectrMLSModeGet(self):
        print('BiasSpectr.MLSModeGet\
            \nReturns the Bias Spectroscopy sweep mode.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Sweep mode (int) is the number of characters of the sweep mode string. If the sweep mode is Linear, this value is 6. If the sweep mode is MLS, this value is 3\
            \n- Sweep mode (string) is Linear in Linear mode or MLS in MultiSegment mode\
            \n- Error described in the Response message>Body section')

    def BiasSpectrMLSValsSet(self):
        print('BiasSpectr.MLSValsSet\
            \nSets the bias spectroscopy multiple line segment configuration for Multi Line Segment mode.\
            \nUp to 16 distinct line segments may be defined. Any segments beyond the maximum allowed amount will be ignored.\
            \nArguments:\
            \n- Number of segments (int) indicates the number of segments configured in MLS mode. This value is also the size of the 1D arrays set afterwards\
            \n- Bias start (V) (1D array float32) is the Start Bias value (V) for each line segment\
            \n- Bias end (V) (1D array float32 is the End Bias value (V) for each line segment\
            \n- Initial settling time (s) (1D array float32) indicates the number of seconds to wait at the beginning of each segment after the Lock-In setting is applied\
            \n- Settling time (s) (1D array float32) indicates the number of seconds to wait before measuring each data point each the line segment\
            \n- Integration time (s) (1D array float32) indicates the time during which the data are acquired and averaged in each segment\
            \n- Steps (1D array int) indicates the number of steps to measure in each segment\
            \n- Lock-In run (1D array unsigned int32) indicates if the Lock-In will run during the segment. This is true only if the global Lock-In per Segment flag is enabled.\
            \nOtherwise, the Lock-In is set globally according to the flag in the Advanced section of Bias spectroscopy\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def BiasSpectrMLSValsGet(self):
        print('BiasSpectr.MLSValsGet\
            \nReturns the bias spectroscopy multiple line segment configuration for Multi Line Segment mode.\
            \nUp to 16 distinct line segments may be defined.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Number of segments (int) indicates the number of segments configured in MLS mode. This value is also the size of the 1D arrays set afterwards\
            \n- Bias start (V) (1D array float32) is the Start Bias value (V) for each line segment\
            \n- Bias end (V) (1D array float32 is the End Bias value (V) for each line segment\
            \n- Initial settling time (s) (1D array float32) indicates the number of seconds to wait at the beginning of each segment after the Lock-In setting is applied\
            \n- Settling time (s) (1D array float32) indicates the number of seconds to wait before measuring each data point each the line segment\
            \n- Integration time (s) (1D array float32) indicates the time during which the data are acquired and averaged in each segment\
            \n- Steps (1D array int) indicates the number of steps to measure in each segment\
            \n- Lock-In run (1D array unsigned int32) indicates if the Lock-In will run during the segment. This is true only if the global Lock-In per Segment flag is enabled.\
            \nOtherwise, the Lock-In is set globally according to the flag in the Advanced section of Bias spectroscopy\
            \n- Error described in the Response message>Body section')
        
    def CurrentGet(self):
        print('Current.Get\
            \nReturns the tunneling current value.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Current value (A) (float32)\
            \n- Error described in the Response message>Body section')
        
    def CurrentCalibrGet(self):
        print('Current.CalibrGet\
            \nGets the calibration and offset of the selected gain in the Current module.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Calibration (float64)\
            \n- Offset (float64)\
            \n- Error described in the Response message>Body section')
        
    def ZCtrlZPosSet(self):
        print('ZCtrl.ZPosSet\
            \nSets the Z position of the tip.\
            \nNote: to change the Z-position of the tip, the Z-controller must be switched OFF.\
            \nArguments:\
            \n- Z position (m) (float32)\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')
    
    def ZCtrlZPosGet(self):
        print('ZCtrl.ZPosGet\
            \nReturns the current Z position of the tip.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Z position (m) (float32)\
            \n- Error described in the Response message>Body section')
        
    def ZCtrlOnOffSet(self):
        print('ZCtrl.OnOffSet\
            \nSwitches the Z-Controller On or Off.\
            \nArguments:\
            \n- Z-Controller status (unsigned int32) switches the controller Off (=0) or On (=1)\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def ZCtrlOnOffGet(self):
        print('ZCtrl.OnOffGet\
            \nReturns the status of the Z-Controller.\
            \nThis function returns the status from the real-time controller (i.e. not from the Z-Controller module).\
            \nThis function is useful to make sure that the Z-controller is really off before starting an experiment. Due to the communication delay, switch-off delay... sending the off command with the ZCtrl.OnOffGet function might take some time before the controller is off.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Z-Controller status (unsigned int32) indicates if the controller is Off (=0) or On (=1)\
            \n- Error described in the Response message>Body section')

    def ZCtrlSetpntSet(self):
        print('ZCtrl.SetpntSet\
            \nSets the setpoint of the Z-Controller.\
            \nArguments:\
            \n- Z-Controller setpoint (float32)\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def ZCtrlSetpntGet(self):
        print('ZCtrl.SetpntGet\
            \nReturns the setpoint of the Z-Controller.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Z-Controller setpoint (float32)\
            \n- Error described in the Response message>Body section')
        
    def ZCtrlTipLiftSet(self):
        print('ZCtrl.TipLiftSet\
              \nSets the TipLift of the Z-Controller.\
              \nRetracts the tip by the specified amount when turning off the Z-controller.\
              \nArguments:\
              \n- TipLift (m) (float32)\
              \nReturn arguments (if Send response back flag is set to True when sending request message):\
              \n- Error described in the Response message>Body section')
    def ZCtrlTipLiftSet(self):
        print('ZCtrl.TipLiftGet\
            \nReturns the TipLift of the Z-Controller.\
            \nRetracts the tip by the specified amount when turning off the Z-controller.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- TipLift (m) (float32)\
            \n- Error described in the Response message>Body section')

    def ScanAction(self):
        print('Scan.Action\
            \nStarts, stops, pauses or resumes a scan.\
            \nArguments:\
            \n- Scan action (unsigned int16) sets which action to perform, where 0 means Start, 1 is Stop, 2 is Pause, and\
            \n3 is Resume\
            \n- Scan direction (unsigned int32) that if 1, scan direction is set to up. If 0, direction is down\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def ScanStatusGet(self):
        print('Scan.StatusGet\
            \nReturns if the scan is running or not.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Scan status (unsigned int32) means that if it is 1, scan is running. If 0, scan is not running\
            \n- Error described in the Response message>Body section')

    def ScanWaitEndOfScan(self):
        print('Scan.WaitEndOfScan\
            \nWaits for the End-of-Scan.\
            \nThis function returns only when an End-of-Scan or timeout occurs (whichever occurs first).\
            \nArguments:\
            \n- Timeout (ms) (int) sets how many milliseconds this function waits for an End-of-Scan. If –1, it waits\
            \nindefinitely\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Timeout status status (unsigned int32) means that if it is 1, the function timed-out. If 0, it didn’t time-out\
            \n- File path size (unsigned int32) is the number of bytes corresponding to the File path string\
            \n- File path (string) returns the path where the data file was automatically saved (if auto-save was on). If no\
            \nfile was saved at the End-of-Scan, it returns an empty path\
            \n- Error described in the Response message>Body section')

    def ScanFrameSet(self):
        print('Scan.FrameSet\
            \nConfigures the scan frame parameters.\
            \nArguments:\
            \n- Center X (m) (float32) is the X position of the scan frame center\
            \n- Center Y (m) (float32) is the Y position of the scan frame center\
            \n- Width (m) (float32) is the width of the scan frame\
            \n- Height (m) (float32) is the height of the scan frame\
            \n- Angle (deg) (float32) is the angle of the scan frame (positive angle means clockwise rotation)\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def ScanFrameGet(self):
        print('Scan.FrameGet\
            \nReturns the scan frame parameters.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Center X (m) (float32) is the X position of the scan frame center\
            \n- Center Y (m) (float32) is the Y position of the scan frame center\
            \n- Width (m) (float32) is the width of the scan frame\
            \n- Height (m) (float32) is the height of the scan frame\
            \n- Angle (deg) (float32) is the angle of the scan frame (positive angle means clockwise rotation)\
            \n- Error described in the Response message>Body section')

    def ScanBufferSet(self):
        print('Scan.BufferSet\
            \nConfigures the scan buffer parameters.\
            \nArguments:\
            \n- Number of channels (int) is the number of recorded channels. It defines the size of the Channel indexes\
            \narray\
            \n- Channel indexes (1D array int) are the indexes of recorded channels. The index is comprised between 0\
            \nand 127, and it corresponds to the full list of signals available in the system.\
            \nTo get the signal name and its corresponding index in the list of the 128 available signals in the Nanonis\
            \nController, use the Signal.NamesGet function, or check the RT Idx value in the Signals Manager module.\
            \n- Pixels (int) is the number of pixels per line.\
            \nIn the scan control module this value is coerced to the closest multiple of 16, because the scan data is sent\
            \nfrom the RT to the host in packages of 16 pixels\
            \n- Lines (int) is the number of scan lines.\
            \nBe aware that if the chain button to keep the scan resolution ratio in the scan control module is active and\
            \nthe number of lines is set to 0 or left unconnected, the number of lines will automatically coerce to keep the\
            \nscan resolution ratio according to the new number of pixels.\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def ScanBufferGet(self):
        print('Scan.BufferGet\
            \nReturns the scan buffer parameters.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Number of channels (int) is the number of recorded channels. It defines the size of the Channel indexes\
            \narray\
            \n- Channel indexes (1D array int) are the indexes of recorded channels. The index is comprised between 0\
            \nand 127, and it corresponds to the full list of signals available in the system.\
            \nTo get the signal name and its corresponding index in the list of the 128 available signals in the Nanonis\
            \nController, use the Signal.NamesGet function, or check the RT Idx value in the Signals Manager module.\
            \n- Pixels (int) is the number of pixels per line\
            \n- Lines (int) is the number of scan lines\
            \n- Error described in the Response message>Body section')

    def ScanPropsSet(self):
        print('Scan.PropsSet\
            \nConfigures some of the scan parameters.\
            \nArguments:\
            \n- Continuous scan (unsigned int32) sets whether the scan continues or stops when a frame has been\
            \ncompleted. 0 means no change, 1 is On, and 2 is Off\
            \n- Bouncy scan (unsigned int32) sets whether the scan direction changes when a frame has been completed. 0\
            \nmeans no change, 1 is On, and 2 is Off\
            \n- Autosave (unsigned int32) defines the save behavior when a frame has been completed. "All" saves all the\
            \nfuture images. "Next" only saves the next frame. 0 means no change, 1 is All, 2 is Next, and 3 sets this\
            \nfeature Off\
            \n- Series name size (int) is the size in bytes of the Series name string\
            \n- Series name (string) is base name used for the saved images\
            \n- Comment size (int) is the size in bytes of the Comment string\
            \n- Comment (string) is comment saved in the file\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def ScanPropsGet(self):
        print('Scan.PropsGet\
            \nReturns some of the scan parameters.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Continuous scan (unsigned int32) indicates whether the scan continues or stops when a frame has been\
            \ncompleted. 0 means Off, and 1 is On\
            \n- Bouncy scan (unsigned int32) indicates whether the scan direction changes when a frame has been\
            \ncompleted. 0 means Off, and 1 is On\
            \n- Autosave (unsigned int32) defines the save behavior when a frame has been completed. "All" saves all the\
            \nfuture images. "Next" only saves the next frame. 0 is All, 1 is Next, and 2 means Off\
            \n- Series name size (int) is the size in bytes of the Series name string\
            \n- Series name (string) is base name used for the saved images\
            \n- Comment size (int) is the size in bytes of the Comment string\
            \n- Comment (string) is comment saved in the file\
            \n- Error described in the Response message>Body section')

    def ScanSpeedSet(self):
        print('Scan.SpeedSet\
            \nConfigures the scan speed parameters.\
            \nArguments:\
            \n- Forward linear speed (m/s) (float32)\
            \n- Backward linear speed (m/s) (float32)\
            \n- Forward time per line (s) (float32)\
            \n- Backward time per line (s) (float32)\
            \n- Keep parameter constant (unsigned int16) defines which speed parameter to keep constant, where 0\
            \nmeans no change, 1 keeps the linear speed constant, and 2 keeps the time per line constant\
            \n- Speed ratio (float32) defines the backward tip speed related to the forward speed\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def ScanSpeedGet(self):
        print('Scan.SpeedGet\
            \nReturns the scan speed parameters.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Forward linear speed (m/s) (float32)\
            \n- Backward linear speed (m/s) (float32)\
            \n- Forward time per line (s) (float32)\
            \n- Backward time per line (s) (float32)\
            \n- Keep parameter constant (unsigned int16) defines which speed parameter to keep constant, where 0\
            \nkeeps the linear speed constant, and 1 keeps the time per line constant\
            \n- Speed ratio (float32) is the backward tip speed related to the forward speed\
            \n- Error described in the Response message>Body section')

    def ScanFrameDataGrab(self):
        print('Scan.FrameDataGrab\
            \nReturns the scan data of the selected frame.\
            \nArguments:\
            \n- Channel index (unsigned int32) selects which channel to get the data from.\
            \nThe channel must be one of the acquired channels.\
            \nThe list of acquired channels while scanning can be configured by the function Scan.BufferSet.\
            \nThe index is comprised between 0 and 127, and it corresponds to the full list of signals available in the\
            \nsystem.\
            \nTo get the signal name and its corresponding index in the list of the 128 available signals in the Nanonis\
            \nController, use the Signal.NamesGet function, or check the RT Idx value in the Signals Manager module.\
            \n- Data direction (unsigned int32) selects the data direction, where 1 is forward, and 0 is backward\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Channels name size (int) is the size in bytes of the Channel name string\
            \n- Channel name (string) is the name of the channel selected by Channel index\
            \n- Scan data rows (int) defines the number of rows of the Scan data array\
            \n- Scan data columns (int) defines the number of columns of the Scan data array\
            \n- Scan data (2D array float32) returns the scan frame data of the selected channel\
            \n- Scan direction (unsigned int32) is the scan direction, where 1 is up, and 0 is down\
            \n- Error described in the Response message>Body section')

    def FolMeXYPosSet(self):
        print('FolMe.XYPosSet\
            \nMoves the tip.\
            \nThis function moves the tip to the specified X and Y target coordinates (in meters). It moves at the speed specified\
            \nby the "Speed" parameter in the Follow Me mode of the Scan Control module.\
            \nThis function will return when the tip reaches its destination or if the movement stops.\
            \nArguments:\
            \n- X (m) (float64) sets the target X position of the tip\
            \n- Y (m) (float64) sets the target Y position of the tip\
            \n- Wait end of move (unsigned int32) selects whether the function immediately (=0) or if it waits until the\
            \ntarget is reached or the movement is stopped (=1)\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def FolMeXYPosGet(self):
        print('FolMe.XYPosGet\
            \nReturns the X,Y tip coordinates (oversampled during the Acquisition Period time, Tap).\
            \nArguments:\
            \n- Wait for newest data (unsigned int32) selects whether the function returns the next available signal value\
            \nor if it waits for a full period of new data.\
            \nIf 0, this function returns a value 0 to Tap seconds after being called.\
            \nIf 1, the function discards the first oversampled signal value received but returns the second value received.\
            \nThus, the function returns a value Tap to 2*Tap seconds after being called\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- X (m) (float64) is the current X position of the tip\
            \n- Y (m) (float64) is the current Y position of the tip\
            \n- Error described in the Response message>Body section')

    def FolMeSpeedSet(self):
        print('FolMe.SpeedSet\
            \nConfigures the tip speed when moving in Follow Me mode.\
            \nArguments:\
            \n- Speed (m/s) (float32) sets the surface speed in Follow Me mode\
            \n- Custom speed (unsigned int32) sets whether custom speed setting is used for Follow Me mode (=1) or if\
            \nscan speed is used (=0)\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def FolMeSpeedGet(self):
        print('FolMe.SpeedGet\
            \nReturns the tip speed when moving in Follow Me mode.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Speed (m/s) (float32) is the surface speed in Follow Me mode\
            \n- Custom speed (unsigned int32) returns whether custom speed setting is used for Follow Me mode (=1) or\
            \nif scan speed is used (=0)\
            \n- Error described in the Response message>Body section')

    def FolMeOversamplSet(self):
        print('FolMe.OversamplSet\
            \nSets the oversampling of the acquired data when the tip is moving in Follow Me mode.\
            \nArguments:\
            \n- Oversampling (int)\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def FolMeOversamplGet(self):
        print('FolMe.OversamplGet\
            \nReturns the oversampling and rate of the acquired data when the tip is moving in Follow Me mode.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Oversampling (int)\
            \n- Sampling rate (Samples/s) (float32)\
            \n- Error described in the Response message>Body section')

    def FolMeStop(self):
        print('FolMe.Stop\
            \nStops the tip movement in Follow Me mode.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def FolMePSOnOffGet(self):
        print('FolMe.PSOnOffGet\
            \nReturns if Point & Shoot is enabled or disabled in Follow Me mode.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Point & Shoot status (unsigned int32) returns whether Point & Shoot is enabled (=1) or disabled (=0)\
            \n- Error described in the Response message>Body section')

    def FolMePSOnOffSet(self):
        print('FolMe.PSOnOffSet\
            \nEnables or disables Point & Shoot in Follow Me mode.\
            \nArguments:\
            \n- Point & Shoot status (unsigned int32) enables (=1) or disables (=0) Point & Shoot\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def FolMePSExpGet(self):
        print('FolMe.PSExpGet\
            \nReturns the Point & Shoot experiment selected in Follow Me mode.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Point & Shoot experiment (unsigned int16) returns the selected Point & Shoot experiment\
            \n- Size of the list of experiments (int) is the full size in bytes of the List of experiments string array\
            \n- Number of experiments (int) is the number of elements of the List of experiments string array\
            \n- List of experiments (1D array string) returns the list of experiments available in the Pattern section. The\
            \nsize of each string item comes right before it as integer 32\
            \n- Error described in the Response message>Body section')

    def FolMePSExpSet(self):
        print('FolMe.PSExpSet\
            \nSets the Point & Shoot experiment selected in Follow Me mode.\
            \nArguments:\
            \n- Point & Shoot experiment (unsigned int16) returns the selected Point & Shoot experiment\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def FolMePSPropsGet(self):
        print('FolMe.PSPropsGet\
            \nReturns the Point & Shoot configuration in Follow Me mode.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Auto resume (unsigned int32) returns if the scan resumes after running the experiment (=1) or if it remains\
            \npaused (=0)\
            \n- Use own basename (unsigned int32) returns if the file basename is the one defined in the experiment\
            \nmodule (i.e. in Bias Spectroscopy) (=1) or if it uses the basename configured in Point & Shoot (=0)\
            \n- Basename size (int) is the size in bytes of the Basename string\
            \n- Basename (string) returns the basename defined in Point & Shoot\
            \n- External VI path size (int) is the size in bytes of the External VI path string\
            \n- External VI path (string) returns the path of the External VI selected in Point & Shoot\
            \n- Pre-measure delay (s) (float32) is the time to wait on each point before performing the experiment\
            \n- Error described in the Response message>Body section')

    def FolMePSPropsSet(self):
        print('FolMe.PSPropsSet\
            \nSets the Point & Shoot configuration in Follow Me mode.\
            \nArguments:\
            \n- Auto resume (unsigned int32) sets if the scan resumes after running the experiment (=1) or if it remains\
            \npaused (=2). A value=0 means no change.\
            \n- Use own basename (unsigned int32) sets if the file basename is the one defined in the experiment module\
            \n(i.e. in Bias Spectroscopy) (=1) or if it uses the basename configured in Point & Shoot (=2). A value=0\
            \nmeans no change.\
            \n- Basename size (int) is the size in bytes of the Basename string\
            \n- Basename (string) sets the basename in Point & Shoot\
            \n- External VI path size (int) is the size in bytes of the External VI path string\
            \n- External VI path (string) sets the path of the External VI selected in Point & Shoot\
            \n- Pre-measure delay (s) (float32) is the time to wait on each point before performing the experiment\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')


    def TipShaperStart(self):
        print('TipShaper.Start\
            \nStarts the tip shaper procedure.\
            \nArguments:\
            \n- Wait until finished (unsigned int32) defines if this function waits (1=True) until the Tip Shaper procedure stops.\
            \n- Timeout (ms) (int) sets the number of milliseconds to wait if Wait until Finished is set to True.\
            \nA value equal to -1 means waiting forever.\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def TipShaperPropsSet(self):
        print('TipShaper.PropsSet\
            \nSets the configuration of the tip shaper procedure.\
            \nArguments:\
            \n- Switch Off Delay (float32) is the time during which the Z position is averaged right before switching the Z-Controller off.\
            \n- Change Bias? (unsigned int32) decides whether the Bias value is applied (0=no change, 1=True, 2=False) right before the first Z ramping.\
            \n- Bias (V) (float32) is the value applied to the Bias signal if Change Bias? is True.\
            \n- Tip Lift (m) (float32) defines the relative height the tip is going to ramp for the first time (from the current Z position).\
            \n- Lift Time 1 (s) (float32) defines the time to ramp Z from the current Z position by the Tip Lift amount.\
            \n- Bias Lift (V) (float32) is the Bias voltage applied just after the first Z ramping.\
            \n- Bias Settling Time (s) (float32) is the time to wait after applying the Bias Lift value, and it is also the time to wait after applying Bias (V) before ramping Z for the first time.\
            \n- Lift Height (m) (float32) defines the height the tip is going to ramp for the second time.\
            \n- Lift Time 2 (s) (float32) is the given time to ramp Z in the second ramping.\
            \n- End Wait Time (s) (float32) is the time to wait after restoring the initial Bias voltage (just after finishing the second ramping).\
            \n- Restore Feedback? (unsigned int32) defines whether the initial Z-Controller status is restored (0=no change, 1=True, 2=False) at the end of the tip shaper procedure.\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def TipShaperPropsGet(self):
        print('TipShaper.PropsGet\
            \nReturns the configuration of the tip shaper procedure.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Switch Off Delay (float32) is the time during which the Z position is averaged right before switching the Z-Controller off.\
            \n- Change Bias? (unsigned int32) returns whether the Bias value is applied (0=False, 1=True) right before the first Z ramping.\
            \n- Bias (V) (float32) is the value applied to the Bias signal if Change Bias? is True.\
            \n- Tip Lift (m) (float32) returns the relative height the tip is going to ramp for the first time (from the current Z position).\
            \n- Lift Time 1 (s) (float32) returns the time to ramp Z from the current Z position by the Tip Lift amount.\
            \n- Bias Lift (V) (float32) is the Bias voltage applied just after the first Z ramping.\
            \n- Bias Settling Time (s) (float32) is the time to wait after applying the Bias Lift value, and it is also the time to wait after applying Bias (V) before ramping Z for the first time.\
            \n- Lift Height (m) (float32) returns the height the tip is going to ramp for the second time.\
            \n- Lift Time 2 (s) (float32) is the given time to ramp Z in the second ramping.\
            \n- End Wait Time (s) (float32) is the time to wait after restoring the initial Bias voltage (just after finishing the second ramping).\
            \n- Restore Feedback? (unsigned int32) returns whether the initial Z-Controller status is restored (0=False, 1=True) at the end of the tip shaper procedure.\
            \n- Error described in the Response message>Body section')
        

    def GenSwpAcqChsSet(self):
        print('GenSwp.AcqChsSet\
            \nSets the list of recorded channels of the Generic Sweeper.\
            \nArguments:\
            \n- Number of channels (int) is the number of recorded channels. It defines the size of the Channel indexes\
            \narray\
            \n- Channel indexes (1D array int) are the indexes of recorded channels. The indexes correspond to the list of\
            \nMeasurement in the Nanonis software.\
            \nTo get the Measurements names use the Signals.MeasNamesGet function\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def GenSwpAcqChsGet(self):
        print('GenSwp.AcqChsGet\
            \nReturns the list of recorded channels of the Generic Sweeper.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Number of channels (int) is the number of recorded channels. It defines the size of the Channel indexes\
            \narray\
            \n- Channel indexes (1D array int) are the indexes of the recorded channels. The indexes correspond to the list\
            \nof Measurement in the Nanonis software.\
            \nTo get the Measurements names use the Signals.MeasNamesGet function\
            \n- Error described in the Response message>Body section')

    def GenSwpSwpSignalSet(self):
        print('GenSwp.SwpSignalSet\
            \nSets the Sweep signal in the Generic Sweeper.\
            \nArguments:\
            \n- Sweep channel name size (int) is the number of characters of the sweep channel name string\
            \n- Sweep channel name (string) is the name of the signal selected for the sweep channel\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def GenSwpSwpSignalGet(self):
        print('GenSwp.SwpSignalGet\
            \nReturns the selected Sweep signal in the Generic Sweeper.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Sweep channel name size (int) is the number of characters of the sweep channel name string\
            \n- Sweep channel name (string) is the name of the signal selected for the sweep channel\
            \n- Channels names size (int) is the size in bytes of the Channels names string array\
            \n- Number of channels (int) is the number of elements of the Channels names string array\
            \n- Channels names (1D array string) returns the list of channels names. The size of each string item comes\
            \nright before it as integer 32\
            \n- Error described in the Response message>Body section')

    def GenSwpLimitsSet(self):
        print('GenSwp.LimitsSet\
            \nSets the limits of the Sweep signal in the Generic Sweeper.\
            \nArguments:\
            \n- Lower limit (float32) defines the lower limit of the sweep range\
            \n- Upper limit (float32) defines the upper limit of the sweep range\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def GenSwpLimitsGet(self):
        print('GenSwp.LimitsGet\
            \nReturns the limits of the Sweep signal in the Generic Sweeper.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Lower limit (float32) defines the lower limit of the sweep range\
            \n- Upper limit (float32) defines the upper limit of the sweep range\
            \n- Error described in the Response message>Body section')

    def GenSwpPropsSet(self):
        print('GenSwp.PropsSet\
            \nSets the configuration of the parameters in the Generic Sweeper.\
            \nArguments:\
            \n- Initial Settling time (ms) (float32)\
            \n- Maximum slew rate (units/s) (float32)\
            \n- Number of steps (int) defines the number of steps of the sweep. 0 points means no change\
            \n- Period (ms) (unsigned int16) where 0 means no change\
            \n- Autosave (int) defines if the sweep is automatically saved, where -1=no change, 0=Off, 1=On\
            \n- Save dialog box (int) defines if the save dialog box shows up or not, where -1=no change, 0=Off, 1=On\
            \n- Settling time (ms) (float32)\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def GenSwpPropsGet(self):
        print('GenSwp.PropsGet\
            \nReturns the configuration of the parameters in the Generic Sweeper.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Initial Settling time (ms) (float32)\
            \n- Maximum slew rate (units/s) (float32)\
            \n- Number of steps (int) defines the number of steps of the sweep\
            \n- Period (ms) (unsigned int16)\
            \n- Autosave (unsigned int32) defines if the sweep is automatically saved, where 0=Off, 1=On\
            \n- Save dialog box (unsigned int32) defines if the save dialog box shows up or not, where 0=Off, 1=On\
            \n- Settling time (ms) (float32)\
            \n- Error described in the Response message>Body section')

    def GenSwpStart(self):
        print('GenSwp.Start\
            \nStarts the sweep in the Generic Sweeper.\
            \nArguments:\
            \n- Get data (unsigned int32) defines if the function returns the sweep data (1=True) or not (0=False)\
            \n- Sweep direction (unsigned int32) defines if the sweep starts from the lower limit (=1) or from the upper\
            \nlimit (=0)\
            \n- Save base name string size (int) defines the number of characters of the Save base name string\
            \n- Save base name (string) is the basename used by the saved files. If empty string, there is no change\
            \n- Reset signal (unsigned int32) where 0=Off, 1=On\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Channels names size (int) is the size in bytes of the Channels names string array\
            \n- Number of channels (int) is the number of elements of the Channels names string array\
            \n- Channels names (1D array string) returns the list of channels names. The size of each string item comes\
            \nright before it as integer 32\
            \n- Data rows (int) defines the numer of rows of the Data array\
            \n- Data columns (int) defines the numer of columns of the Data array\
            \n- Data (2D array float32) returns the sweep data\
            \n- Error described in the Response message>Body section')

    def GenSwpStop(self):
        print('GenSwp.Stop\
            \nStops the sweep in the Generic Sweeper module.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def GenSwpOpen(self):
        print('GenSwp.Open\
            \nOpens the Generic Sweeper module.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')


    def AtomTrackCtrlSet(self):
        print('AtomTrack.CtrlSet\
            \nTurns the selected Atom Tracking control (modulation, controller or drift measurement) On or Off.\
            \nArguments:\
            \n- AT control (unsigned int16) sets which control to switch. 0 means Modulation, 1 means Controller, and 2 means Drift Measurement\
            \n- Status (unsigned int16) switches the selected control Off (=0) or On (=1)\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def AtomTrackStatusGet(self):
        print('AtomTrack.StatusGet\
            \nReturns the status of the selected Atom Tracking control (modulation, controller or drift measurement).\
            \nArguments:\
            \n- AT control (unsigned int16) sets which control to read the status from. 0 means Modulation, 1 means Controller, and 2 means Drift Measurement\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Status (unsigned int16) returns the status of the selected control, where 0 means Off and 1 means On\
            \n- Error described in the Response message>Body section')

    def AtomTrackPropsSet(self):
        print('AtomTrack.PropsSet\
            \nSets the Atom Tracking parameters.\
            \nArguments:\
            \n- Integral gain (float32) is the gain of the Atom Tracking controller\
            \n- Frequency (Hz) (float32) is the frequency of the modulation\
            \n- Amplitude (m) (float32) is the amplitude of the modulation\
            \n- Phase (deg) (float32) is the phase of the modulation\
            \n- Switch Off delay (s) (float32) means that before turning off the controller, the position is averaged over this time delay. The averaged position is then applied. This leads to reproducible positions when switching off the Atom Tracking controller\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def AtomTrackPropsGet(self):
        print('AtomTrack.PropsGet\
            \nReturns the Atom Tracking parameters.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Integral gain (float32) is the gain of the Atom Tracking controller\
            \n- Frequency (Hz) (float32) is the frequency of the modulation\
            \n- Amplitude (m) (float32) is the amplitude of the modulation\
            \n- Phase (deg) (float32) is the phase of the modulation\
            \n- Switch Off delay (s) (float32) means that before turning off the controller, the position is averaged over this time delay. The averaged position is then applied. This leads to reproducible positions when switching off the Atom Tracking controller\
            \n- Error described in the Response message>Body section')

    def LockInModOnOffSet(self):
        print('LockIn.ModOnOffSet\
            \nTurns the specified Lock-In modulator on or off.\
            \nArguments:\
            \n- Modulator number (int) is the number that specifies which modulator to use. It starts from number 1 (=Modulator 1)\
            \n- Lock-In On/Off (unsigned int32) turns the specified modulator on or off, where 0=Off and 1=On\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def LockInModOnOffGet(self):
        print('LockIn.ModOnOffGet\
            \nReturns if the specified Lock-In modulator is turned on or off.\
            \nArguments:\
            \n- Modulator number (int) is the number that specifies which modulator to use. It starts from number 1 (=Modulator 1)\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Lock-In On/Off (unsigned int32) returns if the specified modulator is turned on or off, where 0=Off and 1=On\
            \n- Error described in the Response message>Body section')

    def LockInModAmpSet(self):
        print('LockIn.ModAmpSet\
            \nSets the modulation amplitude of the specified Lock-In modulator.\
            \nArguments:\
            \n- Modulator number (int) is the number that specifies which modulator to use. It starts from number 1 (=Modulator 1)\
            \n- Amplitude (float32) is the modulation amplitude of the specified Lock-In modulator\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def LockInModAmpGet(self):
        print('LockIn.ModAmpGet\
            \nReturns the modulation amplitude of the specified Lock-In modulator.\
            \nArguments:\
            \n- Modulator number (int) is the number that specifies which modulator to use. It starts from number 1 (=Modulator 1)\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Amplitude (float32) is the modulation amplitude of the specified Lock-In modulator\
            \n- Error described in the Response message>Body section')

    def LockInModPhasFreqSet(self):
        print('LockIn.ModPhasFreqSet\
            \nSets the frequency of the specified Lock-In phase register/modulator.\
            \nThe Lock-in module has a total of 8 frequency generators / phase registers. Each modulator and demodulator can be bound to one of the phase registers.\
            \nThis function sets the frequency of one of the phase registers.\
            \nArguments:\
            \n- Modulator number (int) is the number that specifies which phase register/modulator to use. It starts from number 1 (=Modulator 1)\
            \n- Frequency (Hz) (float64) is the frequency of the specified Lock-In phase register\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

    def LockInModPhasFreqGet(self):
        print('LockIn.ModPhasFreqGet\
            \nReturns the frequency of the specified Lock-In phase register/modulator.\
            \nThe Lock-in module has a total of 8 frequency generators / phase registers. Each modulator and demodulator can be bound to one of the phase registers.\
            \nThis function gets the frequency of one of the phase registers.\
            \nArguments:\
            \n- Modulator number (int) is the number that specifies which phase register/modulator to use. It starts from number 1 (=Modulator 1)\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Frequency (Hz) (float64) is the frequency of the specified Lock-In phase register\
            \n- Error described in the Response message>Body section')
        
    def SignalsNamesGet(self):
        print('Signals.NamesGet\
            \nReturns the signals names list of the 128 signals available in the software.\
            \nThe 128 signals are physical inputs, physical outputs and internal channels. By searching in the list the channel’s name you are interested in, you can get its index (0-127).\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Signals names size (int) is the size in bytes of the signals names array\
            \n- Signals names number (int) is the number of elements of the signals names array\
            \n- Signals names (1D array string) returns an array of signals names strings, where each string comes prepended by its size in bytes\
            \n- Error described in the Response message>Body sectionSignals.CalibrGet\
            \nReturns the calibration and offset of the selected signal.')
        

    def DataLogOpen(self):
        print('DataLog.Open\
            \nOpens the Data Logger module.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')
        
    def DataLogStart(self):
        print('DataLog.Start\
            \nStarts the acquisition in the Data Logger module.\
            \nBefore using this function, select the channels to record in the Data Logger.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')
        
    def DataLogStop(self):
        print('DataLog.Stop\
            \nStops the acquisition in the Data Logger module.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')
        
    def DataLogStatusGet(self):
        print('DataLog.StatusGet\
            \nReturns the status parameters from the Data Logger module.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Start time size (int) returns the number of bytes corresponding to the Start time string\
            \n- Start time (string) returns a timestamp of the moment when the acquisition started\
            \n- Acquisition elapsed hours (unsigned int16) returns the number of hours already passed since the\
            \nacquisition started\
            \n- Acquisition elapsed minutes (unsigned int16) returns the number of minutes displayed on the Data Logger\
            \n- Acquisition elapsed seconds (float32) returns the number of seconds displayed on the Data Logger\
            \n- Stop time size (int) returns the number of bytes corresponding to the Stop time string\
            \n- Stop time (string) returns a timestamp of the moment when the acquisition Stopped\
            \n- Saved file path size (int) returns the number of bytes corresponding to the Saved file path string\
            \n- Saved file path (string) returns the path of the last saved file\
            \n- Points counter (int) returns the number of points (averaged samples) to save into file.\
            \nThis parameter updates while running the acquisition\
            \n- Error described in the Response message>Body section')
        
    def DataLogChsSet(self):
        print('DataLog.ChsSet\
            \nSets the list of recorded channels in the Data Logger module.\
            \nArguments:\
            \n- Number of channels (int) is the number of recorded channels. It defines the size of the Channel indexes\
            \narray\
            \n- Channel indexes (1D array int) are the indexes of recorded channels. The index is comprised between 0\
            \nand 127, and it corresponds to the full list of signals available in the system.\
            \nTo get the signal name and its corresponding index in the list of the 128 available signals in the Nanonis\
            \nController, use the Signal.NamesGet function, or check the RT Idx value in the Signals Manager module.\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')
        
    def DataLogChsGet(self):
        print('DataLog.ChsGet\
            \nReturns the list of recorded channels in the Data Logger module.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Number of channels (int) is the number of recorded channels. It defines the size of the Channel indexes\
            \narray\
            \n- Channel indexes (1D array int) are the indexes of recorded channels. The index is comprised between 0\
            \nand 127, and it corresponds to the full list of signals available in the system.\
            \nTo get the signal name and its corresponding index in the list of the 128 available signals in the Nanonis\
            \nController, use the Signal.NamesGet function, or check the RT Idx value in the Signals Manager module\
            \n- Error described in the Response message>Body section')
        
    def DataLogPropsSet(self):
        print('DataLog.PropsSet\
            \nSets the acquisition configuration and the save options in the Data Logger module.\
            \nArguments:\
            \n- Acquisition mode (unsigned int16) means that if Timed (=2), the selected channels are acquired during the\
            \nacquisition duration time or until the user presses the Stop button.\
            \nIf Continuous (=1), the selected channels are acquired continuously until the user presses the Stop button.\
            \nIf 0, the is no change in the acquisition mode.\
            \nThe acquired data are saved every time the averaged samples buffer reaches 25.000 samples and when the\
            \nacquisition stops\
            \n- Acquisition duration( hours) (int) sets the number of hours the acquisition should last. Value -1 means no\
            \nchange\
            \n- Acquisition duration (minutes) (int) sets the number of minutes. Value -1 means no change\
            \n- Acquisition duration (seconds) (float32) sets the number of seconds. Value -1 means no change\
            \n- Averaging (int) sets how many data samples (received from the real-time system) are averaged for one\
            \ndata point saved into file. By increasing this value, the noise might decrease, and fewer points per seconds\
            \nare recorded.\
            \nUse 0 to skip changing this parameter\
            \n- Basename size (int) is the size in bytes of the Basename string\
            \n- Basename (string) is base name used for the saved images\
            \n- Comment size (int) is the size in bytes of the Comment string\
            \n- Comment (string) is comment saved in the file\
            \n- Size of the list of moduless (int) is the size in bytes of the List of modules string array\
            \n- Number of modules (int) is the number of elements of the List of modules string array\
            \n- List of modules (1D array string) sets the modules names whose parameters will be saved in the header of\
            \nthe files. The size of each string item should come right before it as integer 32\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')
        
    def DataLogPropsGet(self):
        print('DataLog.PropsGet\
            \nReturns the acquisition configuration and the save options in the Data Logger module.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Acquisition mode (unsigned int16) means that if Timed (=1), the selected channels are acquired during the\
            \nacquisition duration time or until the user presses the Stop button.\
            \nIf Continuous (=0), the selected channels are acquired continuously until the user presses the Stop button.\
            \nThe acquired data are saved every time the averaged samples buffer reaches 25.000 samples and when the\
            \nacquisition stops\
            \n- Acquisition duration( hours) (int) returns the number of hours the acquisition lasts\
            \n- Acquisition duration (minutes) (int) returns the number of minutes\
            \n- Acquisition duration (seconds) (float32) returns the number of seconds\
            \n- Averaging (int) returns how many data samples (received from the real-time system) are averaged for one\
            \ndata point saved into file\
            \n- Basename size (int) returns the size in bytes of the Basename string\
            \n- Basename (string) returns the base name used for the saved images\
            \n- Comment size (int) returns the size in bytes of the Comment string\
            \n- Comment (string) returns the comment saved in the file\
            \n- Error described in the Response message>Body section')
        

    def UtilSessionPathGet(self):
        print('Util.SessionPathGet\
            \nReturns the session path.\
            \nArguments: None\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Session path size (int) is the number of characters of the Session path string\
            \n- Session path (string)\
            \n- Error described in the Response message>Body section')

    def UtilSessionPathSet(self):
        print('Util.SessionPathSet\
            \nSets the session folder path.\
            \nArguments:\
            \n- Session path size (int) is the number of characters of the Session path string\
            \n- Session path (string)\
            \n- Save settings to previous (unsigned int32) determines if the settings are saved to the previous session file\
            \nbefore changing it, where 0=False and 1=True\
            \nReturn arguments (if Send response back flag is set to True when sending request message):\
            \n- Error described in the Response message>Body section')

class esr_meas_help:
    def __int__(self):
        self.general_info = 'This is a module containing several functions that executes commands for ESR measurements.'

    def check_dirs(self):
        print('check_dirs(self, dirName)\
              \nChecks if the given directory exists. If not, the function creates it.')
    def bias_spectr_par_save(self):
        print('bias_spectr_par_save(self, fdir, fname = '')\
              \nSaves the measurement parameters in Nanonis software as a ".par" file in the given directory.\
              \n"fname" is the suffix of the saved ".par" file')
        
    def bias_spectr_par_load(self):
        print('bias_spectr_par_load(self, fdir, fname)\
              \nLoads the ".par" file as a dictionary\
              \nReturns the dictionary')
        
    def bias_spectr(self):
        print("bias_spectr(self, par, data_folder, basename = '%Y%m%d_')\
              \nRun the bias spectroscopy measurement. \
              \n'par' should be the dictionary returned by 'bias_spectr_par_load' function.\
              \n'data_folder' is the subfolder of the current session folder.\
              \n'basename' is the name of the file, eg. '%Y%m%d_', 'STS_%Y%m%d_', etc. ")
        
    def atom_pickup(self):
        print('atom_pickup(radius)\
              \nRun the atom pickup procedure. The function measures the delta z before and after the pickup process.\
              \n"radius" is the distance used for measuring four points on the substrate around the atom. The default value is 1 nm. ')