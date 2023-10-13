'''
adam6018 Controller - 8 T/C - ModBus

Advantech ADAM 6018+ Data Acquisition Module - Thermocouple - driver

- 8 Thermocouple inputs

Thermocouple type and range:
– Type J: 0~760°C
– Type K: 0~1370°C
– Type T: -100~400°C
– Type E: 0~1000°C
– Type R: 500~1750°C
– Type S: 500~1750°C
– Type B: 500~1800°C

##NOTE: tc_type does nothing at the moment! (set type in adam utility)

# READ THE DOCS!
https://pypi.org/project/pyModbusTCP/
In directory: adam-user-manuals:
- ADAM-6000_User_Manaul_Ed.12-FINAL.pdf
- ADAM-6200_User_Manual_Ed.5_FINAL.pdf
'''


from pyModbusTCP.client import ModbusClient

class adam6018ModBus:
    def __init__(self, adam_ip, port = 502, tc_type="k"):
        print(f'Initializing adam6018 8-TC ModBus...')
        self._IP = adam_ip
        self.port = port
        self.TC_list = [0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07]
        self.TC_state = [0,0,0,0,0,0,0,0]
        self.TC_type = tc_type
        self.adam6018 = ModbusClient(host=self._IP, port=self.port, unit_id=1, auto_open=True)

    def get_all_inputs(self):
        #print("adam6217: Reading all Inputs")
        inputs_list = self.adam6018.read_input_registers(0, 8)
        #self.DI_state = [int(val) for val in inputs_list]   ## turn bool list into int list
        if inputs_list:
            #print(f"AI_0-7: {inputs_list}")
            i = 0
            for value in inputs_list:
                #print(f"AI_{i}:",end=" " )
                temp = self.calculate_temperature(value)
                self.TC_state[i] = temp
                i = i+1
            print(f"TC_0-7: {self.TC_state}")
            return self.TC_state
        else:
            print("adam6018: Unable to read thermocouples :(")
            return "ERROR"

    def calculate_temperature(self, inputValue):
        # 996 = 20.8 degC (set to type k)
        # 20.8/996 = *(26/1245)
        temp = round(inputValue*26/1245, 1)
        #print(f"Measured Voltage: {voltage}")
        return temp


