# -*- encoding: utf-8 -*-
'''
@Time    :   2023/02/28 14:52:33
@Author  :   Shixuan Shan 
'''
import socket
from collections import defaultdict
import struct as st
from timeit import default_timer as timer
import numpy as np
import sys
# data types: 'str', 'int'(i), 'uint16'(H), 'uint32'(L), 'float32'(f), 'float64'(d), 'hex'
# big-endian encoded '>'

############################### functions #####################################
#################### basic functions for creating commands ####################
# ! remember to define buffer size!!!!!!!
# create a connection between tcp client and nanonis software
def socket_connect(TCP_IP = '127.0.0.1', PORT = 6501):
    server_address = (TCP_IP, PORT)
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.connect(server_address)
    return sk

# close socket
def socket_close(sk):
    sk.close()

# data type conversion
# ! only support formats in supported_formats list
def dtype_convert(data, original_fmt, target_fmt):
    supported_formats = ['int', 'uint16', 'uint32', 'float32', 'float64', 'bin', 'str', 'bool']
    if original_fmt in supported_formats and target_fmt in supported_formats:
        try:
            dtype_conv = defaultdict(lambda: None, 
                                    {
                                    # to binary
                                    ('str'    , 'bin'): lambda: bytes(data, 'utf-8'),
                                    ('int'    , 'bin'): lambda: st.pack('>i', data),
                                    ('uint16' , 'bin'): lambda: st.pack('>H', data),
                                    ('uint32' , 'bin'): lambda: st.pack('>L', data),
                                    ('float32', 'bin'): lambda: st.pack('>f', data),
                                    ('float64', 'bin'): lambda: st.pack('>d', data),
                                    # from binary
                                    ('bin', 'str'    ): lambda: st.unpack('>%ds' % len(data), data)[0].decode('utf-8'),
                                    ('bin', 'int'    ): lambda: st.unpack('>i', data)[0],
                                    ('bin', 'uint16' ): lambda: st.unpack('>H', data)[0],
                                    ('bin', 'uint32' ): lambda: st.unpack('>L', data)[0],
                                    ('bin', 'float32'): lambda: st.unpack('>f', data)[0],
                                    ('bin', 'float64'): lambda: st.unpack('>d', data)[0]
                                    })
            return dtype_conv[(original_fmt, target_fmt)]()
        except:
            print('ValueError: Check if the type of "data" matches with the type specified in "original_fmt"')
    else:
        print("TyPeError: Please check the data types! Supported data formats are: 'int', 'uint16', 'uint32', 'float32', 'float64', 'hex', 'str'")

# unit conversion function
def unit_convert(data):
    unit_list = ['', 'm', 'u', 'n', 'p', 'f']
    unit_conv ={'' : 1.0,
                'm': 1e-3,
                'u': 1e-6,
                'n': 1e-9,
                'p': 1e-12,
                'f': 1e-15
                }
    if type(data) == str:
        for item in unit_list:
            if item in data:
                significand = float(''.join(char for char in data if char.isdigit() or char =='.'))
                new_data = significand*unit_conv[item]
    else:
        new_data = data
    return new_data

# construct header
def header_construct(command_name, body_size, res = True):
    header_bin_rep =  bytes(command_name, 'utf-8').ljust(32, b'\x00')  # convert command name to binary representation and pad it to 32 bytes long with b'\x00'
    header_bin_rep += dtype_convert(body_size, 'int', 'bin')         # boty size
    header_bin_rep += dtype_convert(1 if res else 0, 'uint16', 'bin') # send response back (1) or not (0)
    header_bin_rep += b'\x00\x00'
    return header_bin_rep

# send command
def cmd_send(sk, data):
    sk.sendall(data)

# receive and decode response message
def res_recv(*varg_fmt, get_header = False, get_arg = True, get_err = True):
    res_bin_rep = sk.recv(1024)
    res_arg = []
    res_err = []

    # parse the header of a response message
    if get_header:
        header_cmd_name = dtype_convert(res_bin_rep[0:32], 'bin', 'str').replace('\x00', '')
        header_body_size = dtype_convert(res_bin_rep[32:36], 'bin', 'int')
        res_arg.append(header_cmd_name)
        res_arg.append(header_body_size)

    # parse the arguments values of a response message
    if get_arg:
        arg_byte_idx = 40
        arg_size_dict = {'int': 4,'uint16': 2,'uint32': 4,'float32': 4,'float64': 8}
        for idx, arg_fmt in enumerate(varg_fmt):
            arg_size = arg_size_dict[arg_fmt]
            arg = dtype_convert(res_bin_rep[arg_byte_idx: arg_byte_idx + arg_size], 'bin', arg_fmt)
            arg_byte_idx += arg_size                                           
            res_arg.append(arg)
        res_bin_rep = res_bin_rep[arg_byte_idx-1:] # for parsing the error in a request or a response

    # parse the error of a response message
    if get_err:
        body_err_status = dtype_convert(res_bin_rep[0:4], 'bin', 'uint32') # error status
        body_err_dsc_size = dtype_convert(res_bin_rep[4:8], 'bin', 'int') # error description size
        body_err_dsc = dtype_convert(res_bin_rep[8:], 'bin', 'str') # error description

        res_err.append(body_err_status)
        res_err.append(body_err_dsc_size)
        res_err.append(body_err_dsc)
    return res_arg, res_err

def BiasSet(sk, bias):
    header = header_construct('Bias.Set', body_size = 4)
    body = dtype_convert(unit_convert(bias), 'float32', 'bin')
    cmd = header+body
    cmd_send(sk, cmd)
    res_recv()

def BiasGet(sk):
    header = header_construct('Bias.Get', body_size=0) # the body size here is the body size of Bias.Get argument 
    cmd_send(sk, header)
    bias = str(res_recv('float32')[0][0]) + 'V'
    return bias


# sk =socket_connect()

# BiasSet(sk, '7')
# BiasGet(sk)
# socket_close(sk)

# start = timer()
# stop = timer()
# print(stop-start)

# # dtype_convert()
# TCP_IP = '127.0.0.1'
# PORT = 6501 # avialable ports: 6501, 6502, 6503, 6504
# server_address = (TCP_IP, PORT)

# # create a TCP/IP socket
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(server_address)

# s.close()
original_fmt = 'bin'
target_fmt = 'str'

data = b'FolMe XYPosGet'
# import struct

byte_string = b'\x48\x65\x6c\x6c\x6f\x20\x57\x6f\x72\x6c\x64'   # The byte-like string to be unpacked
string = 455


# t1 = timer()
# print(dtype_convert(np.array(string, dtype = '>i').tobytes(), 'bin', 'int'))
# t2 = timer()
# print(t2-t1)

# t3 = timer()
# print(np.frombuffer(np.array(string, dtype = '>i').tobytes(), dtype = '>i')[0])
# t4 = timer()
# print(t4-t3)
data = np.array([1, 2, 3], dtype=np.int32)
dtype_cvt_dict = defaultdict(lambda: None, {
        ('1dstr' or 'str', 'bin'): lambda data: np.array(data, dtype = '>S').tobytes(),
        ('int' or '1dint', 'bin'): lambda data: np.array(data, dtype = '>i').tobytes(),
    })

key = ('1dint', 'bin')
value = dtype_cvt_dict[key](data)
print(value)
# string = struct.unpack('%ds' % len(byte_string), byte_string)[0].decode('utf-8')  # Convert the byte-like string to a string