import nanonis_esr_tcp as tcp
from os import mkdir
from os.path import exists
# import time
import pickle
import numpy as np
import pandas as pd

pd.set_option('display.max_columns', 100)


my_tcp = tcp.tcp_ctrl()
connect = tcp.nanonis_ctrl(my_tcp)

df = connect.BiasGet()
print(df)

