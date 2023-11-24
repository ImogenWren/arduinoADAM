# adam-controller
 Python and alternative software interfaces for controlling ADAM industrial Controllers

 Current Testing Instructions:

## Setup
 1. Ensure that `manualServer.py` HOST variable is set to loopback address `127.0.0.1` OR address of server host.
 2. Ensure that `websocketClient.py` HOST variable is set to same address as server
 3. If testing without hardware, ensure that `simulate_hardware = True` set in `acUnitGlobals.py`
 4. Run `manualServer.py`
 5. Run `main.py`. It should connect to server with no issues

## Operation
Enter commands as prompted in `manualServer.py` CLI. Track changes in state and function using CLI for `main.py`. view logfile during operation for debug messages, based on logging level set in `init_logging` in `acUnitGlobals`

## Issues

1. NOTE: 1st command sent from `manualServer.py` causes websocket to loose connection & reset. All commands after this should be handled normally.

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
