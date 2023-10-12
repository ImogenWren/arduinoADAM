'''

adamModbus

- Attempt to move away from ASCII commands and towards a more robust implementation using MODBUS

https://control.com/forums/threads/reading-di-do-status-of-adam-6050.27164/

import pymodbus
import minimalmodbus

Example: Force Coil 3 (Address 00003) to ON in an ADAM-6000 module.
01 05 00 03 FF 00


Example: Force Coil DO 0 (Address 00017 (0x11)) to ON in an ADAM-6000 module.
01 05 00 11 FF 00

# READ THE DOCS!
https://pypi.org/project/pyModbusTCP/
'''
# Ethernet Delarations
ADAM_6052_IP = "192.168.1.111"
ADAM_6217_IP = "192.168.1.112"
#PORT = 1025    #1024-1029 valid for http
PORT = 502
BUFFER = 1024


DO_0 = 0x10  # THIS MAKES NO SENSE!! should be 0x11 given documentation!
DO_1 = 0x11
DO_2 = 0x12
DO_3 = 0x13
DO_4 = 0x14
DO_5 = 0x15
DO_6 = 0x16
DO_7 = 0x17

DO_list = [DO_0,DO_1,DO_2,DO_3,DO_4,DO_5,DO_6,DO_7]

## Init
from pyModbusTCP.client import ModbusClient
import time

# Create a Modbus TCP client
#Module init (TCP always open)
adam6052 = ModbusClient(host=ADAM_6052_IP,port=PORT, unit_id=1, auto_open=True)
bit = True


def adam6052_set_coil(DO_number, state):
    no_error = adam6052.write_single_coil(DO_list[DO_number], state)
    # no_error = client.w
    time.sleep(0.5)
    if (no_error):
        print(f"adam6052: coil DO_{DO_number}: Written to {state}")
        return 0   # return false if complete
    else:
        print(f"adam6052: coil DO_{DO_number}: Unable to write to {state}")
        return 1  # error code can be returned here



## Main Loop
while True:
    print("Starting Modbus Connection")
    adam6052_set_coil(0, True)
    time.sleep(4)
    adam6052_set_coil(0, False)
    time.sleep(4)



