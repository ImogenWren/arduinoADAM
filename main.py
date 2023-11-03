'''
acUnitMain

'''
import asyncio
import acUnitGlobals as glbs
import acUnitHardware
import sensorObjects as so
hw = acUnitHardware.acUnitHardware()
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

iteration = 0
async def gather_data(iteration=0):
    valve_list = hw.get_all_valves(glbs.simulate_hardware)
    relay_list = hw.get_power_relays(glbs.simulate_hardware)
    pressure_list = hw.get_pressure_sensors(glbs.simulate_hardware)
    PS1.add_new_datapoint(pressure_list[0])
    PS2.add_new_datapoint(pressure_list[1])
    PS3.add_new_datapoint(pressure_list[2])
    temps_list = hw.get_temp_sensors(glbs.simulate_hardware)
    i = 0
    for temp in temps_list:
        TS_array[i].add_new_datapoint(temp)
        i = i+1
    misc_list = hw.get_misc_sensors(glbs.simulate_hardware)
    flow.add_new_datapoint(misc_list[0])
    power.add_new_datapoint(misc_list[1])

    glbs.pack.load_valve_data(valve_list)
    glbs.pack.load_relay_data(relay_list)
    glbs.pack.load_pressure_data(pressure_list)
    glbs.pack.load_temp_data(temps_list)
    glbs.pack.load_misc_data(misc_list)
    glbs.pack.load_history_data("PS1", PS1.calculate_history())
    glbs.pack.load_history_data("PS2", PS2.calculate_history())
    glbs.pack.load_history_data("PS3", PS3.calculate_history())
    i=0
    for sensor in TS_array:
        glbs.pack.load_history_data(glbs.pack.ts_list[i], sensor.calculate_history())
        i = i+1
    glbs.pack.load_history_data("flow", flow.calculate_history())
    glbs.pack.load_history_data("power", power.calculate_history())
    glbs.pack.dump_json()
    print(iteration)
    iteration = iteration+1



    # TODO write to csv
    # TODO check functions to calculate history for each sensor

    await asyncio.sleep(1)


#using asyncio each "task" should be defined as an async option.
# tasks detailed below
"""
task: gather-data: save into current state dictionary, update 5 mins of samples to buffers, update csv with timestamp, calculate sensor history
task: listen for JSON messages and parse commands
task: run-state-machine: set hardware IO and system state in response to commands
"""

def main():
    i = 0
    while(1):
        asyncio.run(gather_data(i))
        i = i+1





if __name__ == '__main__':
    main()

