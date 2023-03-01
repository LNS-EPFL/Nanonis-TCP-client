# -*- encoding: utf-8 -*-
'''
@Time    :   2023/02/28 14:52:33
@Author  :   Shixuan Shan 
'''
import socket
from collections import defaultdict

############################### functions ###################################
def socket_connect(TCP_IP = '127.0.0.1', PORT = PORT):
    server_address = (TCP_IP, PORT)
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.connect(server_address)
    return sk

def socket_close(sk):
    sk.close()

def data_type_converter(original_fmt, target_fmt, data):
    data_type_convert = defaultdict(
                                    {(f_reference < 16 or f_reference > 20):'AA',
                                    (16 <= f_reference < 16.8): 'BB',
                                    ((17.96 <= f_reference <= 18.04 and delta_HH_HB_abs > 17) or (18.04 < f_reference <= 20) or (17.8 < f_reference < 17.96)): 'CC',
                                    (16.8 <= f_reference <= 17.8 and delta_HH_HB_abs > 17): 'DD',
                                    (16.8 <= f_reference <= 17.8 and delta_HH_HB_abs <= 17 and d_criteria == d_criteria): 'EE',
                                    ((17.96 <= f_reference <= 18.04 and delta_HH_HB_abs <= 17) or
                                    (16.8 <= f_reference <= 17.8 and delta_HH_HB_abs <= 17 and d_criteria != d_criteria)): 'FF',
                                    (17.96 <= f_reference <= 18.04 and delta_HH_HB_abs <= 17 and (d_criteria < -6 or d_criteria > 8 or p_criteria > 10)): 'GG',
                                    (17.96 <= f_reference <= 18.04 and -6 <= d_criteria <= 8 and p_criteria <= 10): 'II',
                                    (Hx_mean_df.iloc[0, 1] == 'error2' or
                                    Hx_mean_df.iloc[0, 2] == 'error2' or
                                    Hx_mean_df.iloc[0, 3] == 'error2' or
                                    Hx_mean_df.iloc[0, 4] == 'error2' or
                                    Hx_mean_df.iloc[0, 5] == 'error2'): "JJ"
                                    }
                                    )
    





TCP_IP = '127.0.0.1'
PORT = 6501 # avialable ports: 6501, 6502, 6503, 6504
server_address = (TCP_IP, PORT)

# create a TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(server_address)

s.close()