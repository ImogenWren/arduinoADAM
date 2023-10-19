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
ADAM_6052_IP = "192.168.1.111"
ADAM_6217_A_IP = "192.168.1.112"
ADAM_6217_B_IP = "192.168.1.115"

PORT = 502

'''
IO List
# DO
V1 = adamDIO.DO_list[0]
V2 = adamDIO.DO_list[1]
V3 = adamDIO.DO_list[2]
V4 = adamDIO.DO_list[3]
V5 = adamDIO.DO_list[4]
V6 = adamDIO.DO_list[5]
V7 = adamDIO.DO_list[6]
V8 = adamDIO.DO_list[7]

#Voltage AI
PS1 = adamAI_A.AI_list[0]
PS2 = adamAI_A.AI_list[1]
PS3 = adamAI_A.AI_list[2]
TC1 = adamAI_A.AI_list[3]
TC2 = adamAI_A.AI_list[4]
TC3 = adamAI_A.AI_list[5]
TC4 = adamAI_A.AI_list[6]
TC5 = adamAI_A.AI_list[7]

#Current AI
flow_meter = adamAI_B.AI_list[0]


'''




def main():
    print("Starting GUNT Refridgeration Rig - DEMO")
    adamDIO = adam6052.adam6052ModBus(ADAM_6052_IP, PORT)
    adamAI_A = adam6217.adam6217ModBus(ADAM_6217_A_IP, PORT)    #0-10v in for temp & pressure sensors
    adamAI_B = adam6217.adam6217ModBus(ADAM_6217_B_IP, PORT)    # 4-20mA in for flow sensor
    while(1):
        adamAI_B.get_current_inputs()
        time.sleep(2)




if __name__ == "__main__":
    main()
    print("Program Quit")

