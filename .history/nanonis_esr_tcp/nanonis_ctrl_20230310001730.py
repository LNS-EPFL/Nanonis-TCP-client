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

# recommend to construct body first so that you don't need to calculate the body size by yourself
######################################## Bias Module #############################################
    def BiasSet(self, bias):
        self.bias = self.tcp.unit_cvt(bias)
        if self.bias > 10:
            raise ValueError('The maximum allowed bias is 10V. Please check your input! Bias has been set to 0 to protect the tip!')    
        
        body = self.tcp.dtype_cvt(self.bias, 'float32', 'bin')
        header = self.tcp.header_construct('Bias.Set', body_size = len(body))
        cmd = header+body

        self.tcp.cmd_send(cmd)

        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        print(f'The bias voltage is set to {bias}V')

    def BiasGet(self):
        header = self.tcp.header_construct('Bias.Get', body_size=0) # the body size here is the body size of Bias.Get argument 

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('float32')

        self.tcp.print_err(res_err)
        self.bias = str(res_arg[0]) + 'V' # first [0] gives the res_arg list, second [0] gives the bias value in the list
        print(f'Current bias: {self.bias}')
        return self.bias
    
    def BiasRangeSet(): 
        return print('function in progress......')
    
    def BiasRangeGet():
        return print('function in progress......')
    
    def BiasCalibrSet():
        return print('function in progress......')

    def BiasCalibrGet():
        return print('function in progress......')
    
    def BiasPulse(self, bias_pulse_width, bias_value, wait_until_done = False, zctrl_on_hold = 1, pulse_abs_rel = 2):
        bias_pulse_width = self.tcp.unit_cvt(bias_pulse_width)
        bias_value = self.tcp.unit_cvt(bias_value)
        if bias_value > 10:
            raise ValueError('The maximum allowed bias is 10V. Please check your input! Bias has been set to 0 to protect the tip!') 
        
        # recommend to construct body first so that you don't need to calculate the body size by yourself
        body  = self.tcp.dtype_cvt(wait_until_done, 'uint32', 'bin')
        body += self.tcp.dtype_cvt(bias_pulse_width, 'float32', 'bin')
        body += self.tcp.dtype_cvt(bias_value, 'float32', 'bin')
        body += self.tcp.dtype_cvt(zctrl_on_hold, 'uint16', 'bin')
        body += self.tcp.dtype_cvt(pulse_abs_rel, 'uint16', 'bin')
        header = self.tcp.header_construct('Bias.Pulse', body_size = len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, _, res_err= self.tcp.res_recv()

        self.tcp.print_err(res_err)
        print(f'Bias pulse finished. \n Pulse width: {bias_pulse_width}s \n Pulse value: {bias_value}V')

# todo
######################################## Bias Spectroscopy Module #############################################
    def BiasSpectrOpen(self):
        header = self.tcp.header_construct('BiasSpectr.Open', body_size=0)

        self.tcp.cmd_send(header)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        print('Bias Spectroscopy opened.')

    # ! todo: finish this func
    def BiasSpectrStart(self, save_base_name, get_data = 1):
        save_base_name_size = len(save_base_name)

        body  = self.tcp.dtype_cvt(get_data, 'uint32', 'bin')
        body += self.tcp.dtype_cvt(save_base_name_size, 'int', 'bin')
        body += self.tcp.dtype_cvt(save_base_name, 'str', 'bin')
        header = self.tcp.header_construct('BiasSpectr.Start', body_size = len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, res_arg, res_err= self.tcp.res_recv('int', 'int', '1dstr', 'int', 'int', '2dfloat32', )
        print(res_arg)

        self.tcp.print_err(res_err)

    def BiasSpectrStop(self):
        header = self.tcp.header_construct('BiasSpectr.Stop', body_size=0)

        self.tcp.cmd_send(header)
        _, _, res_err = self.tcp.res_recv()

        self.tcp.print_err(res_err)
        print('Bias spectroscopy measurement stoped.')

    def BiasSpectrStatusGet(self):
        header = self.tcp.header_construct('BiasSpectr.StatusGet', body_size=0)

        self.tcp.cmd_send(header)
        _, res_arg, res_err = self.tcp.res_recv('uint32')
        self.tcp.print_err(res_err)
        if res_arg[0] == 1:
            print('A bias spectroscopy measurement is in process......')
        else:
            print('No bias spectroscopy measurement in process.') 
  
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
# ccc.BiasSet('7')
# ccc.BiasGet()
ccc.BiasPulse('600m', '7')
ccc.BiasSpectrStart('dgyuf')
