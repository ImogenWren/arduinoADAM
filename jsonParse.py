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
        "TS1" : 0,
        "TS2" : 0,
        "TS3" : 0,
        "TS4" : 0,
        "TS5" : 0
    },
    "sensors-other":{
        "flow": 0,
        "power":0,
        "APS" : 0,
        "ATS" : 0
    }
}


https://www.w3schools.com/python/python_json.asp

"""

import json


test_command = '{"set":"V1", "state":"open"}'

# parse x:
#cmd = json.loads(test_command)

#print(cmd["set"])


data_dictionary = {
    "valves" : {
        "V1" : 0,
        "V2" : 0,
        "V3" : 0,
        "V4" : 0,
        "V5" : 0,
        "V6" : 0,
        "V7" : 0,
        "V8" : 0
    },
    "power-relays"  :  {
        "W1" : 0,
        "W2" : 0,
        "V_comp": 0
    },
    "sensors-pressure": {
        "PS1" : 0,
        "PS2" : 0,
        "PS3" : 0
    },
    "sensors-temperature": {
        "TS1" : 0,
        "TS2" : 0,
        "TS3" : 0,
        "TS4" : 0,
        "TS5" : 0
    },
    "sensors-other":{
        "flow": 0,
        "power":0,
        "APS" : 0,
        "ATS" : 0
    },
    "sensors-history":{
        "TS1":{
            "dTdt": 0,
            "average": 0,
            "least_mean_sqr": 0,
            "min": 0,
            "max": 0
        },
        "TS2":{
            "dTdt": 0,
            "average": 0,
            "least_mean_sqr": 0,
            "min": 0,
            "max": 0
        },
        "TS3":{
            "dTdt": 0,
            "average": 0,
            "least_mean_sqr": 0,
            "min": 0,
            "max": 0
        },
        "TS4":{
            "dTdt": 0,
            "average": 0,
            "least_mean_sqr": 0,
            "min": 0,
            "max": 0
        },
        "TS5":{
            "dTdt": 0,
            "average": 0,
            "least_mean_sqr": 0,
            "min": 0,
            "max": 0
        }
    }
}

#y = json.dumps(data_dictionary, indent=4)

valves_list = [1,0,1,0,1,0,1,0]

test_dic = {"V1":1, "V2":1}

class jsonParser:
    def __init__(self):
        self.data_dic = data_dictionary
        self.json_template = json.dumps(self.data_dic, indent=2)
        self.valve_list = ["V1","V2","V3","V4","V5","V6","V7","V8"]
        print(self.json_template)

    def dump_json(self, dictionary):
        self.json_template = json.dumps(self.data_dic, indent=4)
        print(self.json_template)




    def load_valve_data(self, valve_list):
        new_list = []
        i = 0
        for state in valve_list:
            part_list = [self.valve_list[i], state]
            new_list.append(part_list)
            i = i+1
        self.data_dic["valves"].update(new_list)
        #print(self.data_dic["valves"])



def main():
    jp = jsonParser()
    jp.load_valve_data(valves_list)
    jp.dump_json(jp.data_dic)



if __name__ == "__main__":
    main()
    print("Program Quit")




