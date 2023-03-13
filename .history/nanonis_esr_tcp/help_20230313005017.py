# -*- encoding: utf-8 -*-
'''
@Time    :   2023/03/13 00:44:06
@Author  :   Shixuan Shan 
'''

#  This is a help module if you don't know how to use the funcitons in nanonis_ctrl.py file

class help:
    def __init__(self):
        self.general_info = "This is a help module if you don't know how to use the funcitons in nanonis_ctrl.py file"

    def help(self):
        return print('Here are some tips of using this Nanonis TCP module: \
              \n 1. Normally for a tristate setting, such as "save all" in "BiasSpectrPropsSet" function, there are three valid input values: \n\
              1) 0 --> No change \n\
              2) 1 --> Yes/On \n\
              3) 2 --> No/Off')

    def BiasSet(self):
        return print('BiasSet(self, bias)')

    def BiasGet(self):
        return print('BiasGet(self)')

