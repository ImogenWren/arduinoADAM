'''
guntRig - DEMO

Refrigeration experiment IO demo program.

Demonstraits the function of all hardware IOs. No state machine


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

# Ethernet Delarations
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
V7 = adamDIO_A.DO_list[6]       # Receiver Bypass
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

'''




def test():
    print("Test")

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


class guntFridge:
    def __init__(self):
        print("Starting GUNT Refridgeration Rig - DEMO")
        # Setup IOs
        self.adamDIO_A = adam6052.adam6052ModBus(ADAM_6052_A_IP, PORT)
        self.adamDIO_B = adam6052.adam6052ModBus(ADAM_6052_B_IP, PORT)
        self.adamAI_C = adam6217.adam6217ModBus(ADAM_6217_A_IP, PORT)  # 0-10v in for temp & pressure sensors
        self.adamAI_D = adam6217.adam6217ModBus(ADAM_6217_B_IP, PORT)  # 4-20mA in for flow sensor
        self.sensors = sensorCalc  ## library for sensor conversions
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

    def get_all_valves(self):
        valveStates = self.adamDIO_A.get_coil_range(self.V1, self.V7)
        valve = 1
        for state in valveStates:
            print(f"V{valve} = {state}")
            valve = valve + 1
        return valveStates

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





#TODO CHECK RELAYS IN adamDIO_B NO GROUND WIRE


def main():
    print("Starting GUNT Refridgeration Rig - DEMO")
    # Setup IO Devices & start GUNT library
    gunt = guntFridge()
    # Set up Initial State
    gunt.adamDIO_A.set_all_coils([0,0,0,0,0,0,0,0])   # direct method setting specific controller coil states
    gunt.adamDIO_B.set_all_coils([0,0,0,0,0,0,0,0])
    gunt.adamDIO_A.get_all_coils()
    gunt.adamDIO_B.get_all_coils()
    gunt.set_compressor(False)
    gunt.set_fans(False)
    print("GUNT Init Complete - Starting Acquisition & Control loop")
    time.sleep(2)
    iteration = 0
    while(1):
        print(f"{iteration}:", end="\n")
        gunt.get_all_valves()
        #adamAI_C.get_voltage_inputs()
        #could above lines be compressed into
        #flow_rate_Lh = sense.current_to_flowmeter(adamAI_D.get_current_inputs()[0])
        time.sleep(2)
        iteration = iteration + 1
        gunt.set_valve(5, True)    ## abstracted method setting gunt valve state
        gunt.set_valve(6, True)
        gunt.set_compressor(True)
        gunt.set_fans(True)
        time.sleep(5)
        if (iteration/2).is_integer():
            gunt.set_compressor(False)
            gunt.set_fans(True)
            time.sleep(5)






if __name__ == "__main__":
    main()
    print("Program Quit")

