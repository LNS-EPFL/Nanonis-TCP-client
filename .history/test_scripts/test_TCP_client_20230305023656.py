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

# ! only support formats in supported_formats list
def dtype_convert(original_fmt, target_fmt, data):
    supported_formats = ['int', 'uint16', 'uint32', 'float32', 'float64', 'bin', 'str', 'bool']
    if original_fmt in supported_formats and target_fmt in supported_formats:
        try:
            dtype_conv = defaultdict(lambda: None, 
                                    {
                                    # to binary
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

def header_construct(command_name, body_size, res = True):
    header_bin_rep =  bytes(command_name, 'utf-8').ljust(32, b'\x00')  # convert command name to binary representation and pad it to 32 bytes long with b'\x00'
    header_bin_rep += dtype_convert('int', 'bin', body_size)         # boty size
    header_bin_rep += dtype_convert('uint16', 'bin', 1 if res else 0) # send response back (1) or not (0)
    header_bin_rep += b'\x00\x00'
    return header_bin_rep

# todo: construct command
def cmd_construct(header, body):
    return

# todo: send command
def cmd_send(data):
    socket.sendall(data)

# todo: receive and decode response message
def res_recv(*varg):
    res = socket.receive()
    return

# 


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

data = b'FolMe.XYPosGet\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

print(unit_convert(78))
# import struct

# byte_string = b'\x48\x65\x6c\x6c\x6f\x20\x57\x6f\x72\x6c\x64'   # The byte-like string to be unpacked
# string = struct.unpack('%ds' % len(byte_string), byte_string)[0].decode('utf-8')  # Convert the byte-like string to a string
# print(string)