# -*- encoding: utf-8 -*-
'''
@Time    :   2023/03/04 01:54:34
@Author  :   Shixuan Shan 
'''
from tcp_ctrl import tcp_ctrl

class nanonis_ctrl:
    def __init__(self, tcp):
        self.tcp = tcp

######################################## Bias Module #############################################
    def BiasSet(self, bias):
        self.bias = self.tcp.unit_convert(bias)
        if self.bias > 10:
            raise ValueError('The maximum allowed bias is 10V. Please check your input! Bias has been set to 0 to protect the tip!')    
        
        # recommend to construct body first so that you don't need to calculate the body size by yourself
        body = self.tcp.dtype_convert(self.bias, 'float32', 'bin')
        header = self.tcp.header_construct('Bias.Set', body_size = len(body))
        cmd = header+body

        self.tcp.cmd_send(cmd)
        _, err = self.tcp.res_recv()
        self.tcp.print_err(err)
        print(f'The bias voltage is set to {bias}V')

    def BiasGet(self):
        header = self.tcp.header_construct('Bias.Get', body_size=0) # the body size here is the body size of Bias.Get argument 

        self.tcp.cmd_send(header)
        arg, err = self.tcp.res_recv('float32')
        self.tcp.print_err(err)

        self.bias = str(arg[0]) + 'V' # first [0] gives the res_arg list, second [0] gives the bias value in the list
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
        bias_pulse_width = self.tcp.unit_convert(bias_pulse_width)
        bias_value = self.tcp.unit_convert(bias_value)
        if bias_value > 10:
            raise ValueError('The maximum allowed bias is 10V. Please check your input! Bias has been set to 0 to protect the tip!') 
        
        # recommend to construct body first so that you don't need to calculate the body size by yourself
        body  = self.tcp.dtype_convert(wait_until_done, 'uint32', 'bin')
        body += self.tcp.dtype_convert(bias_pulse_width, 'float32', 'bin')
        body += self.tcp.dtype_convert(bias_value, 'float32', 'bin')
        body += self.tcp.dtype_convert(zctrl_on_hold, 'uint16', 'bin')
        body += self.tcp.dtype_convert(pulse_abs_rel, 'uint16', 'bin')
        header = self.tcp.header_construct('Bias.Pulse', body_size = len(body))
        cmd = header + body

        self.tcp.cmd_send(cmd)
        _, err = self.tcp.res_recv()

        self.tcp.print_err(err)
        print(f'Bias pulse finished. \n Pulse width: {bias_pulse_width}s \n Pulse value: {bias_value}V')

    
# todo
######################################## Bias Sweep Module#############################################
######################################## Bias Spectroscopy Module #############################################
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
ccc.BiasSet('8p')
ccc.BiasGet()
ccc.BiasPulse('500m', 7)
