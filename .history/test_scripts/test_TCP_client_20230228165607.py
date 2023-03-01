# -*- encoding: utf-8 -*-
'''
@Time    :   2023/02/28 14:52:33
@Author  :   Shixuan Shan 
'''
import socket

############################### functions ###################################
def socket_connect():
    

def socket_close(sk):
    sk.close()



TCP_IP = '127.0.0.1'
PORT = 6501 # avialable ports: 6501, 6502, 6503, 6504
server_address = (TCP_IP, PORT)

# create a TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(server_address)

s.close()