import nanonis_esr_tcp as net

tcp = net.tcp_ctrl()
nctrl = net.nanonis_ctrl(tcp)

nctrl.BiasSpectrOpen()
nctrl.BiasSpectrPropsSet(0, 1, 2, 121, 0,0,0)
