# -*- encoding: utf-8 -*-
'''
@Time    :   2023/03/04 01:54:34
@Author  :   Shixuan Shan 
'''


class meas_ctrl:
    def __init__(self, basic_func):
        self.tcp = basic_func

    def BiasSet(self, sk, bias):
        header = self.tcp.header_construct('Bias.Set', body_size = 4)
        body = self.tcp.dtype_convert(self.tcp.unit_convert(bias), 'float32', 'bin')
        cmd = header+body
        print(header+body)
        self.tcp.cmd_send(sk, cmd)    