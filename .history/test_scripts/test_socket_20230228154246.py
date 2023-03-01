import socket # for socket
import sys
import struct
 

# Defines data types and their sizes in bytes
datatype_dict = {'int':'>i', \
                 'uint16':'>H', \
                 'uint32':'>I', \
                 'float32':'>f', \
                 'float64':'>d' \
                }
datasize_dict = {'int':4, \
                 'uint16':2, \
                 'uint32':4, \
                 'float32':4, \
                 'float64':8 \
                }

si_prefix = {'':1.0, \
             'a':1e-18, \
             'f':1e-15, \
             'p':1e-12, \
             'n':1e-9, \
             'u':1e-6, \
             'm':1e-3 \
            }
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket successfully created")
except socket.error as err:
    print ("socket creation failed with error %s" %(err))
 
# default port for socket
PORT = 6501 
try:
    host_ip = socket.gethostbyname('localhost')
except socket.gaierror:
 
    # this means could not resolve the host
    print ("there was an error resolving the host")
    sys.exit()
 
# connecting to the server
s.connect((host_ip, PORT))
print ("the socket has successfully connected")

# receive data from the server and decoding to get the string.
#print (s.recv(1024).decode())
# close the connection
def construct_header(command_name, body_size, send_response_back = True):
    r'''
    Builds a 40 byte header with the Nanonis command name and body size in bytes
    '''
    cmd_name_bytes = to_binary('string', command_name)
    len_cmd_name_bytes = len(cmd_name_bytes)
    cmd_name_bytes += b'\0' * (32 - len_cmd_name_bytes) # Pad command name with 0x00 to 32 bytes
    if send_response_back:
        response_flag = b'\x00\x01' # Tell Nanonis to send a response to client
    else:
        response_flag = b'\0\0' # Tell Nanonis to not send a response to client
    header = cmd_name_bytes + \
             to_binary('int', body_size) + \
             response_flag + b'\0\0'
    return header

def construct_command(command_name, *vargs):
    r'''
    Builds the sequence of bytes to send to Nanonis.
    This function takes an odd number of arguments. The first argument is the command name.
    The following arguments come in pairs: a string specifying the data type, the value of the data.
    '''
    if len(vargs) % 2 != 0:
        raise nanonisException('Unbalanced number of arguments')
    body_size = 0
    body = b''
    datatype = ''
    for idx, arg in enumerate(vargs):
        if idx % 2 == 0:
            datatype = arg
            body_size += datasize_dict[datatype]
        else:
            body += to_binary(datatype, arg)
    header = construct_header(command_name, body_size)
    return header + body

#s.send('Bias.Set', 'float32', 5)


def to_binary(datatype, input_data):
    r'''
    Converts input_data to a sequence of bytes based on the datatype
    '''
    if datatype == 'string':
        return bytes(input_data,'utf-8')
    try:
        return struct.pack(datatype_dict[datatype], input_data)
    except KeyError:
        raise nanonisException('Unknown Data Type: ' + str(datatype))


my_command = construct_command('AtomTrack.CtrlSet', 'float32', 1)
print(my_command)
s.sendall(my_command)
answer=s.recv(1024)
print(answer)

# s.close()
# #s.connect((IP, PORT))
