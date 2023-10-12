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

## Init
from pyModbusTCP.client import ModbusClient
import time

# Ethernet Delarations
ADAM_6052_IP = "192.168.1.111"
ADAM_6217_IP = "192.168.1.112"
#PORT = 1025    #1024-1029 valid for http
PORT = 502



class adam6052ModBus:
    def __init__(self, adam_ip, port = 502):
        print(f'Initializing adam6052 8-DI 8-DO ModBus...')
        self._IP = adam_ip
        self.port = port
        self.DO_list = [0x10,0x11,0x12,0x13,0x14,0x15,0x16,0x17]  #DO_0 to DO_7
        self.DO_state = [0,0,0,0,0,0,0,0]   # Dont rely too much on this untill checking added
        self.DI_list = [0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07]
        self.DI_state = [0,0,0,0,0,0,0,0]
        # Create a Modbus TCP client
        # Module init (TCP always open)
        self.adam6052 = ModbusClient(host=self._IP, port=self.port, unit_id=1, auto_open=True)


    def set_coil(self, DO_number, state):
        no_error = self.adam6052.write_single_coil(self.DO_list[DO_number], state)
        self.DO_state[DO_number] = state
        time.sleep(0.5)
        if (no_error):
            print(f"adam6052: coil DO_{DO_number}: Written to {state}")
            return 0   # return false if complete
        else:
            print(f"adam6052: coil DO_{DO_number}: Unable to write to {state}")
            return 1  # error code can be returned here

    def set_all_coils(self, states):
        no_error = (self.adam6052.write_multiple_coils(self.DO_list[0], states))
        self.DO_state = states
        time.sleep(0.5)
        if (no_error):
            print(f"adam6052: all coils: Written to {states}")
            return 0  # return false if complete
        else:
            print(f"adam6052: all coils: Unable to write to {states}")
            return 1  # error code can be returned here


    def get_input(self, DI_number):
        #print(f"adam6052: Reading Input DI_{DI_number}")
        inputs_list = self.adam6052.read_discrete_inputs(DI_number, 1)
        inputs_list = [int(val) for val in inputs_list]   ## turn bool list into int list
        if inputs_list:
            print(f"DI_{DI_number}: {inputs_list}")
            return inputs_list
        else:
            print("Unable to read inputs :(")
            return "ERROR"

    def get_all_inputs(self):
        #print("adam6052: Reading all Inputs")
        inputs_list = self.adam6052.read_discrete_inputs (0, 8)
        self.DI_state = [int(val) for val in inputs_list]   ## turn bool list into int list
        if inputs_list:
            print(f"DI_0-7: {self.DI_state}")
            return self.DI_state
        else:
            print("Unable to read inputs :(")
            return "ERROR"


class adam6217ModBus:
    def __init__(self, adam_ip, port = 502):
        print(f'Initializing adam6217 8-AI ModBus...')
        self._IP = adam_ip
        self.port = port
        self.AI_list = [0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07]
        self.AI_state = [0,0,0,0,0,0,0,0]
        self.adam6217 = ModbusClient(host=self._IP, port=self.port, unit_id=1, auto_open=True)

    def get_all_inputs(self):
        #print("adam6217: Reading all Inputs")
        inputs_list = self.adam6217.read_input_registers(0, 8)
        #self.DI_state = [int(val) for val in inputs_list]   ## turn bool list into int list
        if inputs_list:
            #print(f"AI_0-7: {inputs_list}")
            i = 0
            for value in inputs_list:
                #print(f"AI_{i}:",end=" " )
                voltage = self.calculate_voltage(value)
                self.AI_state[i] = voltage
                i = i+1
            print(f"AI_0-7: {self.AI_state}")
            return self.AI_state
        else:
            print("Unable to read inputs :(")
            return "ERROR"

    def calculate_voltage(self, inputValue):
        # Offset is 32768
        voltage = inputValue - 32768
        #with offset removed 3v input = 9772 returned
        voltage = round(voltage/3257.333,2)
        #print(f"Measured Voltage: {voltage}")
        return voltage



def main():
    print("Starting adam Modbus control")
    iteration = 0
    adam6052 = adam6052ModBus(ADAM_6052_IP, PORT)
    adam6217 = adam6217ModBus(ADAM_6217_IP, PORT)
    while (True):
        print(f"{iteration}:", end=" ")
        adam6052.get_all_inputs()
        print(f"{iteration}:", end=" ")
        adam6217.get_all_inputs()
        time.sleep(2)
        iteration = iteration + 1


    # adam6052_set_coil(0, True)
    # time.sleep(4)
    # adam6052_set_coil(0, False)
    # time.sleep(4)
    # time.sleep(5)
    # adam6052_set_all_coils(DO_state)
    # time.sleep(4)
    # time.sleep(5)
    # adam6052_set_all_coils([0,0,0,0,0,0,0,0])






if __name__ == "__main__":
    main()


