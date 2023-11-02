'''
acUnit - DEMO

Refrigeration experiment IO demo program.

Demonstrates the function of all hardware IOs.


'''

#import adamModbus as adam
## Init
#from pyModbusTCP.client import ModbusClient
import time


import adam6052ModBus as adam6052
import adam6217ModBus as adam6217
import adam6018ModBus as adam6018
import adam6024ModBus as adam6024

import sensorCalc

# Ethernet Declarations
ADAM_6052_A_IP = "192.168.1.111"
ADAM_6052_B_IP = "192.168.1.116"
ADAM_6217_A_IP = "192.168.1.112"
ADAM_6217_B_IP = "192.168.1.115"

PORT = 502

'''
IO List
# DO - adam6052_A
V1 = adamDIO_A.DO_list[0]       # Self Regulating
V2 = adamDIO_A.DO_list[1]       # Small Capillary
V3 = adamDIO_A.DO_list[2]       # medium Capillary
V4 = adamDIO_A.DO_list[3]       # large Capillary
V5 = adamDIO_A.DO_list[4]       # Receiver Outlet
V6 = adamDIO_A.DO_list[5]       # Receiver Inlet
V7 = adamDIO_A.DO_list[6]       # Receiver Bypass0
unused = adamDIO.DO_list[7]     # Unused

# DO - adam6052_B
W1 = adamDIO_B.DO_list[0]       # fan - condenser
W2 = adamDIO_B.DO_list[1]       # fan - evaporator
V_comp = adamDIO_B.DO_list[2]   # Compressor

#Voltage AI
PS1 = adamAI_C.AI_list[0]       # Evaporation Pressure
PS2 = adamAI_C.AI_list[1]       # Compressor Outlet Pressure
PS3 = adamAI_C.AI_list[2]       # Condenser Outlet Pressure
TC1 = adamAI_C.AI_list[3]       # Compressor Inlet Temperature
TC2 = adamAI_C.AI_list[4]       # Compressor Outlet Temperature
TC3 = adamAI_C.AI_list[5]       # Condenser Outlet Temperature
TC4 = adamAI_C.AI_list[6]       # Evaporator Inlet Temperature
TC5 = adamAI_C.AI_list[7]       # Evaporator Outlet Temperature


#Current AI
flow_meter = adamAI_D.AI_list[0] # Flowmeter
power_meter = adamAI_D.AI_list[1] # Power Meter
APS = adamAI_D.AI_list[2] # ambient pressure sensor
ATS = adamAI_D.AI_list[3] # ambient temp sensor
'''



'''
Program operation:
Init:
-Setup all IOs
- Create Data Structures for sensors
- Create Data Structures for valve state - UI should interrogate this program to report valve state
#TODO Write function for adam 6052 to report current valve states
Loop:
- Sample all sensors and return as dictionary. (format below)
- wait for JSON commands.
    - Return data or run function based on JSON parsing

ILLEGAL STATES:
- Compressor ON, IF (V5 & V6) & (V1 or V2 or V3 or V4)  CLOSED
- Compressor ON, IF (FanA & FanB) OFF
 
'''

