import nanonis_esr_tcp as tcp
import time
import numpy as np
import pandas as pd

my_tcp = tcp.tcp_ctrl()

connect = tcp.nanonis_ctrl(my_tcp)
tcphelp = tcp.help()
esr_meas = tcp.esr_meas(connect)

# pos = connect.FolMeXYPosGet(1)
connect.MarksPointsGet()
# connect.MarksPointDraw(200e-9, 100e-9, 'aaa', [255,255,55])
# connect.MarksPointsErase(0)
# 16776960
# connect.MarksLinesDraw(2,
#     [, 0.000000450],
#     [0.000000420, 0.000000430],
#     [0.000000470, 0.000000480],
#     [0.000000330, 0.000000470], 
#     [255, 255])
# connect.MarksLinesDraw(2,
#     [320e-9, 450e-9],
#     [420e-9, 430e-9], 
#     [350e-9, 460-9],
#     [450e-9, 460e-9],
#     [255255, 255]
#     )
# connect.MarksPointsGet()
# connect.MarksLinesGet()
# connect.MarksLinesErase(0)
