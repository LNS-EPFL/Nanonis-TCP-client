# -*- encoding: utf-8 -*-
'''
@Time    :   2023/03/04 01:54:29
@Author  :   Shixuan Shan 
'''

# data types: 'str', 'int'(i), 'uint16'(H), 'uint32'(L), 'float32'(f), 'float64'(d), 'hex'
# big-endian encoded '>'
############################### packages ######################################
import socket
from collections import defaultdict
import struct as st
import pandas as pd
import numpy as np

class tcp_ctrl:
############################### functions #####################################
#################### basic functions for creating commands ####################
    # ! remember to define buffer size!!!!!!!
    # create a connection between tcp client and nanonis software
    def __init__(self, TCP_IP = '127.0.0.1', PORT = 6501, buffersize = 512):
        self.server_addr = (TCP_IP, PORT)
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sk.connect(self.server_addr)
        self.buffersize = buffersize

    # close socket
    def socket_close(self):
        self.sk.close()

    # data type conversion
    # ! only support formats in supported_formats list
    def dtype_cvt(self, data, original_fmt, target_fmt): # data_size is the length of an 1d array (8 for example)or the number of rows and columns of a 2d array ([2,2] for example) 
        supported_formats = ['bin', 'str', 'int', 'uint16', 'uint32', 'float32', 'float64']
        dtype_cvt_dict = defaultdict(lambda: None, 
                                     {
                                     # to binary
                                      ('str'    , 'bin'): lambda: np.array(data, dtype = '>S').tobytes(),
                                      ('int'    , 'bin'): lambda: np.array(data, dtype = '>i').tobytes(),
                                      ('uint16' , 'bin'): lambda: np.array(data, dtype = '>H').tobytes(),
                                      ('uint32' , 'bin'): lambda: np.array(data, dtype = '>L').tobytes(),
                                      ('float32', 'bin'): lambda: np.array(data, dtype = '>f').tobytes(),
                                      ('float64', 'bin'): lambda: np.array(data, dtype = '>d').tobytes(),
                                      # from binary
                                      ('bin', 'str'    ): lambda: np.frombuffer(data, '>%dS' % len(data)),
                                      ('bin', 'int'    ): lambda: np.frombuffer(data, '>i'), 
                                      ('bin', 'uint16' ): lambda: np.frombuffer(data, '>H'),
                                      ('bin', 'uint32' ): lambda: np.frombuffer(data, '>L'),
                                      ('bin', 'float32'): lambda: np.frombuffer(data, '>f'),
                                      ('bin', 'float64'): lambda: np.frombuffer(data, '>d')
                                     })
        if original_fmt in supported_formats and target_fmt in supported_formats:
            try:
                return dtype_cvt_dict[(original_fmt, target_fmt)]()
            except TypeError:
                print('Check if the type of "data" matches with the type specified in "original_fmt"')
        else:
            raise TypeError("Please check the data types! Supported data types are: 'int', 'uint16', 'uint32', 'float32', 'float64', 'hex', 'str'")

    # 1d and 2d array conversion function
    def array_dtype_cvt(self, data, original_fmt, target_fmt, array_size): # array size can be a integer like 7 (for 1d arrays) or a list [7,8] (for 2d arrays)
        supported_formats = ['bin', '1dstr', '1dint32', '1duint32', '1dfloat32', '1dfloat64', '2dfloat32', '2dstr']
        array_cvt_dict = defaultdict(lambda: None,
                                     {
                                      # to binary
                                      ('1dstr'    , 'bin'): lambda: np.array(data, dtype = '>S').tobytes(), 
                                      ('1dint'    , 'bin'): lambda: np.array(data, dtype = '>i').tobytes(),
                                      ('1duint32' , 'bin'): lambda: np.array(data, dtype = '>L').tobytes(),
                                      ('1dfloat32', 'bin'): lambda: np.array(data, dtype = '>f').tobytes(),
                                      ('1dfloat64', 'bin'): lambda: np.array(data, dtype = '>d').tobytes(),
                                      ('2dfloat32', 'bin'): lambda: np.array(data, dtype = '>f').tobytes(),
                                      ('2dstr'    , 'bin'): lambda: np.array(data, dtype = '>S').tobytes(), 
                                      # from binary
                                      ('bin', '1dstr'    ): lambda: 
                                      ('bin', '1dint32'  ): lambda:  
                                      ('bin', '1duint32' ): lambda:
                                      ('bin', '1dfloat32'): lambda: 
                                      ('bin', '1dfloat64'): lambda: 
                                      ('bin', '2dfloat32'): lambda:
                                      ('bin', '2dstr'    ): lambda:  
                                     }
                                    )
        if original_fmt in supported_formats and target_fmt in supported_formats:
            try:
                return array_cvt_dict[(original_fmt, target_fmt)]()
            except TypeError:
                print('Check if the type of "data" matches with the type specified in "original_fmt"')
        else:
            raise TypeError("Please check the data types! Supported data types are: 'int', 'uint16', 'uint32', 'float32', 'float64', 'hex', 'str'")
    

    # unit conversion function
    def unit_cvt(self, data):
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
                    significand = float(''.join(char for char in data if char.isdigit() or char in ['.', '-']))
                    new_data = significand*unit_conv[item]
        else:
            new_data = data
        return new_data

    # construct header
    def header_construct(self,command_name, body_size, res = True):
        self.header_bin_rep =  bytes(command_name, 'utf-8').ljust(32, b'\x00')  # convert command name to binary representation and pad it to 32 bytes long with b'\x00'
        self.header_bin_rep += self.dtype_cvt(body_size, 'int', 'bin')         # boty size
        self.header_bin_rep += self.dtype_cvt(1 if res else 0, 'uint16', 'bin') # send response back (1) or not (0)
        self.header_bin_rep += b'\x00\x00'
        return self.header_bin_rep

    # send command to nanonis tcp server
    def cmd_send(self, data):
        self.sk.sendall(data)

    # receive and decode response message
    # ! todo check this func
        '''
        supported argument formats (arg_fmt) are: 
            'str', 'int', 'uint16', 'uint32', 'float32', 'float64', 
            '1dstr', '1dint', '1duint8'(noy supported now), '1duint32', 
            '1dfloat32', '1dfloat64', '2dfloat32', '2dstr'
        '''

    def res_recv(self, *varg_fmt, get_header = True, get_arg = True, get_err = True):
        res_bin_rep = self.sk.recv(self.buffersize)
        res_arg = []
        res_err = pd.DataFrame()
        res_header = pd.DataFrame()

        # parse the header of a response message
        if get_header:
            res_header['commmand name'] = self.dtype_cvt(res_bin_rep[0:32], 'bin', 'str').replace('\x00', '') # drop all '\x00' in the string
            res_header['body size'] = self.dtype_cvt(res_bin_rep[32:36], 'bin', 'int')            

        # parse the arguments values of a response message
        if get_arg:
            arg_byte_idx = 40   
            arg_size_dict = {'int': 4,'uint16': 2,'uint32': 4,'float32': 4,'float64': 8}
            for idx, arg_fmt in enumerate(varg_fmt):
                if arg_fmt in arg_size_dict.keys(): # arg_fmts that are: 'int', 'uint16', 'uint32', 'float32', 'float64'
                    arg_size = arg_size_dict[arg_fmt]
                    arg = self.dtype_cvt(res_bin_rep[arg_byte_idx: arg_byte_idx + arg_size], 'bin', arg_fmt)
                    arg_byte_idx += arg_size                                           
                    res_arg.append(arg)
                    
                elif arg_fmt == 'str':
                    int_size = arg_size_dict['int'] # the size of an integer 32 that give the size of the following string
                    str_size = self.dtype_cvt(res_bin_rep[arg_byte_idx: arg_byte_idx + int_size], 'bin', 'int') # the size of the string 
                    arg_byte_idx += int_size

                    arg = self.dtype_cvt(res_bin_rep[arg_byte_idx: arg_byte_idx + str_size], 'bin', arg_fmt) # convert the string from binary
                    arg_byte_idx += str_size                                           
                    res_arg.append(arg)

                elif arg_fmt == '1dstr':
                    str_1d = []
                    array_size = res_arg[idx-1] # array size in bytes
                    num_of_ele = res_arg[idx-2] # number of elements
                    for ele_idx in range(num_of_ele): 
                        int_size = arg_size_dict['int'] # the size of the integer that indicate the string size
                        ele_size = self.dtype_cvt(res_bin_rep[arg_byte_idx: arg_byte_idx + int_size], 'bin', 'int') # the size of the string element
                        arg_byte_idx += int_size

                        ele = self.dtype_cvt(res_bin_rep[arg_byte_idx: arg_byte_idx + ele_size], 'bin', arg_fmt)
                        arg_byte_idx += ele_size
                        str_1d.append(ele)
                    res_arg.append(str_1d)

                elif arg_fmt in ['1dint', '1duint32', '1dfloat32', '1dfloat64']: # 1duint8 currently not supported
                    num_1d = []
                    array_size = res_arg[idx-1] # array size in bytes
                    ele_size = arg_size_dict[arg_fmt]
                    if array_size % ele_size == 0:
                        num_of_ele = round(array_size//ele_size) # number of elements in the array
                    else:
                        print(f'array size ({array_size}) is not a multiple of element size ({ele_size}). Please check if the input "arg_fmt" is correct.')

                    for ele_idx in range(num_of_ele):
                        ele = self.dtype_cvt(res_bin_rep[arg_byte_idx: arg_byte_idx + ele_size], 'bin', arg_fmt[2:]) # '2:' --> leaving out '1d' in the fmt string
                        arg_byte_idx += ele_size
                        num_1d.append(ele)
                    res_arg.append(num_1d)
                    
                elif arg_fmt == '2dfloat32':
                    num_of_rows = res_arg[idx-2] # the number of rows of the 2d array
                    num_of_cols = res_arg[idx-1] # the number of columns of the 2d array


                elif arg_fmt == '2dstr':
                    num_of_rows = res_arg[idx-2] # the number of rows of the 2d array
                    num_of_cols = res_arg[idx-1] # the number of columns of the 2d array

                elif arg_fmt == '1duint8':
                    print('this part of the function is still in progress...')
                
                else: 
                    raise TypeError('Please check the data types! Supported data types are: \
                                    "str", "int", "uint16", "uint32", "float32", "float64", \
                                    "1dstr", "1dint", "1duint8" (currently unavailable), "1duint32", "1dfloat32", "1dfloat64", \
                                    "2dfloat32", "2dstr"')
            res_bin_rep = res_bin_rep[arg_byte_idx-1:] # for parsing the error in a request or a response

        # parse the error of a response message
        if get_err:
            res_err['error status'] = self.dtype_cvt(res_bin_rep[0:4], 'bin', 'uint32') # error status
            res_err['error body size'] = self.dtype_cvt(res_bin_rep[4:8], 'bin', 'int') # error description size
            res_err['error description'] = self.dtype_cvt(res_bin_rep[8:], 'bin', 'str') # error description

        print(res_arg)
        return res_header, res_arg, res_err
    
    def print_err(self, res_err):
        if not res_err.empty:
            print(res_err['error description'])
