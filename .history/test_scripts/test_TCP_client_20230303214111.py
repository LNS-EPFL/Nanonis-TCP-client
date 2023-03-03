# -*- encoding: utf-8 -*-
'''
@Time    :   2023/02/28 14:52:33
@Author  :   Shixuan Shan 
'''
import socket
from collections import defaultdict
import struct as st
from timeit import default_timer as timer

# data types: 'str', 'int'(i), 'uint16'(H), 'uint32'(L), 'float32'(f), 'float64'(d), 'hex'
# big-endian encoded '>'

############################### functions #####################################
#################### basic functions for creating commands ####################
def socket_connect(TCP_IP = '127.0.0.1', PORT = 6501):
    server_address = (TCP_IP, PORT)
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.connect(server_address)
    return sk

def socket_close(sk):
    sk.close()

# only support formats in supported_formats list
def data_type_converter(original_fmt, target_fmt, data):
    supported_formats = ['int', 'uint16', 'uint32', 'float32', 'float64', 'hex', 'str']
    if original_fmt and target_fmt in supported_formats:
        data_type_convert = defaultdict(lambda: None, 
                                        {
                                        # to hex
                                        # (original_fmt == 'str'     and target_fmt == 'hex'     ): 'a',
                                        ('int'    , 'hex'    ): lambda: st.pack('>i', data).hex(),
                                        ('uint16' , 'hex'    ): lambda: st.pack('>H', data).hex(),
                                        ('uint32' , 'hex'    ): lambda: st.pack('>L', data).hex(),
                                        ('float32', 'hex'    ): lambda: st.pack('>f', data).hex(),
                                        ('float64', 'hex'    ): lambda: st.pack('>d', data).hex(),
                                        # from hex
                                        ('hex'    , 'str'    ): lambda: bytes.fromhex(data).decode('utf-8'),
                                        ('hex'    , 'int'    ): lambda: st.unpack('>i', bytes.fromhex(data))[0],
                                        ('hex'    , 'uint16' ): lambda: st.unpack('>H', bytes.fromhex(data))[0],
                                        ('hex'    , 'uint32' ): lambda: st.unpack('>L', bytes.fromhex(data))[0],
                                        ('hex'    , 'float32'): lambda: st.unpack('>f', bytes.fromhex(data))[0],
                                        ('hex'    , 'float64'): lambda: st.unpack('>d', bytes.fromhex(data))[0]
                                        })
        return data_type_convert[(original_fmt, target_fmt)]()
    else:
        print("Please check the data formats! Supported data formats are: 'int', 'uint16', 'uint32', 'float32', 'float64', 'hex', 'str'")


# # data_type_converter()
# TCP_IP = '127.0.0.1'
# PORT = 6501 # avialable ports: 6501, 6502, 6503, 6504
# server_address = (TCP_IP, PORT)

# # create a TCP/IP socket
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(server_address)

# s.close()
original_fmt = 'infdt'
target_fmt = 'hex'
supported_formats = ['int', 'uint16', 'uint32', 'float32', 'float64', 'hex', 'str']
data = 4
print(data_type_converter(original_fmt, target_fmt, 10))