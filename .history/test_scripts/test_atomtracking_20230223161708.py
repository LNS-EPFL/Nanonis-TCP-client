# -*- encoding: utf-8 -*-
'''
@Time    :   2023/02/23 15:51:41
@Author  :   Shixuan Shan 
'''

from nanonisTCP import nanonisTCP

TCP_IP = '127.0.0.1'
TCP_PORT = 6501
NTCP = nanonisTCP(TCP_IP, TCP_PORT)

class AtomTracking:
    '''
    Nanonis Atom Tracking Module
    '''
    def __init__(self, NanonisTCP):
        self.NanonisTCP = NanonisTCP
    
    def CtrlSet(self, ATControl, Status)
        hex_rep = self.NanonisTCP.make_header('AtomTrack.CtrlSet', body_size = 8)