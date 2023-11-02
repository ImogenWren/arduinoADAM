'''
 acUnit State machine

 is this better defined as part of acUnit?
 - No because acUnit should be called in here as a library


'''


'''

 
#0 transition state - init
adamDIO_A: [0,0,0,0,0,0,0,0]
adamDIO_B: [0,0,0,0,0,0,0,0]
W1: off
W2: off
V_comp: off

#1 hold state - waiting-for-user
- wait for start command

#2 transition state - user-start
- sample sensors
- log start conditions


#3 hold state - check-init-conditions
- start timer
- sample sensors (1000mS)
check:
- flow == 0
- all valves shut
- fanA & fan B == off
- compressor == off
- dt/dT <= 0.1 degC/min   (sampled over at least 5 minutes)
wait: 5 minutes


#4 state - start-experiment-fans
- allow user to access:
W1: on
W2: on

#5 state - start-experiment-valves
- allow user to access:
V5: open
V6: open

#6 state - select-expansion-valve
- allow user to access:
V1 xor V2 xor V3 xor V4: open

#7 hold state - check-pre-compressor
- sample sensors (1000mS)
check:
- dt/dT <= 0.1 degC/min   ?(sampled over at least 5 minutes)?
- flow == 0
- 0 < PS1 < 8 bar 
- 0 < PS2 < 8 bar 
- 0 < PS3 < 8 bar
 
#8 state - power-compressor
- allow user to access:
V_comp: on



#9 hold state - experiment-running
- start timer
- sample sensors (1000mS)
- report all sensor values json at regular intervals (1000mS)
check:
- flow > 0 L/h
- 0 < PS1 < 8 bar 
- 0 < PS2 < 8 bar 
- 0 < PS3 < 8 bar
- 0 < TS1 < 90 degC 
- 0 < TS2 < 90 degC  
- 0 < TS3 < 90 degC 
- 0 < TS4 < 90 degC  
- 0 < TS5 < 90 degC 
wait:
- timer > 30 mins
OR
- dt/dT <= 0.1 degC/min   ?(sampled over at least 5 minutes)?
OR
- User Input


#10 state - experiment-finished-comp-off
- allow user to access:
V_comp: off
check:
V_comp_E == 0


#11 state - experiment-finished--ex-valve-shut
- allow user to access:
V1 xor V2 xor V3 xor V4: close
check:
- flow == 0 L/h

#12 hold state - cool-down
- start cool-down timer
- sample sensors (1000mS)
wait:
- timer > 30 mins
- dt/dT <= 0.1 degC/min   ?(sampled over at least 5 minutes)?

#13 state - re-run-user-select
- wait for user selection
IF (re-run): GOTO state 6
else: GOTO state 14

#14 state - experiment-finished-fans-off
- allow user to access:
W1: off
W2: off

#15 state - experiment-finished-all-valves-shut
check: flow == 0 L/h
- allow user to access:
V5: close
V6: close

#16 state - wait-for-next-user
GOTO: state 0
OR
safe-to-shutdown? -> GOTO state 17

#17 state - shutdown
- no additional items
power off equipment


#20 state - manual-mode
- All valves are available for manual control
- all sensor data to be reported in response to get data command

#21 state - safety-stop
- V_comp: off
- W1: off
- W2: off
- adamDIO_A: [0,0,0,0,0,0,0,0]
- adamDIO_B: [0,0,0,0,0,0,0,0]

#undefined - power-loss
power loss will cause:
- V_comp: stop
- W1: stop
- W2: stop
all valves to shut.
condition is safe





'''




import acUnitHardware
import jsonPacker
import time

class acUnitStateMachine:
    def __init__(self):
        print("Starting AC Unit Refrigeration Rig - State Machine")
        self.current_state = 0
        self.last_state = 0
        self.next_state = 0
        self.hw = acUnitHardware.acUnitHardware()
        self.pack = jsonPacker.jsonPacker()
        print(f"init state = {self.current_state}")

    def run_state(self, newstate):
        print(f"\nCurrent State: {self.current_state}")
        print(f"changing state to: {newstate}")
        self.last_state = self.current_state
        print(f"Last State: {self.last_state}")
        self.current_state = newstate
        print(f"Current State: {self.current_state}")
        self.next_state = self.current_state
        print(f"Next State: {self.next_state}")

    '''
    # 0 transition state - init
    adamDIO_A: [0, 0, 0, 0, 0, 0, 0, 0]
    adamDIO_B: [0, 0, 0, 0, 0, 0, 0, 0]
    W1: off
    W2: off
    V_comp: off
    '''
    def state_init(self):
        print("acUnit - State: init")
        #self.hw.adamDIO_A.set_all_coils([0, 0, 0, 0, 0, 0, 0, 0])  # direct method setting specific controller coil states
        #self.hw.adamDIO_B.set_all_coils([0, 0, 0, 0, 0, 0, 0, 0])
        #self.hw.adamDIO_A.get_all_coils()
        #self.hw.adamDIO_B.get_all_coils()
        #self.hw.set_compressor(False)
        #self.hw.set_fans(False)

    '''
    #1 hold state - waiting-for-user
        - wait for start command    
    '''
    def state_wait_for_user(self):
        user = "no"
        while (user != "yes"):
            user = input("Start Experiment? Type \"yes\" to begin..")
        print("Starting acUnit Experiment")


    '''
    # 2 transition state - user-start
    - sample sensors
    - log start conditions
    '''

    def state_user_start(self):
        #valve_list = self.hw.get_all_valves(test_mode=True)
        # self.hw.get_pressure_sensors()
        temp_vals = self.hw.get_temp_sensors(test_mode=True)
        self.pack.load_temp_data(temp_vals)
        self.pack.dump_json(self.pack.data_dic)
        # self.hw.get_flow_sensor()
        # self.hw.get_power_meter()
        # self.hw.get_ambient_sensors()

    '''
    #3 hold state - check-init-conditions
    - start timer
    - sample sensors (1000mS)
    check:
    - flow == 0
    - all valves shut
    - fanA & fan B == off
    - compressor == off
    - dt/dT <= 0.1 degC/min   (sampled over at least 5 minutes)
    wait: 5 minutes
    '''

    def state_check_init_conditions(self):
        print("State: check-init-conditions")




def main():
    sm = acUnitStateMachine()
    sm.state_init()
    sm.state_wait_for_user()
    sm.state_user_start()


if __name__ == "__main__":
    main()
    print("Program Quit")
