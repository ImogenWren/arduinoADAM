"""
 acUnit State machine

 is this better defined as part of acUnit?
 - No because acUnit should be called in here as a library


"""


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
#TODO Allow students to move on before turning on both fans? 

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





#import jsonPacker
import acUnitGlobals as glbs
import time


class acUnitStateMachine:
    def __init__(self):
        print("Starting AC Unit Refrigeration Rig - State Machine")
        self.current_state = 0
        self.last_state = 0
        self.next_state = 0
        #self.hw = acUnitHardware.acUnitHardware()
        self.initial_conditions = {}
        self.state_names = ["init", "waiting"]
        self.state_functions = [self.state_waiting()]
        #self.pack = jsonPacker.jsonPacker()  ## try moving this to globals
        print(f"init state = {self.current_state}")



    def run_state(self, state_message=0):
        if state_message != 0:
            print(f"\nCurrent State: {self.current_state}")
            print(f"New State: {state_message}")


    def state_init(self):
        print("Initialising State Machine")
        #hw.adamDIO_A.set_all_coils([0, 0, 0, 0, 0, 0, 0, 0])  # direct method setting specific controller coil states
        #hw.adamDIO_B.set_all_coils([0, 0, 0, 0, 0, 0, 0, 0])
        #ac.adamDIO_A.get_all_coils()
        #ac.adamDIO_B.get_all_coils()
        #ac.set_compressor(False)
        #ac.set_fans(False)
        print("AC Unit Init Complete - Starting Acquisition & Control loop")

    def state_waiting(self):
        glbs.acUnitState = "waiting"
        return 0

    def state_close_expansion_valves(self, current_state=[0,0,0,0,0,0,0,0]):
        glbs.acUnitState = "close-expansion-valves"
        hw.adamDIO_A.set_all_coils([0,0,0,0])   ## TODO dont know if this will work with just 4 datapoints will have to test else:
        #cs = current_state
        #hw.adamDIO_A.set_all_coils([0,0,0,0,cs[4],cs[5],cs[6],cs[7]])
        return 0

    def state_open_expansion_valve(self, valve_name):
        print("makethiswork")



    def select_expansion_valve(self, valve_name):
        ## Check that expansion valve is not already open
        glbs.acUnitState = "select-expansion-valve"
        valve_state = hw.get_all_valves(glbs.simulate_hardware)
        print(valve_state[0:4])
        print(valve_name)
        if (1 in valve_state[0:4]):
            error = ("Error Expansion Valve Already Selected", 9)
            print(error)
            return error
        else:
            error = self.state_open_expansion_valve(valve_name)
            print(error)
            return error







    '''
    ADVANCED STATE MACHINE
    >>>TOO MUCH DONT DO IT<<<
    
    '''



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
        #self.hw.set_compressor(False)
        #self.hw.set_fans(False)
        time.sleep(2) # allow system to stabilise
        self.hw.get_all_data()  # this saves all data into the global dictionary
        #TODO use data in init dictionary for self testing

    '''
    #1 hold state - waiting-for-user
        - wait for start command    
    '''
    def state_wait_for_user(self):
        print("State: wait-for-user")
        user = "no"
        while (user != "yes"):
            user = input("Start Experiment? Type \"yes\" to begin..")
        print("Starting acUnit Experiment")
        #TODO add JSON parser, only respond to start message


    '''
    # 2 transition state - user-start
    - sample sensors
    - log start conditions
    '''
    def state_user_start(self):
        print("State: user-start")
        self.hw.get_all_data()
        self.initial_conditions = glbs.acUnit_dictionary
        glbs.pack.dump_json(self.initial_conditions)
        #print(self.initial_conditions)


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
        #TODO really need to start adding sensor history here


    '''    
    #4 state - start-fans
    - allow user to access:
    W1: on
    W2: on
    '''
    def state_start_fans(self):
        print("State: start-fans")
        #TODO add JSON parser, only respond to start fans command


    '''
    #5 state - open-experiment-valves
    - allow user to access:
    V5: open
    V6: open
    '''
    def state_open_experiment_valves(self):
        print("State: start-fans")
        #TODO add JSON parser, only respond to open valves 5 and 6

    '''
    #6 state - select-expansion-valve
    - allow user to access:
    V1 xor V2 xor V3 xor V4: open
    '''

    def state_select_expansion_valve(self):
        print("State select expansion valves")
        # TODO add JSON parser, only respond to open valves V1 or V2 or V3 or V4



    '''
    #7 hold state - check-pre-compressor
    - sample sensors (1000mS)
    check:
    - dt/dT <= 0.1 degC/min  
    - flow < 3
    - 0 < PS1 < 8 bar 
    - 0 < PS2 < 8 bar 
    - 0 < PS3 < 8 bar
    '''
    def state_check_pre_compressor(self):
        print("State check-pre-compressor")




    ''' 
    #8 s   tate - power-compressor
    - allow user to access:
    V_comp: on
    ...
    

    ...
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
'''
'''
#10 state - experiment-finished-comp-off
- allow user to access:
V_comp: off
check:
V_comp_E == 0
'''
'''
#11 state - experiment-finished--ex-valve-shut
- allow user to access:
V1 xor V2 xor V3 xor V4: close
check:
- flow == 0 L/h
'''
'''
#12 hold state - cool-down
- start cool-down timer
- sample sensors (1000mS)
wait:
- timer > 30 mins
- dt/dT <= 0.1 degC/min   ?(sampled over at least 5 minutes)?
'''
'''
#13 state - re-run-user-select
- wait for user selection
IF (re-run): GOTO state 6
else: GOTO state 14
'''
'''
#14 state - experiment-finished-fans-off
- allow user to access:
W1: off
W2: off
'''
'''
#15 state - experiment-finished-all-valves-shut
check: flow == 0 L/h
- allow user to access:
V5: close
V6: close

'''
'''
#16 state - wait-for-next-user
GOTO: state 0
OR
safe-to-shutdown? -> GOTO state 17
'''
'''
#17 state - shutdown
- no additional items
power off equipment
'''
'''
#20 state - manual-mode
- All valves are available for manual control
- all sensor data to be reported in response to get data command
'''
'''
#21 state - safety-stop
- V_comp: off
- W1: off
- W2: off
- adamDIO_A: [0,0,0,0,0,0,0,0]
- adamDIO_B: [0,0,0,0,0,0,0,0]
'''
'''
#undefined - power-loss
power loss will cause:
- V_comp: stop
- W1: stop
- W2: stop
all valves to shut.
condition is safe

    
    '''



def main():
    sm = acUnitStateMachine()
    sm.state_init()
    sm.state_wait_for_user()
    sm.state_user_start()
    sm.state_check_init_conditions()


if __name__ == "__main__":
    main()
    print("Program Quit")
