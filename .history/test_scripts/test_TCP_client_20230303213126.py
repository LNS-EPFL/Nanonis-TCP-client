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

def data_converter_2(original_fmt, target_fmt, data):
    if original_fmt == 'int' and target_fmt == 'hex':
        return st.pack('>i', data).hex()
    elif original_fmt == 'uint16' and target_fmt == 'hex':
        return st.pack('>H', data).hex()
    elif original_fmt == 'uint32' and target_fmt == 'hex':
        return st.pack('>L', data).hex()
    elif original_fmt == 'float32' and target_fmt == 'hex':
        return st.pack('>f', data).hex()
    elif original_fmt == 'float64' and target_fmt == 'hex':
        return st.pack('>d', data).hex()
    elif original_fmt == 'hex' and target_fmt == 'str':
        bytes.fromhex(data).decode('utf-8')
    elif original_fmt == 'hex' and target_fmt == 'int':
        return st.unpack('>i', bytes.fromhex(data))[0]
    elif original_fmt == 'hex' and target_fmt == 'uint16':
        return st.unpack('>H', bytes.fromhex(data))[0]
    elif original_fmt == 'hex' and target_fmt == 'uint32':
        return st.unpack('>L', bytes.fromhex(data))[0]
    elif original_fmt == 'hex' and target_fmt == 'float32':
        return st.unpack('>f', bytes.fromhex(data))[0]
    elif original_fmt == 'hex' and target_fmt == 'float64':
        return st.unpack('>d', bytes.fromhex(data))[0]
    



# # data_type_converter()
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
data = 4
# if original_fmt and target_fmt in supported_formats:
start_dict = timer()
data_type_converter(original_fmt, target_fmt, data)
stop_dict = timer()
print(stop_dict-start_dict)

start_dict1 = timer()
data_converter_2(original_fmt, target_fmt, data)
stop_dict1 = timer()
print(stop_dict1-start_dict1)