#TODO Define Unknowns:
'''
- Error handling
- Exception Handling
- status reporting
- program exit?
- logs - detail required - datapoints required- time periods
- Blocking action given specific states
- sending JSON commands into python program
- sending JSON commands from python program

# Defining JSON Commands as python dictionary

# SET COMMANDS (ideas)
{"cmd":"set", "V1":"open"} 
{"cmd":"set", "V5":"open","V6":"open"}
{"cmd":"set","item":"V1","state":"open"}
{"cmd":"V1", "value":"open"}

{"set":"V1", "state":"open"}

# all these should work
{"set:"V_comp","state":"on"}
{"set:"V_comp","state":1}
{"set:"V_comp","state":"true"}

{"set:"V_comp","state":"off"}
{"set:"V_comp","state":0}
{"set:"V_comp","state:"false"}


# GET COMMANDS
- Get commands for data return entire data packet for all values
{"cmd":"get"} - get all data
{"get":"V1"}
{"get":"all"}

acUnit_state = {
    "valves" : {
        "V1" : 0,
        "V2" : 0,
        "V3" : 0,
        "V4" : 0,
        "V5" : 0,
        "V6" : 0,
        "V7" : 0           
    },
    "power-relays"  :  {
        "W1" : 0,
        "W2": 0,
        "V_comp": 0
    },
    "sensors-pressure": {
        "PS1" : 0,
        "PS2" : 0,
        "PS3" : 0
    },
    "sensors-temperature": {
        "TC1" : 0, 
        "TC2" : 0, 
        "TC3" : 0, 
        "TC4" : 0, 
        "TC5" : 0
    },
    "sensors-other":{
        "flow": 0,
        "power":0,
        "APS" : 0,
        "ATS" : 0
    }    
}


'''


class acUnit:
    def __init__(self):
        print("Starting AC Unit Refrigeration Rig - DEMO")
        # Setup IOs
        self.adamDIO_A = adam6052.adam6052ModBus(ADAM_6052_A_IP, PORT)
        self.adamDIO_B = adam6052.adam6052ModBus(ADAM_6052_B_IP, PORT)
        self.adamAI_C = adam6217.adam6217ModBus(ADAM_6217_A_IP, PORT)  # 0-10v in for temp & pressure sensors
        self.adamAI_D = adam6217.adam6217ModBus(ADAM_6217_B_IP, PORT)  # 4-20mA in for flow sensor
        self.sensors = sensorCalc.sensorCalc()  ## library for sensor conversions
        # List IO channels
        self.V1 = 0  # Self Regulating
        self.V2 = 1  # Small Capillary
        self.V3 = 2  # medium Capillary
        self.V4 = 3  # large Capillary
        self.V5 = 4 # Receiver Outlet
        self.V6 = 5  # Receiver Inlet
        self.V7 = 6  # Receiver Bypass
        self.unused = 7  # Unused



    def set_valve(self, valveNumber, state):
        if valveNumber >= 1 and valveNumber <= 7:
            self.adamDIO_A.set_coil(valveNumber-1, state)
            valveState = self.adamDIO_A.get_coil_state(valveNumber-1)
            if (valveState[0] == state):
                print(f"Valve V{valveNumber} set to {state}")
            else:
                print(f"Error checking valve V{valveNumber} state")
        else:
            print(f"ERROR: Unknown Valve V{valveNumber} requested ")

    def get_valve_state(self, valveNumber):
        if valveNumber >= 1 and valveNumber <= 7:
            valveState = self.adamDIO_A.get_coil_state(valveNumber - 1)
            return valveState[0]
        else:
            print(f"ERROR: Unknown Valve V{valveNumber} requested ")

    def get_all_valves(self, test_mode=False):
        if test_mode == False:
            valveStates = self.adamDIO_A.get_coil_range(self.V1, self.V7)
            valve = 1
            for state in valveStates:
                print(f"V{valve} = {state}")
                valve = valve + 1
            return valveStates
        else:
            return [0,0,0,0,0,0,0,0]

    def set_compressor(self,state):
        self.adamDIO_B.set_coil(0, state)
        compressorState = self.adamDIO_B.get_coil_state(0)
        if (compressorState[0] == state):
            print(f"Compressor set to {state}")
        else:
            print(f"Error Compressor state")

    def set_fans(self,state):
        self.adamDIO_B.set_coil(1, state)
        self.adamDIO_B.set_coil(2, state)
        fanA_state = self.adamDIO_B.get_coil_state(1)
        fanB_state = self.adamDIO_B.get_coil_state(2)
        if (fanA_state[0] == state):
            print(f"Fan A set to {state}")
        else:
            print(f"Error Setting Fan A state")
        if (fanB_state[0] == state):
            print(f"Fan B set to {state}")
        else:
            print(f"Error Setting Fan B state")

    def get_sensors(self):
        print(f"Getting Sensors")

    def get_pressure_sensors(self):
        print("Getting Pressure Sensors")
        pressure_voltages = self.adamAI_C.get_voltage_inputs(0, 2)
        pressure_list = []
        for voltage in pressure_voltages:
            pressure_bar = self.sensors.voltage_to_pressure(voltage, 0,30,1,6)
            pressure_list.append(pressure_bar)
            #print(f"Pressure: {pressure_bar} bar")
        print(f"Pressures: P1-3: {pressure_list} bar")
        return pressure_list



    def get_temp_sensors(self):
        print("Getting Temp Sensors")
        temp_voltages = self.adamAI_C.get_voltage_inputs(3, 7)
        temp_list = []
        for voltage in temp_voltages:
            temp_degC = self.sensors.voltage_to_temp(voltage)
            temp_list.append(temp_degC)
            # print(f"Pressure: {pressure_bar} bar")
        print(f"Temperature: T1-5: {temp_list} degC")
        return temp_list


    def get_flow_sensor(self):
        print("Getting Flow Sensor")
        flow_mA = self.adamAI_D.get_current_inputs(0, 0)[0]
        flow_rate_Lh = self.sensors.current_to_flowmeter(flow_mA)
        print(f"Flow Rate: {flow_rate_Lh} L/hour")
        return flow_rate_Lh


    def get_power_meter(self):
        # getting offset of 2.6 W at zero, under scale by ~ 2 W at upper range
        print("Getting Power Meter Value")
        power_mA = self.adamAI_D.get_current_inputs(1,1)[0]
        #print(f"Power Meter: {power_mA} mA")
        power_W =  self.sensors.current_20mA_to_power(power_mA)
        print(f"Power Consumption: {power_W} W")
        return power_W


    def get_ambient_sensors(self):
        print("Getting Ambient Conditions Sensor")
        ambi_pressure = self.sensors.current_to_pressure(self.adamAI_D.get_current_inputs(2, 2)[0])
        ambi_temperature = self.sensors.current_to_temperature(self.adamAI_D.get_current_inputs(3, 3)[0])
        ambient_sensors = [ambi_temperature,ambi_pressure]
        print(f"Ambient Temp: {ambient_sensors[0]} degC, Ambient Pressure: {ambient_sensors[1]} mBar")
        return ambient_sensors



