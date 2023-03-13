# -*- encoding: utf-8 -*-
'''
@Time    :   2023/03/04 01:54:34
@Author  :   Shixuan Shan 
'''
from tcp_ctrl import tcp_ctrl
import numpy as np

class nanonis_ctrl:
    def __init__(self, tcp):
        self.tcp = tcp

######################################## Bias Module #############################################
    def BiasSet(self, bias):
        self.bias = self.tcp.unit_cvt(bias)
        if self.bias > 10:
            raise ValueError('The maximum allowed bias is 10V. Please check your input! Bias has been set to 0 to protect the tip!')    
        
        # recommend to construct body first so that you don't need to calculate the body size by yourself
        body = self.tcp.dtype_cvt(self.bias, 'float32', 'bin')
        header = self.tcp.header_construct('Bias.Set', body_size = len(body))
        cmd = header+body


        self.tcp.cmd_send(cmd)

        res_header, res_arg, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        print(f'The bias voltage is set to {bias}V')

    def BiasGet(self):
        return print('function in progress......')

    
    def BiasRangeSet(): 
        return print('function in progress......')
    
    def BiasRangeGet():
        return print('function in progress......')
    
    def BiasCalibrSet():
        return print('function in progress......')

    def BiasCalibrGet():
        return print('function in progress......')
    
    def BiasPulse(self, bias_pulse_width, bias_value, wait_until_done = False, zctrl_on_hold = 1, pulse_abs_rel = 2):
        return print('function in progress......')

    
# todo
######################################## Bias Spectroscopy Module #############################################
    def BiasSpectrOpen(self):
        header = self.tcp.header_construct('BiasSpectr.Open', body_size=0)

        self.tcp.cmd_send(header)
        _, err = self.tcp.res_recv()

        self.tcp.print_err(err)
        print('Bias Spectroscopy opened.')

    # ! todo: finish this func
    def BiasSpectrStart(self, save_base_name, get_data = 1):
        save_base_name_str_size = len(save_base_name)
        body  = self.tcp.dtype_cvt(get_data, 'uint32', 'bin')
        body += self.tcp.dtype_cvt(save_base_name_str_size, 'int', 'bin')
        body += self.tcp.dtype_cvt(save_base_name, 'str', 'bin')
        header = self.tcp.header_construct('BiasSpectr.Start', body_size = len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        arg, err = self.tcp.res_recv()

     
    def BiasSpectrStop(self):
        header = self.tcp.header_construct('BiasSpectr.Stop', body_size=0)

        self.tcp.cmd_send(header)
        _, err = self.tcp.res_recv()

        self.tcp.print_err(err)
        print('Bias spectroscopy measurement stoped.')

    def BiasSpectrStatusGet(self):
        header = self.tcp.header_construct('BiasSpectr.StatusGet', body_size=0)

        self.tcp.cmd_send(header)
        arg, err = self.tcp.res_recv('uint32')

        self.tcp.print_err(err)
        if arg[0] == 1:
            print('A bias spectroscopy measurement is in process......')
        else:
            print('Currently there is no bias spectroscopy measurement.')      
######################################## Current Module #############################################
######################################## Z-controller Module #############################################
######################################## Safe Tip Module #############################################
######################################## Auto Approach Module #############################################
######################################## Scan Module #############################################
######################################## Follow Me Module #############################################
######################################## Tip Shaper Module #############################################
######################################## Atom Tracking Module #############################################
######################################## Lock-in Module #############################################

tcp = tcp_ctrl()
ccc = nanonis_ctrl(tcp)
ccc.BiasSet('300p')
# ccc.BiasGet()
# ccc.BiasPulse('500m', 7)