# -*- encoding: utf-8 -*-
'''
@Time    :   2023/03/04 01:54:34
@Author  :   Shixuan Shan 
'''
from tcp_ctrl import tcp_ctrl

class nanonis_ctrl:
    def __init__(self, tcp):
        self.tcp = tcp

    def BiasSet(self, bias):
        self.bias = self.tcp.unit_convert(bias)
        if self.bias > 10:
            raise ValueError('The maximum allowed bias is 10V. Please check your input! Bias has been set to 0 to protect the tip!')    
        header = self.tcp.header_construct('Bias.Set', body_size = 4)
        body = self.tcp.dtype_convert(self.bias, 'float32', 'bin')
        cmd = header+body
        self.tcp.cmd_send(cmd)

tcp = tcp_ctrl()
ccc = nanonis_ctrl(tcp)
ccc.BiasSet(5.5)