#TODO: Implement JSON interface using user inputs for CLI


def main():
    print("Starting AC Unit Refrigeration Rig - DEMO")
    # Setup IO Devices & start  library
    ac = acUnit()
    # Set up Initial State
    ac.adamDIO_A.set_all_coils([0,0,0,0,0,0,0,0])   # direct method setting specific controller coil states
    ac.adamDIO_B.set_all_coils([0,0,0,0,0,0,0,0])
    ac.adamDIO_A.get_all_coils()
    ac.adamDIO_B.get_all_coils()
    ac.set_compressor(False)
    ac.set_fans(False)
    print("AC Unit Init Complete - Starting Acquisition & Control loop")
    time.sleep(2)
    iteration = 0
    while(1):
        print(f"{iteration}:", end="\n")
        # Functions to return data to UI
        # tested
        #ac.get_all_valves()
        #ac.get_pressure_sensors()
        ac.get_temp_sensors()
        #ac.get_flow_sensor()
        #ac.get_power_meter()
        #ac.get_ambient_sensors()

        time.sleep(1)
        iteration = iteration + 1
        ## Functions for setting acUnit State
        #ac.set_valve(5, True)    ## abstracted method setting ac valve state
        ##ac.set_valve(6, True)
        #ac.set_compressor(True)
        #ac.set_fans(True)
        #time.sleep(5)
        #ac.adamDIO_A.set_all_coils([1,1,1,1,1,1,1,1])
        if (iteration/2).is_integer():
            ##ac.set_valve(5, False)  ## abstracted method setting ac valve state
            ##ac.set_valve(6, False)
            continue







if __name__ == "__main__":
    main()
    print("Program Quit")

