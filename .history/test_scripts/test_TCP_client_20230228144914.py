import socket

tcp_ip = '127.0.0.1'
tcp_port = 6501 # avialable ports: 6501, 6502, 6503, 6504

# create a TCP/IP socket
socket.socket(socket.AF_INET, socket.SOCK_STREAM)