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
    def dtype_convert(self, data, original_fmt, target_fmt):
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
                                        ('bin', 'str'    ): lambda: st.unpack('>%ds' % len(data), data)[0].decode('utf-8'), # unpack a string with a certain length
                                        ('bin', 'int'    ): lambda: st.unpack('>i', data)[0],
                                        ('bin', 'uint16' ): lambda: st.unpack('>H', data)[0],
                                        ('bin', 'uint32' ): lambda: st.unpack('>L', data)[0],
                                        ('bin', 'float32'): lambda: st.unpack('>f', data)[0],
                                        ('bin', 'float64'): lambda: st.unpack('>d', data)[0]
                                        })
                return dtype_conv[(original_fmt, target_fmt)]()
            except TypeError:
                print('Check if the type of "data" matches with the type specified in "original_fmt"')
        else:
            raise TypeError("Please check the data types! Supported data formats are: 'int', 'uint16', 'uint32', 'float32', 'float64', 'hex', 'str'")

    # unit conversion function
    def unit_convert(self, data):
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
        self.header_bin_rep += self.dtype_convert(body_size, 'int', 'bin')         # boty size
        self.header_bin_rep += self.dtype_convert(1 if res else 0, 'uint16', 'bin') # send response back (1) or not (0)
        self.header_bin_rep += b'\x00\x00'
        return self.header_bin_rep

    # send command to nanonis tcp server
    def cmd_send(self, data):
        self.sk.sendall(data)

    # receive and decode response message
    def res_recv(self, *varg_fmt, get_header = False, get_arg = True, get_err = True):
        res_bin_rep = self.sk.recv(1024)
        res_arg = []
        res_err = []

        # parse the header of a response message
        if get_header:
            header_cmd_name = self.dtype_convert(res_bin_rep[0:32], 'bin', 'str').replace('\x00', '')
            header_body_size = self.dtype_convert(res_bin_rep[32:36], 'bin', 'int')
            res_arg.append(header_cmd_name)
            res_arg.append(header_body_size)

        # parse the arguments values of a response message
        if get_arg:
            arg_byte_idx = 40
            arg_size_dict = {'int': 4,'uint16': 2,'uint32': 4,'float32': 4,'float64': 8}
            for idx, arg_fmt in enumerate(varg_fmt):
                arg_size = arg_size_dict[arg_fmt]
                arg = self.dtype_convert(res_bin_rep[arg_byte_idx: arg_byte_idx + arg_size], 'bin', arg_fmt)
                arg_byte_idx += arg_size                                           
                res_arg.append(arg)
            res_bin_rep = res_bin_rep[arg_byte_idx-1:] # for parsing the error in a request or a response

        # parse the error of a response message
        if get_err:
            body_err_status = self.dtype_convert(res_bin_rep[0:4], 'bin', 'uint32') # error status
            body_err_dsc_size = self.dtype_convert(res_bin_rep[4:8], 'bin', 'int') # error description size
            body_err_dsc = self.dtype_convert(res_bin_rep[8:], 'bin', 'str') # error description

            res_err.append(body_err_status)
            res_err.append(body_err_dsc_size)
            res_err.append(body_err_dsc)
        return res_arg, res_err