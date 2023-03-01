# -*- encoding: utf-8 -*-
'''
@Time    :   2023/02/23 15:51:41
@Author  :   Shixuan Shan 
'''

from nanonisTCP import nanonisTCP

class AtomTracking:
    '''
    Nanonis Atom Tracking Module
    '''
    def __init__(self, NanonisTCP):
        self.NanonisTCP = NanonisTCP
    
    def CtrlSet(self, ATControl, Status):
        # Make Hearder
        hex_rep = self.NanonisTCP.make_header('AtomTrack.CtrlSet', body_size = 8)

        # Arguments
        hex_rep += self.NanonisTCP.to_hex(ATControl, 2)
        hex_rep += self.NanonisTCP.to_hex(Status, 2)

        self.NanonisTCP.send_command(hex_rep)

        self.NanonisTCP.receive_response(0)

    def PropsSet(self, IntegralGain, Frequency, Amplitude, Phase, SwitchOffDelay):
        # Make Header
        hex_rep = self.NanonisTCP.make_header('AtomTrack.PropsSet', body_size = 20)

        # Arguments
        hex_rep += self.NanonisTCP.float32_to_hex(IntegralGain)
        hex_rep += self.NanonisTCP.float32_to_hex(Frequency)
        hex_rep += self.NanonisTCP.float32_to_hex(Amplitude)
        hex_rep += self.NanonisTCP.float32_to_hex(Phase)
        hex_rep += self.NanonisTCP.float32_to_hex(SwitchOffDelay)

        self.NanonisTCP.send_command(hex_rep)

        self.NanonisTCP.receive_response(0)
    
    def StatusGet(self, ATControl):
        # Make header
        hex_rep = self.NanonisTCP.make_header('AtomTrack.StatusGet', body_size = 4)

        # Arguments
        hex_rep += self.NanonisTCP.to_hex(ATControl, 2)
        print(self.NanonisTCP.to_hex(ATControl, 2))

        self.NanonisTCP.send_command(hex_rep)

        response = self.NanonisTCP.receive_response() # 4 is the body size of the response
        print(response)
        # status = self.NanonisTCP.hex_to_uint16(response[0:4])
        return status

    

TCP_IP = '127.0.0.1'
TCP_PORT = 6501
NTCP = nanonisTCP(TCP_IP, TCP_PORT)

print('start')
atomtracking = AtomTracking(NTCP)
print('1')


# atomtracking.CtrlSet(0, 0)
# atomtracking.CtrlSet(1, 0)
print('2')

status = atomtracking.StatusGet(1)
print(status)
NTCP.close_connection()   
print('end')