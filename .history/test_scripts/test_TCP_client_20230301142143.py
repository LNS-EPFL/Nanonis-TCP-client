# -*- encoding: utf-8 -*-
'''
@Time    :   2023/02/28 14:52:33
@Author  :   Shixuan Shan 
'''
import socket
from collections import defaultdict

data types: 'str', 'int', 'uint16', 'uint32', 'float32', 'float64', 'hex'

############################### functions ###################################
def socket_connect(TCP_IP = '127.0.0.1', PORT = PORT):
    server_address = (TCP_IP, PORT)
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.connect(server_address)
    return sk

def socket_close(sk):
    sk.close()

def data_type_converter(original_fmt, target_fmt, data):
    data_type_convert = defaultdict({
        (original_fmt == 'hex'     and target_fmt == 'str'     ):'AA',
        (original_fmt == 'hex'     and target_fmt == 'int'     ): 'BB',
        (original_fmt == 'hex'     and target_fmt == 'uint16'  ): 'CC',
        (original_fmt == 'hex'     and target_fmt == 'uint32'  ): 'DD',
        (original_fmt == 'hex'     and target_fmt == 'float32' ): 'EE',
        (original_fmt == 'hex'     and target_fmt == 'float64' ): 'FF',
        (original_fmt == 'str'     and target_fmt == 'hex'     ): 'GG',
        (original_fmt == 'int'     and target_fmt == 'hex'     ): 'II',
        (original_fmt == 'uint16'  and target_fmt == 'hex'     ):'AA',
        (original_fmt == 'uint32'  and target_fmt == 'hex'     ): 'BB',
        (original_fmt == 'float32' and target_fmt == 'hex'     ): 'CC',
        (original_fmt == 'float64' and target_fmt == 'hex'     ): 'DD',
        (Hx_mean_df.iloc[0, 1] == 'error2' or
        Hx_mean_df.iloc[0, 2] == 'error2' or
        Hx_mean_df.iloc[0, 3] == 'error2' or
        Hx_mean_df.iloc[0, 4] == 'error2' or
        Hx_mean_df.iloc[0, 5] == 'error2'): "JJ"
        })
    new_type = data_type_convert[original_fmt, target_fmt, data]
    return new_type





TCP_IP = '127.0.0.1'
PORT = 6501 # avialable ports: 6501, 6502, 6503, 6504
server_address = (TCP_IP, PORT)

# create a TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(server_address)

s.close()