# -*- encoding: utf-8 -*-
'''
@Time    :   2023/03/04 01:54:34
@Author  :   Shixuan Shan 
'''


class meas_ctrl:
    def __init__(self):
        self.tcp = basic_func
        
    def BiasSet(self, sk, bias):
        header = header_construct('Bias.Set', body_size = 4)
        body = dtype_convert(unit_convert(bias), 'float32', 'bin')
        cmd = header+body
        print(header+body)
        cmd_send(sk, cmd)    