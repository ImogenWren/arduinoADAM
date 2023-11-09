'''
acUnitMain


understanding asyncio
https://medium.com/dev-bits/a-minimalistic-guide-for-understanding-asyncio-in-python-52c436c244ea
'''
import asyncio
from threading import Thread
thread_running = True
import acUnitGlobals as glbs
import acUnitStateMachine
import time

import sensorObjects as so
import jsonParse

parse = jsonParse.jsonParser()

# Renaming global variables to reduce number of things.with.references.to.other.things
hw = glbs.acHardware
pack = glbs.jsonPack
# State machine must be defined here to avoid circular references
#sm = acUnitStateMachine.init_state()


PS1 = so.temperatureSensor()     ## method for datalogging and analysis is generic at the moment
PS2 = so.temperatureSensor()
PS3 = so.temperatureSensor()
TS1 = so.temperatureSensor()
TS2 = so.temperatureSensor()
TS3 = so.temperatureSensor()
TS4 = so.temperatureSensor()
TS5 = so.temperatureSensor()
flow = so.temperatureSensor()
power = so.temperatureSensor()

PS_array = [PS1, PS2, PS3]
TS_array = [TS1, TS2, TS3, TS4, TS5]


#async def gather_data(iteration=0):
def gather_data(iteration=0):
    global thread_running
    # Sample the hardware IOs: Valves, Power Relays, Pressure Sensors
    #TODO get timestamp when sampling data
    start_time = time.time()
    while thread_running:
        valve_list = hw.get_all_valves(glbs.simulate_hardware)
        relay_list = hw.get_power_relays(glbs.simulate_hardware)
        pressure_list = hw.get_pressure_sensors(glbs.simulate_hardware)
        # add pressure sensor datapoints to sensor history
        PS1.add_new_datapoint(pressure_list[0][0],pressure_list[1])
        PS2.add_new_datapoint(pressure_list[0][1],pressure_list[1])
        PS3.add_new_datapoint(pressure_list[0][2],pressure_list[1])
        # Sample Hardware IOs: Temperature Sensors
        temps_list = hw.get_temp_sensors(glbs.simulate_hardware)
        i = 0
        # Add temperature datapoints to sensor history
        for temp in temps_list[0]:
            #print(temp)
            TS_array[i].add_new_datapoint(temp,temps_list[1])
            i = i+1
        # Sample Hardware IOs: Misc Sensors
        misc_list = hw.get_misc_sensors(glbs.simulate_hardware)
        # Add Flow Rate and Power Consumption datapoints to sensor history
        flow.add_new_datapoint(misc_list[0][0], misc_list[1])
        power.add_new_datapoint(misc_list[0][1], misc_list[1])
        # Pack all recorded current datapoints into global dictionary (database)
        pack.load_valve_data(valve_list)
        pack.load_relay_data(relay_list)
        pack.load_pressure_data(pressure_list[0])
        pack.load_temp_data(temps_list[0])
        pack.load_misc_data(misc_list[0])
        # Calculate sensor history variables & pack into global dictionary
        pack.load_history_data("PS1", PS1.calculate_history())
        pack.load_history_data("PS2", PS2.calculate_history())
        pack.load_history_data("PS3", PS3.calculate_history())
        i=0
        for sensor in TS_array:
            pack.load_history_data(pack.ts_list[i], sensor.calculate_history())
            i = i+1
        pack.load_history_data("flow", flow.calculate_history())
        pack.load_history_data("power", power.calculate_history())
        ## Pack error messages
        pack.load_error_data()
        ## Dump data into JSON format
        ##pack.dump_json()
        #print(iteration)
        iteration += 1
        # TODO write to csv (do as part of add new datapoint) - EDIT: just use JSON message and tap in with seperate python program to store record
        # TODO check functions to calculate history for each sensor
        #await asyncio.sleep(1)
        time.sleep(1)

#async def json_interface(iteration=0):
def json_interface(iteration=0):
    while(1):
        command = parse.user_input_json()
        print(command)
        #glbs.update_command(command)
        glbs.command_received = True
        glbs.command_queue.append(command)
        print(iteration)
        iteration += 1
        time.sleep(1)
    #await asyncio.sleep(1)


#TODO Move this to JSON parser
expansion_valve_list = ["V1", "V2", "V3", "V4"]

##TODO Define all state names in a list
##TODO write function for each state
##TODO state machine should just run state based on listed name

sm = acUnitStateMachine.init_state()

def state_machine():
    while (1):
        sm()
        #await asyncio.sleep(1)
        #ield from asyncio.sleep(n)

def check_globals():
    print(f"command_received: {glbs.command_received}")
    #wait asyncio.sleep(1)


#using asyncio each "task" should be defined as an async option.
# tasks detailed below
"""
task: gather-data: save into current state dictionary, update 5 mins of samples to buffers, update csv with timestamp, calculate sensor history
task: listen for JSON messages and parse commands -> do all sorting here
task: run-state-machine: set hardware IO and system state in response to commands
"""
# An Event Loop
#loop = asyncio.get_event_loop()

# Create a function to schedule co-routines on the event loop
# then print results and stop the loop
#NOT SURE ABOUT THAT ONE CHEIF
async def run_loop():
    await asyncio.gather(state_machine(), gather_data(), json_interface(), check_globals())




def main():
    i = 0
    t1 = Thread(target=gather_data)
    t2 = Thread(target=state_machine)
    t3 = Thread(target=json_interface)

    t1.start()
    t2.start()
    t3.start()

    t3.join()
    #hile(1):
        #syncio.run(run_loop())
      #asyncio.run(state_machine())
        #asyncio.run(gather_data(i))
        #asyncio.run(json_interface(i))
        #loop = asyncio.get_event_loop()

    i = i+1





if __name__ == '__main__':
    main()

