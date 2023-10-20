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

class sensorConversion:
    def __init__(self):
        print(f'Sensor Voltage/Current to Process Value Libary')


    def current_to_flowmeter(self, current_mA, range_min=2, range_max=25, offset=1.3):   # for ABB D10A3255xxA1 flowmeter
        range = range_max - range_min
        flow_per_mA = range/16
        flowrate = round(((flow_per_mA * (current_mA-4))+ offset),3)       #
        print(f"Convert Current: {current_mA} to flow-rate: {flowrate} L/h")
        print("ERROR/TODO: Calculated value does not precicely match guage value")
        return flowrate






def main():
    print("Starting GUNT Refridgeration Rig - DEMO")
    # Setup IO Devices
    adamDIO_A = adam6052.adam6052ModBus(ADAM_6052_A_IP, PORT)
    adamDIO_B = adam6052.adam6052ModBus(ADAM_6052_B_IP, PORT)
    adamAI_C = adam6217.adam6217ModBus(ADAM_6217_A_IP, PORT)    #0-10v in for temp & pressure sensors
    adamAI_D = adam6217.adam6217ModBus(ADAM_6217_B_IP, PORT)    # 4-20mA in for flow sensor
    sense = sensorConversion()
    # Set up Initial State
    adamDIO_A.set_all_coils([0,0,0,0,0,0,0,0])
    adamDIO_B.set_all_coils([0,0,0,0,0,0,0,0])
    print("GUNT Init Complete - Starting Acquisition & Control loop")
    time.sleep(2)
    iteration = 0
    while(1):
        print(f"{iteration}:", end="\n")
        #adamAI_C.get_voltage_inputs()
        current_sense_vals_mA = adamAI_D.get_current_inputs()
        flow_meter_current = current_sense_vals_mA[0]  # Flowmeter
        flow_rate_Lh = sense.current_to_flowmeter(flow_meter_current)
        time.sleep(2)
        iteration = iteration + 1




if __name__ == "__main__":
    main()
    print("Program Quit")

