'''
acUnitMain

'''
import asyncio
import acUnitGlobals as glbs
import acUnitStateMachine

import sensorObjects as so
import jsonParse

parse = jsonParse.jsonParser()

# Renaming global variables to reduce number of things.with.references.to.other.things
hw = glbs.acHardware
# State machine must be defined here to avoid circular references
sm = acUnitStateMachine.acUnitStateMachine()


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


async def gather_data(iteration=0):
    # Sample the hardware IOs: Valves, Power Relays, Pressure Sensors
    #TODO get timestamp when sampling data
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
        print(temp)
        TS_array[i].add_new_datapoint(temp,temps_list[1])
        i = i+1
    # Sample Hardware IOs: Misc Sensors
    misc_list = hw.get_misc_sensors(glbs.simulate_hardware)
    # Add Flow Rate and Power Consumption datapoints to sensor history
    flow.add_new_datapoint(misc_list[0][0], misc_list[1])
    power.add_new_datapoint(misc_list[0][1], misc_list[1])
    # Pack all recorded current datapoints into global dictionary (database)
    glbs.pack.load_valve_data(valve_list)
    glbs.pack.load_relay_data(relay_list)
    glbs.pack.load_pressure_data(pressure_list[0])
    glbs.pack.load_temp_data(temps_list[0])
    glbs.pack.load_misc_data(misc_list[0])
    # Calculate sensor history variables & pack into global dictionary
    glbs.pack.load_history_data("PS1", PS1.calculate_history())
    glbs.pack.load_history_data("PS2", PS2.calculate_history())
    glbs.pack.load_history_data("PS3", PS3.calculate_history())
    i=0
    for sensor in TS_array:
        glbs.pack.load_history_data(glbs.pack.ts_list[i], sensor.calculate_history())
        i = i+1
    glbs.pack.load_history_data("flow", flow.calculate_history())
    glbs.pack.load_history_data("power", power.calculate_history())
    ## Pack error messages
    glbs.pack.load_error_data()
    ## Dump data into JSON format
    #glbs.pack.dump_json()
    #print(iteration)
    iteration += 1
    # TODO write to csv (do as part of add new datapoint) - EDIT: just use JSON message and tap in with seperate python program to store record
    # TODO check functions to calculate history for each sensor
    await asyncio.sleep(1)

async def json_interface(iteration=0):
    command = parse.user_input_json()
    print(command)
    print(iteration)
    iteration += 1
    await asyncio.sleep(1)
    return command

#TODO Move this to JSON parser
expansion_valve_list = ["V1", "V2", "V3", "V4"]

##TODO Define all state names in a list
##TODO write function for each state
##TODO state machine should just run state based on listed name

async def state_machine(state_message=0):
    ## Define states in state machine object, then do selection here?
    #sm.run_state(state_message)
    ## All this logic should be in JSON parser
    if state_message != 0:
        print(state_message)
        if (state_message == "get"):
            glbs.pack.dump_json()
            ##TODO function to return JSON?
            #sm.state_waiting() Not sure this does anything
            return 0
        elif (state_message[0] in expansion_valve_list):  ## if the valve requested is an expansion valve
            print(f"Selecting Expansion Valve {state_message[0]}")
            error = sm.select_expansion_valve(state_message[0])
            return error
        elif (state_message[0] in glbs.valve_list):
            print(f"O")
    else:
        sm.state_waiting()
    #TODO should this function be doing all of the JSON responses? (NO)
    await asyncio.sleep(1)



#using asyncio each "task" should be defined as an async option.
# tasks detailed below
"""
task: gather-data: save into current state dictionary, update 5 mins of samples to buffers, update csv with timestamp, calculate sensor history
task: listen for JSON messages and parse commands -> do all sorting here
task: run-state-machine: set hardware IO and system state in response to commands
"""


def main():
    i = 0
    while(1):
        status = asyncio.run(gather_data(i))
        command = asyncio.run(json_interface(i))
        error = asyncio.run(state_machine(command))  ##
        if (error):
            glbs.pack.load_error_data(error)
            glbs.pack.dump_json()
        i = i+1





if __name__ == '__main__':
    main()

