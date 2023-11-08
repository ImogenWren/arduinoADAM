
import time

import time
#print(time.time())

#print(round(time.time()))


class stateMachine:
    def __init__(self):
        print("Testing State Machine Structure")
        self.current_state = "state-two"
        self.state_list = [self.state_init(), self.state_two()]
        self.state_name = ["init", "state-two"]

    def run_state_machine(self):
        state_index = self.state_name.index(self.current_state)
        print(f"State Index for \"{self.current_state}\" is: {state_index}")
        error = self.state_list[state_index]
        return error

    def state_init(self):
        print("Initial State")
        return 0


    def state_two(self):
        print("State Two")
        return 0


sm = stateMachine()

print(sm.run_state_machine())