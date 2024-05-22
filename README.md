# Nanonis-TCP-client
This TCP client package is written in Python to communicates with the Nanonis software. The communication is established over the TCP programming interface which is available for **V5e or V5** software version. 

<!-- ## Installation -->

## Basic usage

Here is an example of using the package:

```
import nanonis_tcp as tcp

my_tcp = tcp.tcp_ctrl()
connect = tcp.nanonis_ctrl(my_tcp)

connect.BiasSet(0.5) # One can also put strings like '500m', '50u', etc.
```

## Available commands
The commands in this package are programmed based on "Nanonis TCP Protocol-TCP Programming Interface" documentation. The following lines gives a list of available commands:
```
import nanonis_esr_tcp as tcp

tcphelp = tcp.help()
tcphelp.help()
```

## Programming commands
If you wish to use commands that are not programmed yet (you are very welcome to contribute to this package), you could follow the procedure:

The function of a command is composed of two main parts (See details in the Nanonis documentation):
* The first part is constructing and sending messages to Nanonis. 
* The second part is receiving and decoding messages from Nanonis.

Below is an example of programming `BiasSpectr.Start` command in the documentation:

1. The command has 3 arguments: Get data (unsigned int32), Save base name string size (int), and Save base name (string). 
    * It is unnecessary to manually count the length of the "Save base name" string, so we can calculate the length at the beginning of the function:
    ```
    def BiasSpectrStart(self, get_data, save_base_name, prt = if_print):
        save_base_name_size = len(save_base_name)
    ```
    * The request message is composed of the name of a command (header) and the argument values of the command (body). When constructing a body, put in the argument value, the original format, and the target format. Then add up the different parts of the body in order. When constructing a header, use the `header_construct` function. Finally use `cmd_send` to send the message.
    ```
        body  = self.tcp.dtype_cvt(get_data, 'uint32', 'bin')
        body += self.tcp.dtype_cvt(save_base_name_size, 'int', 'bin')
        body += self.tcp.dtype_cvt(save_base_name, 'str', 'bin')
        header = self.tcp.header_construct('BiasSpectr.Start', body_size = len(body))
        cmd = header + body
        self.tcp.cmd_send(cmd)
    ```
    * Function `dtype_cvt` converts different data types to binary or vice versa. The supported data types are: binary (`'bin'`), string (`'str'`), 32-bit signed integer (`'int'`), 16-bit unsigned integer (`'uint16'`), 32-bit unsigned integer (`'uint32'`), 32-bit float (`'float32'`), 64-bit float (`'float64'`), 1D string array (`'1dstr'`), 1D 32-bit signed integer array (`'1dint'`), 1D 32-bit unsigned integer array (`'1duint32'`), 1D 32-bit float array (`'1dfloat32'`), 2D string array (`'2dstr`)', 2D 32-bit float array (`'2dfloat32'`). 
    * When one of the arguments has a unit, this package has a function to convert the user input ("100m", "20p", etc...) to SI base unit. You should convert units at the beginning of the function. 
    ```
    t_2_on = self.tcp.unit_cvt(t_2_on) # NOte that these two lines are not a part of "BiasSpectrStart" function
    on_duration = self.tcp.unit_cvt(on_duration)
    ```
2. The function `res_recv` handles receiving and decoding the response message from Nanonis. `res_recv` converts the binary data to the corresponding data format. For `BiasSpectr.Start`, the formats of 9 return arguments needs to be specified manually, while the last one "error" is always processed inside `res_recv` function. As a result, the formats of 8 arguments needs to be specified: Channels names size (int), Number of channels (int), Channels names (1D array string), Data rows (int), Data columns (int), Data (2D array float32), Number of parameters (int), Parameters (1D array float32). 
```
 _, res_arg, res_err= self.tcp.res_recv('int', 'int', '1dstr', 'int', 'int', '2dfloat32', 'int', '1dfloat32')
 self.tcp.print_err(res_err) # print error if there is any 
```

3. Convert the data needed into Pandas DataFrames and print them if necessary. 
```
bias_spectr_df = pd.DataFrame(res_arg[5].T, columns = res_arg[2][0])

bias_spectr_param_df = pd.DataFrame(res_arg[7].T)
print('STS done!')
if prt: 
    print(bias_spectr_df)
    print(bias_spectr_param_df)
```
