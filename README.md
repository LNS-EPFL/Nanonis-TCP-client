# Nanonis-TCP-client
A TCP client package is written in Python to communicates with Nanonis software. The communication is established over the TCP programming interface which is only available for V5e or V5 sftware version. 

Here is an example of using the package.

import nanonis_tcp as tcp

my_tcp = tcp.tcp_ctrl()

connect = tcp.nanonis_ctrl(my_tcp)

connect.BiasSet(0.5)
