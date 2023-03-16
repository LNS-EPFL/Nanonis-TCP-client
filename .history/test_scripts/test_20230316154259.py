import nanonis_esr_tcp as net

tcp = net.tcp_ctrl()
nctrl = net.nanonis_ctrl(tcp)

nctrl.BiasSet(4)
# nctrl.BiasSpectrOpen()
# nctrl.BiasSpectrPropsSet(0, 1, 2, 121, 0,0,0)
tcp.socket_close()
