'''
adam6217 Controller - 8AI - ModBus

Advantech ADAM 6217 Data Acquisition Module - Analog In -  driver

- 8 Analog Inputs (-10/+10 v), (0/20mA)

# READ THE DOCS!
https://pypi.org/project/pyModbusTCP/
In directory: adam-user-manuals:
- ADAM-6000_User_Manaul_Ed.12-FINAL.pdf
- ADAM-6200_User_Manual_Ed.5_FINAL.pdf
'''


from pyModbusTCP.client import ModbusClient






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
            print("adam6217: Unable to read Analog inputs :(")
            return "ERROR"


    def get_current_inputs(self):     #4-20mA input
        # print("adam6217: Reading all Inputs")
        inputs_list = self.adam6217.read_input_registers(0, 8)
        # self.DI_state = [int(val) for val in inputs_list]   ## turn bool list into int list
        if inputs_list:
            print(f"AI_0-7: {inputs_list}")
            i = 0
            for value in inputs_list:
                #print(f"AI_{i}:",end=" " )
                current = self.calculate_current_4(value)
                self.AI_state[i] = current
                i = i + 1
            print(f"AI_0-7: {self.AI_state}")
            return self.AI_state
        else:
            print("adam6217: Unable to read Analog inputs (4-20mA) :(")
            return "ERROR"



    def calculate_voltage(self, inputValue):
        # Offset is 32768
        voltage = inputValue - 32768
        #with offset removed 3v input = 9772 returned
        voltage = round(voltage/3257.333,2)
        #print(f"Measured Voltage: {voltage}")
        return voltage

    def calculate_current_4(self, inputValue):
        # 9772/20 =
        current = round(inputValue/488.6,2)
        return current
