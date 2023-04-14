import nanonis_esr_tcp as tcp
from os import mkdir
from os.path import exists
import time
import pickle
import numpy as np
import pandas as pd

my_tcp = tcp.tcp_ctrl()
connect = tcp.nanonis_ctrl(my_tcp)

connect.AtomTrackCtrlSet(0,1)
connect.AtomTrackCtrlSet(1,1)
print('Wait atom tracking for 5 seconds...')
time.sleep(5)

connect.AtomTrackCtrlSet(0,0)
connect.AtomTrackCtrlSet(1,0)

connect.BiasSet('50u')
connect.ZCtrlOnOffSet(0)
connect.BiasPulse(1, '150m', '650m', 1, 0)
connect.ZCtrlOnOffSet(1)
connect.BiasSet('100m')