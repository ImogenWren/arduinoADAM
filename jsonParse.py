"""
JSON Parse

Library to parse JSON messages and output state as a string?

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



https://www.w3schools.com/python/python_json.asp

"""

import json
from typing import List, Any

test_command = '{"set":"V1", "state":"open"}'

# parse x:
#cmd = json.loads(test_command)

#print(cmd["set"])


#y = json.dumps(data_dictionary, indent=4)

valves_list = [1,0,1,0,1,0,1,0]
relays_list = [1,0,1]
pressures_list = [10.23, 8.34, 6.25]
temps_list = [20.24,4.34,8.22,24.8,53.67]
miscs_list = [16.3, 200.1, 1024, 20.34]
histories_list = [0.2, 20.3, 5.82, 4.12, 25.23]



class jsonParser:
    def __init__(self):
        self.data_dic = data_dictionary
        self.json_template = json.dumps(self.data_dic, indent=2)
        self.valve_list = ["V1","V2","V3","V4","V5","V6","V7","V8"]
        self.relay_list = ["W1","W2", "V_comp"]
        self.ps_list = ["PS1","PS2","PS3"]
        self.ts_list = ["TS1","TS2","TS3","TS4","TS5"]
        self.sense_misc_list = ["flow", "power", "APS", "ATS"]
        self.history_param_list = ["dTdt", "average", "least_mean_sqr", "min", "max"]
        #print(self.json_template)

    def dump_json(self, dictionary):
        self.json_template = json.dumps(self.data_dic, indent=2)
        print(self.json_template)
        return self.json_template





    def load_valve_data(self, valve_state_list):
        new_zip = zip(self.valve_list, valve_state_list)  ## zips two lists together into an object of tuples
        new_dic = dict(new_zip)
        self.data_dic["valves"].update(new_dic)

    def load_relay_data(self, relay_state_list):
        new_zip = zip(self.relay_list, relay_state_list)  ## zips two lists together into an object of tuples
        new_dic = dict(new_zip)
        self.data_dic["power-relays"].update(new_dic)


    def load_pressure_data(self, pressure_list):
        new_zip = zip(self.ps_list, pressure_list)  ## zips two lists together into an object of tuples
        new_dic = dict(new_zip)
        self.data_dic["sensors-pressure"].update(new_dic)

    def load_temp_data(self, temp_list):
        new_zip = zip(self.ts_list, temp_list)   ## zips two lists together into an object of tuples
        new_dic = dict(new_zip)
        self.data_dic["sensors-temperature"].update(new_dic)

    def load_misc_data(self, misc_list):
        new_zip = zip(self.sense_misc_list, misc_list)  ## zips two lists together into an object of tuples
        new_dic = dict(new_zip)
        self.data_dic["sensors-misc"].update(new_dic)

    def load_history_data(self, history_list, sensor_name ):
        new_zip = zip(self.history_param_list, history_list)  ## zips two lists together into an object of tuples
        new_dic = dict(new_zip)
        self.data_dic["sensors-history"][sensor_name].update(new_dic)


def main():
    jp = jsonParser()
    jp.load_valve_data(valves_list)
    jp.load_relay_data(relays_list)
    jp.load_pressure_data(pressures_list)
    jp.load_temp_data(temps_list)
    jp.load_misc_data(miscs_list)
    jp.load_history_data(histories_list, "TS3")
    jp.dump_json(jp.data_dic)



if __name__ == "__main__":
    main()
    print("Program Quit")




