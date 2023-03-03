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

def dtype_converter(original_fmt, target_fmt, data):
    supported_formats = ['int', 'uint16', 'uint32', 'float32', 'float64', 'hex', 'str']
    if original_fmt in supported_formats and target_fmt in supported_formats:
        try:
            dtype_conv = defaultdict(lambda: None, 
                                            {
                                            # to hex
                                            ('str'    , 'hex'    ): lambda: st.back('>'),
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
            return dtype_conv[(original_fmt, target_fmt)]()
        except:
            print('ValueError: Check if the type of "data" matches with the type specified in "original_fmt"')
    else:
        print("TyPeError: Please check the data types! Supported data formats are: 'int', 'uint16', 'uint32', 'float32', 'float64', 'hex', 'str'")

# def construct_header():
print(bytes.fromhex('0000 0004'))




# # dtype_converter()
# TCP_IP = '127.0.0.1'
# PORT = 6501 # avialable ports: 6501, 6502, 6503, 6504
# server_address = (TCP_IP, PORT)

# # create a TCP/IP socket
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(server_address)

# s.close()
original_fmt = 'int'
target_fmt = 'hex'
supported_formats = ['int', 'uint16', 'uint32', 'float32', 'float64', 'hex', 'str']
data = 4.4
print(dtype_converter(original_fmt, target_fmt, data))