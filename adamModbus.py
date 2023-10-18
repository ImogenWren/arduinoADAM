"""
adamModbus

Series of python drivers for ModBus Communication with Advantech ADAM Data Acquisition Modules.
- More Robust and Simple operation than ASCII commands and websockets.
- Simple


See the following classes for specific ADAM controllers:

ADAM-6052 (8DI, 8DO): adam6052ModBus.py
ADAM-6217 (8AI):      adam6052ModBus.py
ADAM-6018+ (8TC):     adam6018ModBus.py


# READ THE DOCS!
https://pypi.org/project/pyModbusTCP/
https://control.com/forums/threads/reading-di-do-status-of-adam-6050.27164/
In directory: adam-user-manuals:
- ADAM-6000_User_Manaul_Ed.12-FINAL.pdf
- ADAM-6200_User_Manual_Ed.5_FINAL.pdf

Example ModBus commands (ADAM-6052 docs)
Example: Force Coil 3 (Address 00003) to ON in an ADAM-6000 module.
01 05 00 03 FF 00

Example: Force Coil DO 0 (Address 00017 (0x11)) to ON in an ADAM-6000 module.
01 05 00 11 FF 00

"""

## Init
from pyModbusTCP.client import ModbusClient
import time

import adam6052ModBus as adam6052
import adam6217ModBus as adam6217
import adam6018ModBus as adam6018


# Ethernet Delarations
ADAM_6052_IP = "192.168.1.111"
ADAM_6217_IP = "192.168.1.112"
ADAM_6018_IP = "192.168.1.113"
ADAM_6024_IP = "192.168.1.114"

PORT = 502


'''
adam6024 Controller - 12UIO - ModBus

Advantech ADAM 6052 Data Acquisition Module - Universal IO - driver

- 6 Analog Inputs (-10/+10v, 0-20mA)
- 2 Analog Outputs (0-10vDC, 0-20mA)
- 2 Digital Input (Dry Contact, Wet Contact (0-30v)
- 2 Digital Output (Close/Open Contact, 10-30vDC)


# READ THE DOCS!
https://pypi.org/project/pyModbusTCP/
In directory: adam-user-manuals:
- ADAM-6000_User_Manaul_Ed.12-FINAL.pdf
- ADAM-6200_User_Manual_Ed.5_FINAL.pdf
'''



#TODO Add analog outputs

class adam6024ModBus:
    def __init__(self, adam_ip, port = 502):
        print(f'Initializing adam6024 6-AI 2-AO 2-DI 2-DO Universal IO ModBus...')
        self._IP = adam_ip
        self.port = port
        self.AI_list = [0x00, 0x01, 0x02,0x03,0x04,0x05]   ## Not sure this is correct
        self.AI_state = [0,0,0,0,0,0]
        self.AO_list = [0x40,0x41]
        self.AO_state = [0.0,0.0]
        self.DI_list = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]
        self.DI_state = [0, 0, 0, 0, 0, 0, 0, 0]
        self.DO_list = [0x10,0x11,0x12,0x13,0x14,0x15,0x16,0x17]  #DO_0 to DO_7
        self.DO_state = [0,0]  # Dont rely too much on this until checking added

        # Create a Modbus TCP client
        # Module init (TCP always open)
        self.adam6024 = ModbusClient(host=self._IP, port=self.port, unit_id=1, auto_open=True)


    def set_coil(self, DO_number, state):
        no_error = self.adam6024.write_single_coil(self.DO_list[DO_number], state)
        self.DO_state[DO_number] = state
        time.sleep(0.5)
        if (no_error):
            print(f"adam6024: coil DO_{DO_number}: Written to {state}")
            return 0   # return false if complete
        else:
            print(f"adam6024: coil DO_{DO_number}: Unable to write to {state}")
            return 1  # error code can be returned here

    def set_all_coils(self, states):
        no_error = (self.adam6024.write_multiple_coils(self.DO_list[0], states))
        self.DO_state = states
        time.sleep(0.5)
        if (no_error):
            print(f"adam6024: all coils: Written to {states}")
            return 0  # return false if complete
        else:
            print(f"adam6024: all coils: Unable to write to {states}")
            return 1  # error code can be returned here

#TODO add error handling to all subroutines
    #TODO Test Error Handling Here!
    def get_digital_inputs(self):
        #print(f"adam6052: Reading Input DI_{DI_number}")
        try:
            inputs_list = self.adam6024.read_discrete_inputs(0, 2)
            inputs_list = [int(val) for val in inputs_list]   ## turn bool list into int list
            if inputs_list:
                print(f"DI_0-1: {inputs_list}")
                return inputs_list
            else:
                print("adam6024: Unable to read Digital input :(")
                return "ERROR"
        except:
            print("adam6024: Error processing Read Digital Input request")

    def get_analog_inputs(self):
        #print("adam6052: Reading all Inputs")
        inputs_list = self.adam6024.read_input_registers(0,6)
        if inputs_list:
            i = 0
            for value in inputs_list:
                voltage = self.calculate_voltage(value)
                self.AI_state[i] = voltage
                i = i+1
            print(f"AI_0-5: {self.AI_state}")
            return self.AI_state
        else:
            print("adam6024: Unable to read Analog inputs :(")
            return "ERROR"

    def calculate_voltage(self, inputValue):
        # Offset is 32768
        voltage = inputValue - 32768
        #with offset removed 3v input = 9772 returned
        voltage = round(voltage/3257.333,2)
        #print(f"Measured Voltage: {voltage}")
        return voltage

    def set_analog_output(self,channel,setPoint):
        
        no_error = self.adam6024.custom_request()
        (channel, setPoint)
        self.AO_state = setPoint
        time.sleep(0.5)
        if (no_error):
            print(f"adam6024: coils: Written to {setPoint}")
            return 0  # return false if complete
        else:
            print(f"adam6024: coils: Unable to write {setPoint} to channel {channel}")
            return 1  # error code can be returned here








def main():
    print("Starting ADAM Modbus control")
    iteration = 0
    adamDIO = adam6052.adam6052ModBus(ADAM_6052_IP, PORT)
    adamAI = adam6217.adam6217ModBus(ADAM_6217_IP, PORT)
    adamTC = adam6018.adam6018ModBus(ADAM_6018_IP, PORT, tc_type="K")   ## tc_type does nothing at the moment! (set type in adam utility)
    adamUIO = adam6024ModBus(ADAM_6024_IP, PORT)
    adamUIO.set_analog_output(4,1)
    while (True):
        '''
        print(f"{iteration}:", end="\n")
        adamDIO.get_all_inputs()
        adamAI.get_all_inputs()
        adamTC.get_all_inputs()
        adamUIO.get_analog_inputs()
        adamUIO.get_digital_inputs()
        adamDIO.set_coil(0, True)
        adamUIO.set_all_coils([1,0])
        time.sleep(5)
        adamDIO.set_all_coils([0, 0, 0, 0, 0, 0, 0, 0])
        adamUIO.set_all_coils([0,1])
        '''
        time.sleep(3)
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
    print("Program Quit")

