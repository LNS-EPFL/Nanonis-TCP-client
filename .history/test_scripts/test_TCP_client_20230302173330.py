# -*- encoding: utf-8 -*-
'''
@Time    :   2023/02/28 14:52:33
@Author  :   Shixuan Shan 
'''
import socket
from collections import defaultdict
import struct as st

# data types: 'str', 'int'(i), 'uint16'(H), 'uint32'(L), 'float32'(f), 'float64'(d), 'hex'
# big-endian encoded '>'

############################### functions ###################################
def socket_connect(TCP_IP = '127.0.0.1', PORT = 6501):
    server_address = (TCP_IP, PORT)
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.connect(server_address)
    return sk

def socket_close(sk):
    sk.close()

def data_type_converter(original_fmt, target_fmt, data):
    data_type_convert = defaultdict(lambda:
                                    {
                                    # to hex
                                    # (original_fmt == 'str'     and target_fmt == 'hex'     ): 'a',
                                    (original_fmt == 'int'     and target_fmt == 'hex'     ): st.pack('>i'),
                                    (original_fmt == 'uint16'  and target_fmt == 'hex'     ): st.pack('>H'),
                                    (original_fmt == 'uint32'  and target_fmt == 'hex'     ): st.pack('>L'),
                                    (original_fmt == 'float32' and target_fmt == 'hex'     ): st.pack('>f'),
                                    (original_fmt == 'float64' and target_fmt == 'hex'     ): st.pack('>d'),
                                    # from hex
                                    (original_fmt == 'hex'     and target_fmt == 'str'     ): st.unpack('>s'),
                                    (original_fmt == 'hex'     and target_fmt == 'int'     ): st.unpack('>i'),
                                    (original_fmt == 'hex'     and target_fmt == 'uint16'  ): st.unpack('>H'),
                                    (original_fmt == 'hex'     and target_fmt == 'uint32'  ): st.unpack('>L'),
                                    (original_fmt == 'hex'     and target_fmt == 'float32' ): st.unpack('>f'),
                                    (original_fmt == 'hex'     and target_fmt == 'float64' ): st.unpack('>d'),
                                    (Hx_mean_df.iloc[0, 1] == 'error2' or
                                    Hx_mean_df.iloc[0, 2] == 'error2' or
                                    Hx_mean_df.iloc[0, 3] == 'error2' or
                                    Hx_mean_df.iloc[0, 4] == 'error2' or
                                    Hx_mean_df.iloc[0, 5] == 'error2'): "JJ"
                                    })
    new_type = data_type_convert[original_fmt, target_fmt, data]
    return new_type




# # data_type_converter()
# TCP_IP = '127.0.0.1'
# PORT = 6501 # avialable ports: 6501, 6502, 6503, 6504
# server_address = (TCP_IP, PORT)

# # create a TCP/IP socket
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(server_address)

# s.close()

