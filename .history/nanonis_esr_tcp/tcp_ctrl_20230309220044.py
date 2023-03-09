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
    # create a connection between tcp client and nanonis software
    def __init__(self, TCP_IP = '127.0.0.1', PORT = 6501, buffersize = 512):
        self.server_addr = (TCP_IP, PORT)
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sk.connect(self.server_addr)
        self.buffersize = buffersize

    # close socket
    def socket_close(self):
        self.sk.close()

    # data type conversion. 
    '''
       - the arguments returned by this function are bytelike strings when converting to 'bin' and data in requested format and the length of the data when converting from 'bin'
       - arg is for 1d or 2d array conversions. 
            for 2d arrays: arg should be a tuple in the form of (num_rows, num_cols), eg. (41, 2)
            for 1d string array: put (size, 1) instead of the size directly
    '''
    def dtype_cvt(self, data, original_fmt, target_fmt, *arg):  
        self.supported_dtypes = ['bin', 'str', 'int', 'uint16', 'uint32', 'float32', 'float64',
                                 '1dstr', '1dint', '1duint32', '1dfloat32',
                                 '2dstr', '2dfloat32']
        
        ##############* TO BYTES ####################
        #* str to binary
        if original_fmt == 'str' and target_fmt == 'bin': 
            return np.array(data, '>S').tobytes()
        #* 1dstr to binary
        elif original_fmt == '1dstr' and target_fmt == 'bin': 
            return print('in progress......')        
        #* int32 to binary
        elif original_fmt == 'int' or '1dint' and target_fmt == 'bin': 
            return np.array(data, '>i').tobytes()
        #* unsigned int16 to binary
        elif original_fmt == 'uint16' and target_fmt == 'bin': 
            return np.array(data, '>H').tobytes()
        #* unsigned int32 to binary
        elif original_fmt == 'uint32' or '1duint32' and target_fmt == 'bin': 
            return np.array(data, '>L').tobytes()
        #* float32 to binary
        elif original_fmt == 'float32' or '1dfloat32' or '2dfloat32' and target_fmt == 'bin': 
            return np.array(data, '>f').tobytes()
        #* float64 to binary   
        elif original_fmt == 'float64' and target_fmt == 'bin': 
            return np.array(data, '>d').tobytes()
        
        #############* FROM BYTES ####################
        #* binary to string (expression after '%' gives the size of the string in bytes)
        elif original_fmt == 'bin' and target_fmt == 'str':
            data_cvted = np.frombuffer(data, '>%dS' % arg)[0].decode('utf-8') 
            return [data_cvted[0], len(data)]
        #* binary to 1d or 2d string
        elif original_fmt == 'bin' and target_fmt == '1dstr' or '2dstr': 
            ele_idx = 0
            str_array= []
            for idx in range(np.prod(arg)):
                ele_size = np.frombuffer(data[ele_idx: ele_idx+4], '>i')[0]
                ele_idx += 4

                ele = np.frombuffer(data[ele_idx: ele_idx + ele_size], '>%dS' % ele_size)[0].decode('utf-8')
                ele_idx += ele_size

                str_array.append(ele)
            return [np.array(str_array).reshape(arg), len(data)]
        #* binary to int & 1d int
        elif original_fmt == 'bin' and target_fmt == 'int' or '1dint': 
            data_cvted = np.frombuffer(data, '>i')
            if len(data_cvted) == 1:
                data_cvted = data_cvted[0]
            return [data_cvted, len(data)] 
        #* binary to unsigned int16 
        elif original_fmt == 'bin' and target_fmt == 'uint16': 
            data_cvted = np.frombuffer(data, '>H')
            if len(data_cvted) == 1:
                data_cvted = data_cvted[0]
            return [data_cvted, len(data)]
        #* binary to unsigned int32 and 1d unsigned int32
        elif original_fmt == 'bin' and target_fmt == 'uint32' or '1duint32': 
            data_cvted = np.frombuffer(data, '>L')
            if len(data_cvted) == 1:
                data_cvted = data_cvted[0]
            return [data_cvted, len(data)]
        #* binary to float32 and 1d float32
        elif original_fmt == 'bin' and target_fmt == 'float32' or '1dfloat32': 
            data_cvted = np.frombuffer(data, '>f')
            if len(data_cvted) == 1:
                data_cvted = data_cvted[0]
            return data_cvted, len(data)
        #* binary to 2d float32
        elif original_fmt == 'bin' and target_fmt == '2dfloat32': 
            return [np.frombuffer(data, '>f').reshape(arg), len(data)]
        #* binary to float64
        elif original_fmt == 'bin' and target_fmt == 'float64' or '1dfloat64':
            data_cvted = np.frombuffer(data, '>d') 
            return [[0], len(data)]


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
                    return significand*unit_conv[item]
        else:
            return data

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
                if arg_fmt in arg_size_dict.keys():
                    arg, arg_size = self.dtype_cvt(res_bin_rep[arg_byte_idx: arg_byte_idx + arg_size_dict[arg_fmt]], 'bin', arg_fmt)
                    arg_byte_idx += arg_size
                    res_arg.append(arg)

                elif arg_fmt == 'str': 
                    arg_size, len_int = self.dtype_cvt(res_bin_rep[arg_byte_idx: arg_byte_idx + arg_size_dict['int']], 'bin', 'int')
                    arg_byte_idx += len_int
                    arg, _ = self.dtype_cvt(res_bin_rep[arg_byte_idx: arg_byte_idx + arg_size], 'bin', arg_fmt)
                    arg_byte_idx += arg_size
                    res_arg.append(arg)

                elif arg_fmt == '1dstr' or '2dstr':
                    num_rows = res_arg[idx-2] if arg_fmt == '2dstr' else res_arg[idx-1]
                    num_cols = res_arg[idx-1] if arg_fmt == '2dstr' else 1

                    # calculate the total size of the string array
                    interal_byte_idx = arg_byte_idx
                    for ele_idx in range(num_rows*num_cols): 
                        ele_size, len_int = self.dtype_cvt(res_bin_rep[interal_byte_idx: interal_byte_idx + arg_size_dict['int']], 'bin', 'int')
                        interal_byte_idx += ele_size + len_int
                    array_size = interal_byte_idx - arg_byte_idx

                    arg, arg_size = self.dtype_cvt(res_bin_rep[arg_byte_idx: arg_byte_idx + array_size], 'bin', arg_fmt, (num_rows, num_cols))
                    arg_byte_idx += arg_size
                    if array_size == arg_size:
                        res_arg.append(arg)
                    else:
                        print('There might be an error when parsing the string array. Possible causes could be: \n 1) the argument format (arg_fmt) input is wrong. \n 2) the previous arg_fmt is wrong. ' )
                        res_arg.append(arg)

                elif arg_fmt in ['1dint', '1duint32', '1dfloat32', '1dfloat64', ]:
                    num_ele = res_arg[idx-1]
                    array_size = num_ele * arg_size_dict[arg_fmt[2:]]
                    arg, arg_size = self.dtype_cvt(res_bin_rep[arg_byte_idx: arg_byte_idx + array_size])
                    arg_byte_idx += arg_size
                    res_arg.append(arg)



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
