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
import acUnitGlobals as glbs

#test_command = '{"set":"V1", "state":"open"}'


json_commands = {
    "set" : {
        "V1" : 0,
        "V2" : 0,
        "V3" : 0,
        "V4" : 0,
        "V5" : 0,
        "V6" : 0,
        "V7" : 0,
        "V8" : 0,
        "W1" : 0,
        "W2" : 0,
        "V_comp" : 0,
    },
    "get" : {
        "data" : 0,
        "valves" : 0,
        "sensors" : 0
    },
    "change" : 0
}

test_command = '{"cmd": "set", "V1": "open", "v2":"ON", "V3":"OPEN", "V_comp":"OFF", "w1":"true", "w2":"close"}'
test_2 = '{"cmd": "change", "state":5}'
test_3 = '{"cmd":"get"}'
test_4 = '{"cmd":"change", "state": "manual"}'

class jsonParser:
    def __init__(self):
        self.data_dic = glbs.acUnit_dictionary
        self.json_template = json.dumps(self.data_dic, indent=2)
        self.valve_list = ["V1","V2","V3","V4","V5","V6","V7","V8"]
        self.relay_list = ["W1","W2", "V_COMP"]
        self.outputs_list = self.valve_list + self.relay_list
        self.ps_list = ["PS1","PS2","PS3"]
        self.ts_list = ["TS1","TS2","TS3","TS4","TS5"]
        self.sense_misc_list = ["flow", "power", "APS", "ATS"]
        self.history_param_list = ["dTdt", "average", "least_mean_sqr", "min", "max"]
        #print(self.json_template)

    '''
    JSON Command -> output
    if command is "set" "item" "status:
        return "set" "item" "status"    
    if command is "get"
        return "get"
    if command is "change" "new-state"
        return "new-state"

    this will be input into the state machine controller to change/set the state

    '''


    def parse_json(self, json_string):
        print(f"JSON String: {json_string}")
        command_dic = json.loads(json_string)
        ## function to make all values lowercase
        command_dic = {key.lower(): val.lower() for key, val in command_dic.items()} ## Using dict comprehension (memory intensive?)
        print(f" Command Dic: {command_dic}")
        cmd = command_dic.get("cmd")   ## NOTE better method for extracting from dictionary
        print(f" cmd: {cmd}")
        if (cmd == "set"):
            print("Set Command Received")
            set_outputs = []
            for output in self.outputs_list:
                print(f"checking output: {output}")
                state = command_dic.get(output.casefold())
                print(f"{output} State: {state}")
                if state == None:
                    print(f"No Value Found for {output} ")
                else:
                    state = state.lower()
                if state == "open" or state == "on" or state == "true" or state == True:
                    set_outputs.append(output)
                    set_outputs.append(True)
                elif state == "close" or state == "off" or state == "false" or state == False:
                    set_outputs.append(output)
                    set_outputs.append(False)
                else:
                    print(f"No Value found for set:item:state: {cmd}:{output}:{state}")
            print(set_outputs)
            return(set_outputs)
        elif (cmd == "get"):
            print("Get Command Received")
            return "get"
        elif (cmd == None):
            print("cmd returned NoneType")
        else:
            print("Unable to Parse JSON cmd")






    def dump_json(self, dictionary):
        self.json_template = json.dumps(self.data_dic, indent=2)
        print(self.json_template)
        return self.json_template








def main():
    parse = jsonParser()
    parse.parse_json(test_command)






if __name__ == "__main__":
    main()
    print("Program Quit")




