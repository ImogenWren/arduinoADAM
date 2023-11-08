'''
 acUnit Global variable and type definitions

'''
import jsonPacker
import acUnitHardware


# Creating Instances of Global Methods here to ensure that only 1 object of each. Can be renamed in local files
acHardware = acUnitHardware.acUnitHardware()


simulate_hardware = True

test_valve_status = [0,0,0,0,0,0,0,0]

acUnitState = "init"

valve_list = ["V1","V2","V3","V4","V5","V6","V7","V8"]
relay_list = ["W1","W2", "V_comp"]
ps_list = ["PS1","PS2","PS3"]
ts_list = ["TS1","TS2","TS3","TS4","TS5"]
sense_misc_list = ["flow", "power", "APS", "ATS"]
history_param_list = ["dTdt", "average", "least_mean_sqr", "min", "max"]
error_list = ["state", "code", "message"]

pack = jsonPacker.jsonPacker()



acUnit_dictionary = {
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
    "sensors-misc":{
        "flow": 0,
        "power":0,
        "APS" : 0,
        "ATS" : 0
    },
    "sensors-history":{
        "PS1":{
            "dTdt": 0,
            "average": 0,
            "least_mean_sqr": 0,
            "min": 0,
            "max": 0
        },
        "PS2":{
            "dTdt": 0,
            "average": 0,
            "least_mean_sqr": 0,
            "min": 0,
            "max": 0
        },
        "PS3":{
            "dTdt": 0,
            "average": 0,
            "least_mean_sqr": 0,
            "min": 0,
            "max": 0
        },
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
        },
        "flow":{
            "dTdt": 0,
            "average": 0,
            "least_mean_sqr": 0,
            "min": 0,
            "max": 0
        },
        "power":{
            "dTdt": 0,
            "average": 0,
            "least_mean_sqr": 0,
            "min": 0,
            "max": 0
        }
    },
    "error":{
        "state": " ",
        "code":0,
        "message":" "
    }
}

