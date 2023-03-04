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
    supported_formats = ['int', 'uint16', 'uint32', 'float32', 'float64', 'bin', 'str']
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

def construct_header(command_name):
    return command_name.ljust(32, b'\x00')



# # dtype_converter()
# TCP_IP = '127.0.0.1'
# PORT = 6501 # avialable ports: 6501, 6502, 6503, 6504
# server_address = (TCP_IP, PORT)

# # create a TCP/IP socket
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(server_address)

# s.close()
original_fmt = 'bin'
target_fmt = 'str'

data = b'\x48\x65\x6c\x6c\x6f\x20\x57\x6f\x72\x6c\x64'

print(construct_header('FolMe.XYPosGet'))

# import struct

# byte_string = b'\x48\x65\x6c\x6c\x6f\x20\x57\x6f\x72\x6c\x64'   # The byte-like string to be unpacked
# string = struct.unpack('%ds' % len(byte_string), byte_string)[0].decode('utf-8')  # Convert the byte-like string to a string
# print(string)