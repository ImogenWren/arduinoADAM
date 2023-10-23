'''


'''



class sensorCalc:
    def __init__(self):
        print(f'Sensor Voltage/Current to Process Value Library')


    def current_to_flowmeter(self, current_mA, range_min=2, range_max=25, offset=1.3):   # for ABB D10A3255xxA1 flowmeter
        range = range_max - range_min
        flow_per_mA = range/16
        flowrate = round(((flow_per_mA * (current_mA-4))+ offset),3)       #
        print(f"Convert Current: {current_mA} to flow-rate: {flowrate} L/h")
        print("ERROR/TODO: Calculated value does not precisely match gauge value") #TODO Make sure calculations are accurate
        return flowrate
