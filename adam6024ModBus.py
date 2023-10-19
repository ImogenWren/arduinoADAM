'''
adam6024 Controller - 12UIO - ModBus

Advantech ADAM 6052 Data Acquisition Module - Universal IO - driver

- 6 Analog Inputs (-10/+10v, 0-20mA, 4-20mA)
- 2 Analog Outputs (0-10vDC, 0-20mA, 4-20mA)
- 2 Digital Input (Dry Contact, Wet Contact (0-30v)
- 2 Digital Output (Close/Open Contact, 10-30vDC)


# READ THE DOCS!
https://pypi.org/project/pyModbusTCP/
In directory: adam-user-manuals:
- ADAM-6000_User_Manaul_Ed.12-FINAL.pdf
- ADAM-6200_User_Manual_Ed.5_FINAL.pdf
'''



from pyModbusTCP.client import ModbusClient
import time

class adam6024ModBus:
    def __init__(self, adam_ip, port = 502):
        print(f'Initializing adam6024 6-AI 2-AO 2-DI 2-DO Universal IO ModBus...')
        self._IP = adam_ip
        self.port = port
        self.AI_list = [0x00, 0x01, 0x02,0x03,0x04,0x05]   ## Not sure this is correct
        self.AI_state = [0,0,0,0,0,0]
        self.AI_mode = ["V","V","V","V","V","mA_0"]
        self.AO_list = [0xA,0xB]
        self.AO_state = [0.0,0.0]
        self.AO_mode = [2, 0]     #values: 0 = I(0-20mA), 1 = I(4-20mA), 2 = (0-10v)
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
                if  self.AI_mode[i] == "V":
                    voltage = self.calculate_voltage(value)
                    self.AI_state[i] = voltage
                elif  self.AI_mode[i] == "mA_0":
                    current = self.calculate_current_0(value)
                    self.AI_state[i] = current
                elif self.AI_mode[i] == "mA_4":
                    current = self.calculate_current_4(value)
                    self.AI_state[i] = current
                else:
                    print(f"Unknown AI mode requested")
                    return "ERROR"
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

#TODO Change calculations for current input these are WRONG
    def calculate_current_0(self, inputValue):
        # Offset is 32768
        voltage = inputValue - 32768
        #with offset removed 3v input = 9772 returned
        voltage = round(voltage/3257.333,2)
        #print(f"Measured Voltage: {voltage}")
        return voltage

    def calculate_current_4(self, inputValue):
        # Offset is 32768
        voltage = inputValue - 32768
        #with offset removed 3v input = 9772 returned
        voltage = round(voltage/3257.333,2)
        #print(f"Measured Voltage: {voltage}")
        return voltage



    def set_analog_output(self,channel,setPoint_in, mode="mA_0"):  # Method is output mode agnostic, uses list to check preset mode
        unit = "mA"
                # DAC is 16bit, max_val = 4095 0FFF
        if mode == "mA_0":
            setPoint = self.calculate_Iout_0(setPoint_in)
        elif mode == "mA_4":
            setPoint = self.calculate_Iout_4(setPoint_in)
            unit = "%"
        elif mode == "V":
            setPoint = self.calculate_Vout(setPoint_in)
            unit = "V"
        else:
            print(f"Output Mode {mode} not Recognised")
            return "ERROR"
        no_error = self.adam6024.write_single_register(self.AO_list[channel], setPoint)
        print(no_error)
        time.sleep(0.5)
        if (no_error):
            print(f"adam6024: {setPoint_in} {unit} ({setPoint}) Written to AO_{channel}")
            self.AO_state[channel] = setPoint
            return 0  # return false if complete
        else:
            print(f"adam6024: Unable to write {setPoint_in} {unit} ({setPoint})) to AO_{channel}")
            return 1  # error code can be returned here

    def calculate_Iout_0(self, target_Iout):
        # 0mA = 0, 20mA = 4095
        DAC_value = int(round(target_Iout * 204.75))
        return DAC_value

    def calculate_Iout_4(self, target_percentage):   # This method uses a percentage of open as it makes zero sense setting specific mA output
        #  4mA = 0, 20mA = 4095
        #target_Iout = target_Iout - 4
        DAC_value = int(round(target_percentage * 4095))
        return DAC_value

    def calculate_Vout(self, target_voltage):
        # 10v = 4095
        DAC_value = int(round(target_voltage*409.5))
        return DAC_value

