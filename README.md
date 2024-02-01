# adam-tcp-controller
Arduino/C++, Python, & LabVIEW interfaces for controlling ADAM industrial Controllers using Ethernet/TCP/ModBus

# Arduino/C++ Implementation



## adamController - Example
**NOTE:** This will be simplified when I have time to reflect JUST the Arduino library & example adamController-example
 
- Electronics:
	- Arduino Mega 2560 development board
	- [Arduino Ethernet Shield 2](https://uk.rs-online.com/web/p/shields-for-arduino/8732285?gb=s)
	- 2x [ADAM 6052 Advantech Data Aquisition Module (DIO)](https://www.impulse-embedded.co.uk/products/adam_6052--Ethernet-Digital-IO-Module.htm) 
	- 2x [ADAM 6271 Advantech Data Aquisition Module (AI)](https://www.impulse-embedded.co.uk/products/adam_6217--Ethernet-Analog-Input-Module.htm)
	- Network Switch
	- 3x DPDT Relays, 24v coil, 240VAC Switching
	- SBC (Single Board Computer) Raspberry Pi/Odroid or similar

## Connecting Automation Hardware
* For detailed wiring diagram see ******

5. Arduino Ethernet sheild can now be mated to Arduino Mega 2560 development board
6. Connect Arduino Mega 2560 to SBC using USB cable
7. Connect Arduino Ethernet Shield to Network Switch using Ethernet Cables
8. Connect 4x ADAM modules to Network Switch using Ethernet Cables


## Controlling Experiment
The experimental hardware can now be controlled using JSON formatted commands sent over Serial USB or UART connection to the Arduino.

### Features:
- Arduino will report system status including all sensor data every 1000mS in JSON format

## Running Experiment (Example Commands)
To setup experiment for basic operation, use the following commands:

## Commands List
_list of suitable commands (Examples, not exhaustive)_
```
{"valve":1, "state":0}
{"valve":2, "state":0}
{"valve":3, "state":0}
{"valve":4, "state":0}
{"valve":5, "state":0}
{"valve":6, "state":0}
{"valve":7, "state":0}

{"valve":1, "state":1}
{"valve":2, "state":1}
{"valve":3, "state":1}
{"valve":4, "state":1}
{"valve":5, "state":1}
{"valve":6, "state":1}
{"valve":7, "state":1}

{"fans":0}
{"fans":1}
  
{"comp":0}
{"comp":1}

{"mode":"stop"}

{"cmd":"fans","param":0}  
 
```



# Python Implementation
 ## Prerequisits
`Python3` <br>
External modules used: <br>
`pyModbusTCP` <br>
`numpy` <br>
I believe this was all that was nessissary to install to run the software on RPi Ubuntu

## Setup
 1. Ensure that `testCommandServer.py` HOST variable is set to loopback address `127.0.0.1` OR address of server host.
 2. Ensure that `testReportingServer.py` HOST variable is set to loopback address `127.0.0.1` OR address of server host.
 3. Ensure that `commandClient.py` HOST variable is set to same address as server
 4. Ensure that `reportingClient.py` HOST variable is set to same address as server
 5. If testing without hardware, ensure that `simulate_hardware = True` set in `acUnitGlobals.py`
 6. Run `testCommandServer.py` and `testReportingServer.py` on host server
 7. Run `main.py` on client server (raspberrypi/SBC in final implementation) It should connect to server with no issues

## Operation
1. Enter commands as prompted in `testCommandServer.py` CLI. Track changes in state and function using CLI for `main.py`. view logfile during operation for debug messages, based on logging level set in `init_logging` in `acUnitGlobals`
2. Ensure that JSON messages reported by `testReportingServer.py` display "correct" values (if simulated hardware these values somewhat random and static at the moment

## Issues

1. NOTE: 1st command sent from `testCommandServer.py` causes websocket to loose connection & reset. All commands after this should be handled normally.

## Command Examples
`{"cmd":"set","{item}":"{state}"}`

```
{"cmd":"set","V1":"open"}
{"cmd":"set","V2":"open"}
{"cmd":"set","V3":"open"}
{"cmd":"set","V4":"open"}
{"cmd":"set","V5":"open"}
{"cmd":"set","V6":"open"}
{"cmd":"set","V7":"open"}

{"cmd":"set","V1":"close"}
{"cmd":"set","V2":"close"}
{"cmd":"set","V3":"close"}
{"cmd":"set","V4":"close"}
{"cmd":"set","V5":"close"}
{"cmd":"set","V6":"close"}
{"cmd":"set","V7":"close"}

{"cmd":"set","W1":"on"}
{"cmd":"set","W1":"off"}
{"cmd":"set","W2":"on"}
{"cmd":"set","W2":"off"}
{"cmd":"set","fans":"on"}
{"cmd":"set","fans":"off"}

{"cmd":"set","comp":"start"}
{"cmd":"set","comp":"stop"}

All the following words evaluate to True:
"open","opened","on","true","high","start"

All the following words evaluate to False:
"close","shut","closed","off","false","low","stop"
    
```

![image](https://github.com/ImogenWren/adam-controller/assets/97303986/7265be20-a3c5-4dae-9d01-df3e64b89851)


