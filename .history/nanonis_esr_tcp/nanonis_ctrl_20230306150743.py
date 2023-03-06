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
        header = self.tcp.header_construct('Bias.Set', body_size = 4)
        body = self.tcp.dtype_convert(self.bias, 'float32', 'bin')
        cmd = header+body
        self.tcp.cmd_send(cmd)
        self.tcp.res_recv()
        print(f'The bias voltage is set to {bias}V')

    def BiasGet(self):
        header = self.tcp.header_construct('Bias.Get', body_size=0) # the body size here is the body size of Bias.Get argument 
        self.tcp.cmd_send(header)
        self.bias = str(self.tcp.res_recv('float32')[0][0]) + 'V' # first [0] gives the res_arg list, second [0] gives the bias value in the list
        print(f'Current bias: {self.bias}')
        return self.bias
    
    def BiasRangeSet():
        return
    
    def BiasRangeGet():
        return
    
    def BiasCalibrSet():
        return

    def BiasCalibrGet():
        return
    
    def BiasPulse():
        return
    

######################################## Bias Sweep Module#############################################

tcp = tcp_ctrl()
ccc = nanonis_ctrl(tcp)
ccc.BiasSet('8p')
ccc.BiasGet()
